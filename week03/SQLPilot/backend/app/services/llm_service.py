import json
import openai
from typing import Tuple, Optional
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

    def generate_sql(self, connection_id: int, question: str) -> Tuple[str, Optional[str]]:
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
1. Return a JSON object with two keys: "sql" and "export_format".
2. "sql": The valid SQL query string.
3. "export_format": "csv" or "json" if the user explicitly asks for export or save as file, otherwise null.
4. Do not use markdown blocks (```json).
5. Do not add explanations or introductory text.
6. Ensure the SQL is compatible with PostgreSQL.
7. If the question cannot be answered with the schema, return "sql": "SELECT 'ERROR: Cannot answer'"
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
                temperature=0,
                response_format={"type": "json_object"}
            )
            
            content = response.choices[0].message.content.strip()
            
            # Basic cleanup if LLM returns markdown
            if content.startswith("```"):
                lines = content.split("\n")
                if lines[0].startswith("```"):
                    lines = lines[1:]
                if lines[-1].startswith("```"):
                    lines = lines[:-1]
                content = "\n".join(lines)
            
            try:
                result = json.loads(content)
                sql = result.get("sql", "").strip()
                export_format = result.get("export_format")
                if export_format:
                    export_format = export_format.lower()
                    if export_format not in ["csv", "json"]:
                        export_format = None
            except json.JSONDecodeError:
                # Fallback if JSON parsing fails, treat entire content as SQL
                logger.warning("LLM did not return valid JSON. Falling back to raw text as SQL.")
                sql = content.strip()
                export_format = None
            
            return sql, export_format

        except Exception as e:
            logger.error(f"LLM Error: {e}")
            raise e
