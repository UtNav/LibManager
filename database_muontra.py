import sqlite3
from muontra import MuonTra

def connect_db_muontra():
    conn = sqlite3.connect("library.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS muontra (
            ma_phieu TEXT PRIMARY KEY,
            ma_doc_gia TEXT,
            ma_sach TEXT,
            ngay_muon TEXT,
            han_tra TEXT,
            ngay_tra TEXT,
            trang_thai TEXT
        )
    ''')
    conn.commit()
    conn.close()

def insert_muontra(mt):
    conn = sqlite3.connect("library.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO muontra VALUES (?, ?, ?, ?, ?, ?, ?)", 
                   (mt.ma_phieu, mt.ma_doc_gia, mt.ma_sach, mt.ngay_muon,
                    mt.han_tra, mt.ngay_tra, mt.trang_thai))
    conn.commit()
    conn.close()

def update_muontra(mt):
    conn = sqlite3.connect("library.db")
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE muontra SET
            ma_doc_gia=?,
            ma_sach=?,
            ngay_muon=?,
            han_tra=?,
            ngay_tra=?,
            trang_thai=?
        WHERE ma_phieu=?
    ''', (mt.ma_doc_gia, mt.ma_sach, mt.ngay_muon, mt.han_tra,
          mt.ngay_tra, mt.trang_thai, mt.ma_phieu))
    conn.commit()
    conn.close()

def delete_muontra(ma_phieu):
    conn = sqlite3.connect("library.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM muontra WHERE ma_phieu=?", (ma_phieu,))
    conn.commit()
    conn.close()

def get_all_muontra():
    conn = sqlite3.connect("library.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM muontra")
    result = cursor.fetchall()
    conn.close()
    return result

def search_muontra(ma_phieu):
    conn = sqlite3.connect("library.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM muontra WHERE ma_phieu LIKE ?", ('%' + ma_phieu + '%',))
    result = cursor.fetchall()
    conn.close()
    return result
