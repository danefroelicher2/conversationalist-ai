import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
from services.database_service import DatabaseService

def main():
    print("=" * 50)
    print("🔥 RESETTING DATABASE - ALL DATA WILL BE DELETED")
    print("=" * 50)

    # Get user confirmation
    response = input("\n⚠️  This will delete ALL data. Continue? (yes/no): ")
    if response.lower() != 'yes':
        print("❌ Database reset cancelled")
        return

    db = DatabaseService()

    print("\n1. Dropping existing tables...")
    try:
        # Drop tabless in reverse order off foreign key dependencies
        db.cursor.execute("DROP TABLE IF EXISTS events CASCADE;")
        print("   ✓ Dropped table: events")

        db.cursor.execute("DROP TABLE IF EXISTS conversations CASCADE;")
        print("   ✓ Dropped table: conversations")

        db.cursor.execute("DROP TABLE IF EXISTS users CASCADE;")
        print("   ✓ Dropped table: users")

        db.connection.commit()
        print("✅ All tables dropped successfully")
    except Exception as e:
        print(f"❌ Error dropping tables: {e}")
        db.connection.rollback()
        db.close()
        return

    print("\n2. Creating fresh tables from schema...")
    try:
        # Read and execute schema.sql
        schema_path = Path(__file__).parent.parent / "sql" / "schema.sql"
        with open(schema_path, 'r') as f:
            schema_sql = f.read()

        db.cursor.execute(schema_sql)
        db.connection.commit()
        print("✅ Tables created successfully")
    except Exception as e:
        print(f"❌ Error creating tables: {e}")
        db.connection.rollback()
        db.close()
        return

    print("\n" + "=" * 50)
    print("✅ Database reset complete!")
    print("=" * 50)
    db.close()

if __name__ == "__main__":
    main()
