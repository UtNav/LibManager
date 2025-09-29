import sqlite3

def connect():
    return sqlite3.connect("library.db", timeout=10)

def create_table():
    with connect() as conn:
        cursor = conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS books (
            ma_sach TEXT PRIMARY KEY,
            ten_sach TEXT,
            tac_gia TEXT,
            so_luong INTEGER,
            ma_phieu_nhap TEXT,
            tinh_trang TEXT 
        )
        ''')
        conn.commit()

def insert_book(book):
    create_table()  # Đảm bảo bảng tồn tại
    with connect() as conn:
        cursor = conn.cursor()
        cursor.execute('''
        INSERT INTO books (
            ma_sach, ten_sach, tac_gia, so_luong, ma_phieu_nhap, tinh_trang
        ) VALUES (?, ?, ?, ?, ?, ?)
        ''', (
        book.ma_sach, book.ten_sach, book.tac_gia, book.so_luong, book.ma_phieu_nhap, 
        book.tinh_trang
        ))
        conn.commit()

def update_book(book):
    with connect() as conn:
        cursor = conn.cursor()
        cursor.execute('''
        UPDATE books SET
            ten_sach=?,
            tac_gia=?,
            so_luong=?,
            ma_phieu_nhap=?,
            tinh_trang=?
        WHERE ma_sach=?
        ''', (
        book.ten_sach, book.tac_gia, book.so_luong,
        book.ma_phieu_nhap, book.tinh_trang, book.ma_sach
        ))
        conn.commit()

def delete_book(ma_sach):
    with connect() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM books WHERE ma_sach=?", (ma_sach,))
        conn.commit()

def get_all_books():
    create_table()
    with connect() as conn:
       cursor = conn.cursor()
       cursor.execute("SELECT * FROM books")
       result = cursor.fetchall()
       return result

def search_books(ma_sach):
    with connect() as conn:
       cursor = conn.cursor()
       cursor.execute("SELECT * FROM books WHERE ma_sach LIKE ?", ('%' + ma_sach + '%',))
       result = cursor.fetchall()
       return result
