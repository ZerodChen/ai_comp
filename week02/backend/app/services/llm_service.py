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

    def generate_sql(self, connection_id: int, question: str) -> str:
        # 1. Fetch schema for context
        tables = self.db.query(TableMetadata).filter(TableMetadata.connection_id == connection_id).all()
        
        if not tables:
             raise ValueError("No schema metadata found for this connection. Please index the database first.")

        schema_text = ""
        for table in tables:
            schema_text += f"Table: {table.table_name}\nColumns:\n"
            for col in table.columns:
                schema_text += f"  - {col.column_name} ({col.data_type})\n"
            schema_text += "\n"
            
        # 2. Construct Prompt
        system_prompt = f"""You are an expert database engineer. Convert the user's natural language question into a valid SQL query.
The database schema is as follows:
{schema_text}

Return ONLY the SQL query. Do not use markdown blocks (```sql). Do not add explanations.
Ensure the SQL is compatible with PostgreSQL (or standard SQL).
"""
        
        # 3. Call LLM
        try:
            # Check if API key exists
            if not os.getenv("OPENAI_API_KEY"):
                # Mock response for testing if no key provided
                logger.warning("OPENAI_API_KEY not found. Returning mock SQL.")
                return "SELECT * FROM users LIMIT 5;" 

            client = openai.OpenAI() # Uses OPENAI_API_KEY env var
            response = client.chat.completions.create(
                model="gpt-3.5-turbo", 
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
            
            return sql.strip()

        except Exception as e:
            logger.error(f"LLM Error: {e}")
            raise e
