import sqlite3
from thongke import Thongke

def connect_db_thongke():
    conn = sqlite3.connect("library.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS thongke (
            ma_sach TEXT,
            so_lan_muon TEXT,
            phan_loai TEXT,
            so_luong_muon TEXT,
            so_luong_con_lai TEXT,
            han_tra TEXT
        )
    ''')
    conn.commit()
    conn.close()

def insert_thongke(tk):
    conn = sqlite3.connect("library.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO thongke VALUES (?, ?, ?, ?, ?, ?)", 
                   (tk.ma_sach, tk.so_lan_muon, tk.phan_loai, tk.so_luong_muon, tk.so_luong_con_lai, tk.han_tra))
    conn.commit()
    conn.close()

def update_thongke(tk):
    conn = sqlite3.connect("library.db")
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE thongke SET
            so_lan_muon=?,
            phan_loai=?,
            so_luong_muon=?,
            so_luong_con_lai=?,
            han_tra=?
        WHERE ma_sach=?
    ''', (tk.so_lan_muon, tk.phan_loai, tk.so_luong_muon, tk.so_luong_con_lai, tk.han_tra, tk.ma_sach))
    conn.commit()
    conn.close()

def delete_thongke(ma_sach,han_tra):
    conn = sqlite3.connect("library.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM thongke WHERE ma_sach=? AND han_tra=?", (ma_sach,han_tra))
    conn.commit()
    conn.close()

def get_all_thongke():
    conn = sqlite3.connect("library.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM thongke")
    result = cursor.fetchall()
    conn.close()
    return result
