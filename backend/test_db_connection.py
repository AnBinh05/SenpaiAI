"""Test database connection and table existence."""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.core.database import engine, SessionLocal
from app.models.database import Base, User
from sqlalchemy import inspect

def test_connection():
    """Test database connection."""
    print("🔍 Testing database connection...")
    try:
        # Test connection
        with engine.connect() as conn:
            print("✅ Database connection successful!")
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False
    
    return True

def test_tables():
    """Test if tables exist."""
    print("\n🔍 Checking if tables exist...")
    try:
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        
        required_tables = ["users", "chat_history", "learning_sessions", "documents", "grammar_rules", "vocabulary"]
        
        print(f"Found tables: {tables}")
        
        missing_tables = []
        for table in required_tables:
            if table not in tables:
                missing_tables.append(table)
                print(f"❌ Table '{table}' does NOT exist")
            else:
                print(f"✅ Table '{table}' exists")
        
        if missing_tables:
            print(f"\n⚠️  Missing tables: {missing_tables}")
            print("💡 Run migrations: alembic upgrade head")
            return False
        
        return True
    except Exception as e:
        print(f"❌ Error checking tables: {e}")
        return False

def test_user_model():
    """Test User model."""
    print("\n🔍 Testing User model...")
    try:
        db = SessionLocal()
        # Try to query users table
        count = db.query(User).count()
        print(f"✅ User model works! Current user count: {count}")
        db.close()
        return True
    except Exception as e:
        print(f"❌ User model error: {e}")
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("DATABASE CONNECTION TEST")
    print("=" * 50)
    
    if not test_connection():
        sys.exit(1)
    
    if not test_tables():
        print("\n⚠️  Some tables are missing. Please run migrations:")
        print("   cd backend")
        print("   alembic upgrade head")
        sys.exit(1)
    
    if not test_user_model():
        sys.exit(1)
    
    print("\n" + "=" * 50)
    print("✅ ALL TESTS PASSED!")
    print("=" * 50)
