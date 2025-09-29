import sqlite3
from docgia import DocGia

def connect_db_docgia():
    conn = sqlite3.connect("library.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS docgia (
            ma_doc_gia TEXT PRIMARY KEY,
            ten TEXT,
            so_dien_thoai TEXT,
            ngay_sinh TEXT,
            so_luong_muon TEXT,
            ngay_cap_the TEXT
        )
    ''')
    conn.commit()
    conn.close()

def insert_docgia(docgia):
    conn = sqlite3.connect("library.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO docgia VALUES (?, ?, ?, ?, ?, ?)", 
                   (docgia.ma_doc_gia, docgia.ten, docgia.so_dien_thoai, docgia.ngay_sinh,
                    docgia.so_luong_muon, docgia.ngay_cap_the))
    conn.commit()
    conn.close()

def update_docgia(docgia):
    conn = sqlite3.connect("library.db")
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE docgia SET
            ten=?,
            so_dien_thoai=?,
            ngay_sinh=?,
            so_luong_muon=?,
            ngay_cap_the=?
        WHERE ma_doc_gia=?
    ''', (docgia.ten, docgia.so_dien_thoai, docgia.ngay_sinh, docgia.so_luong_muon,
          docgia.ngay_cap_the, docgia.ma_doc_gia))
    conn.commit()
    conn.close()

def delete_docgia(ma_doc_gia):
    conn = sqlite3.connect("library.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM docgia WHERE ma_doc_gia=?", (ma_doc_gia,))
    conn.commit()
    conn.close()

def get_all_docgia():
    conn = sqlite3.connect("library.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM docgia")
    results = cursor.fetchall()
    conn.close()
    return results

def search_docgia(ma_doc_gia):
    conn = sqlite3.connect("library.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM docgia WHERE ma_doc_gia LIKE ?", ('%' + ma_doc_gia + '%',))
    results = cursor.fetchall()
    conn.close()
    return results
