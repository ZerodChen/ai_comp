import openai
from sqlalchemy.orm import Session
from app.models.metadata import TableMetadata
from app.core.config import settings
import logging
import os

logger = logging.getLogger(__name__)

class LLMService:
    def __init__(self, db: Session):
        self.db = db
        self.provider = os.getenv("LLM_PROVIDER", "openai").lower()
        self.ollama_base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1")
        self.model = os.getenv("OLLAMA_MODEL", "llama3") if self.provider == "ollama" else "gpt-3.5-turbo"

    def generate_sql(self, connection_id: int, question: str) -> str:
        # 1. Fetch schema for context
        tables = self.db.query(TableMetadata).filter(TableMetadata.connection_id == connection_id).all()
        
        if not tables:
             raise ValueError("No schema metadata found for this connection. Please index the database first.")

        schema_text = ""
        for table in tables:
            # Generate DDL-like schema for better LLM understanding
            schema_text += f"CREATE TABLE {table.table_name} (\n"
            cols = []
            for col in table.columns:
                col_def = f"  {col.column_name} {col.data_type}"
                if col.is_primary_key:
                    col_def += " PRIMARY KEY"
                # Note: FKs could be added here if we stored the target table/col in metadata efficiently
                cols.append(col_def)
            schema_text += ",\n".join(cols)
            schema_text += "\n);\n\n"
            
        # 2. Construct Prompt
        system_prompt = f"""You are an expert database engineer. Convert the user's natural language question into a valid SQL query.
The database schema is as follows:
{schema_text}

Rules:
1. Return ONLY the SQL query. 
2. Do not use markdown blocks (```sql). 
3. Do not add explanations or introductory text.
4. Ensure the SQL is compatible with PostgreSQL.
5. If the question cannot be answered with the schema, return SELECT 'ERROR: Cannot answer'
"""
        
        # 3. Call LLM
        try:
            client = None
            if self.provider == "ollama":
                # Ollama is OpenAI compatible
                client = openai.OpenAI(
                    base_url=self.ollama_base_url,
                    api_key="ollama" # Required but ignored
                )
            else:
                # OpenAI
                if not os.getenv("OPENAI_API_KEY"):
                    raise ValueError("OPENAI_API_KEY is not set. Please configure it in .env or use LLM_PROVIDER=ollama.")
                
                client = openai.OpenAI()

            response = client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": question}
                ],
                temperature=0
            )
            
            sql = response.choices[0].message.content.strip()
            
            # Basic cleanup if LLM returns markdown
            if sql.startswith("```"):
                lines = sql.split("\n")
                if lines[0].startswith("```"):
                    lines = lines[1:]
                if lines[-1].startswith("```"):
                    lines = lines[:-1]
                sql = "\n".join(lines)
            
            # Remove any "Here is the SQL:" prefix if local model is chatty
            sql = sql.replace("Here is the SQL:", "").strip()
            
            return sql.strip()

        except Exception as e:
            logger.error(f"LLM Error: {e}")
            raise e
