import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
from services.database_service import DatabaseService

def main():
    print("=" * 50)
    print("🔄 MIGRATING DATABASE TO AUTH SYSTEM")
    print("=" * 50)
    print()

    print("⚠️  WARNING: This will drop all existing data!")
    print("⚠️  Make sure you have backups if needed.")
    print()
    
    response = input("Continue? (yes/no): ")
    if response.lower() != 'yes':
        print("❌ Migration cancelled")
        return

    db = DatabaseService()

    print("\n1. Dropping old tables...")
    try:
        cur = db.conn.cursor()
        cur.execute("DROP TABLE IF EXISTS events CASCADE;")
        cur.execute("DROP TABLE IF EXISTS conversations CASCADE;")
        cur.execute("DROP TABLE IF EXISTS users CASCADE;")
        db.conn.commit()
        cur.close()
        print("✅ Old tables dropped")
    except Exception as e:
        print(f"❌ Error dropping tables: {e}")
        db.conn.rollback()
        db.close()
        return

    print("\n2. Creating new schema...")
    try:
        schema_path = Path(__file__).parent.parent / 'sql' / 'schema.sql'
        with open(schema_path, 'r') as f:
            schema_sql = f.read()
        
        cur = db.conn.cursor()
        cur.execute(schema_sql)
        db.conn.commit()
        cur.close()
        print("✅ New schema created")
    except Exception as e:
        print(f"❌ Error creating schema: {e}")
        db.conn.rollback()
        db.close()
        return

    print("\n" + "=" * 50)
    print("✅ Migration complete!")
    print("=" * 50)
    db.close()

if __name__ == "__main__":
    main()