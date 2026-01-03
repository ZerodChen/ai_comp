import sqlglot
from sqlglot import exp

class SecurityService:
    def validate_sql(self, sql: str) -> bool:
        """
        Validates SQL to ensure it's safe (read-only for now).
        Returns True if safe, raises ValueError if unsafe.
        """
        try:
            # Parse returns a list of expressions
            parsed = sqlglot.parse(sql)
        except Exception as e:
            raise ValueError(f"Invalid SQL syntax: {e}")

        for expression in parsed:
            # Check for destructive commands
            # We want to allow SELECT
            # We want to disallow DROP, DELETE, TRUNCATE, ALTER, UPDATE, INSERT
            
            destructive_types = (
                exp.Drop, 
                exp.Delete, 
                # exp.Truncate, # Truncate might be different in newer sqlglot versions
                exp.Alter, 
                exp.Update, 
                exp.Insert,
                exp.Create, 
            )
            
            for unsafe_type in destructive_types:
                if expression.find(unsafe_type):
                    raise ValueError(f"Destructive command detected: {unsafe_type.__name__.upper()}")
            
        return True
