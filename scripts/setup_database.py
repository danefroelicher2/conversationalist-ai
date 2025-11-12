import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
from services.database_service import DatabaseService

def main():
    print("Setting up database tables...")
    db = DatabaseService()
    schema_path = Path(__file__).parent.parent / 'sql' / 'schema.sql'
    db.execute_sql_file(str(schema_path))
    print("✅ Database setup complete!")
    db.close()

if __name__ == "__main__":
    main()
