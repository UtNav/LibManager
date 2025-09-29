import sqlite3

conn = sqlite3.connect("library.db")
cursor = conn.cursor()

try:
    cursor.execute("ALTER TABLE books ADD COLUMN ma_sach TEXT;")
    conn.commit()
    print("✅ Đã thêm cột 'ma_sach' vào bảng 'books'")
except sqlite3.OperationalError as e:
    print("❌ Có thể cột đã tồn tại hoặc bảng sai tên:", e)

conn.close()
