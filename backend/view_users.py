"""
Script để xem danh sách users và thông tin mật khẩu (hash) trong database.
"""
import sys
import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# Thêm đường dẫn backend vào Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.core.config import settings

def view_users():
    """Xem danh sách users trong database."""
    try:
        # Tạo engine và session
        engine = create_engine(settings.database_url)
        Session = sessionmaker(bind=engine)
        session = Session()
        
        # Query tất cả users
        result = session.execute(text("""
            SELECT 
                id,
                email,
                username,
                hashed_password,
                is_active,
                current_jlpt_level,
                created_at
            FROM users
            ORDER BY created_at DESC
        """))
        
        users = result.fetchall()
        
        if not users:
            print("❌ Không có user nào trong database.")
            return
        
        print(f"\n{'='*80}")
        print(f"📊 DANH SÁCH USERS ({len(users)} user(s))")
        print(f"{'='*80}\n")
        
        for user in users:
            user_id, email, username, hashed_password, is_active, jlpt_level, created_at = user
            
            print(f"👤 User ID: {user_id}")
            print(f"   📧 Email: {email}")
            print(f"   👤 Username: {username}")
            print(f"   🔐 Hash Password: {hashed_password[:50]}...")  # Chỉ hiển thị 50 ký tự đầu
            print(f"   ✅ Active: {is_active}")
            print(f"   📚 JLPT Level: {jlpt_level}")
            print(f"   📅 Created: {created_at}")
            print(f"{'-'*80}\n")
        
        session.close()
        print("✅ Hoàn thành!")
        
    except Exception as e:
        print(f"❌ Lỗi: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    view_users()

