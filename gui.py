import tkinter as tk
from tkinter import ttk, messagebox
from book import Book
import database
from docgia import DocGia
import database_docgia
from thongke import Thongke  
import database_thongke
from muontra import MuonTra
import database_muontra
import unicodedata 

def run_gui(user_role="admin"):
    window = tk.Tk()
    window.title("Phần mềm Quản lý Thư viện")
    window.geometry("1200x650")

    window.configure(bg="WhiteSmoke")
    style = ttk.Style()
    style.theme_use("default")

    style.configure("Treeview.Heading", background="MidnightBlue", foreground="white", font=('Segoe UI', 10, 'bold'))
    style.configure("Treeview", rowheight=25, font=('Segoe UI', 10))
    style.map('Treeview', background=[('selected', '#347083')])

    def apply_treeview_style(tree):
        tree.tag_configure('oddrow', background="white")
        tree.tag_configure('evenrow', background="#F5F5F5")
        for i, item in enumerate(tree.get_children()):
            tag = 'evenrow' if i % 2 == 0 else 'oddrow'
            tree.item(item, tags=(tag,))

    def style_button(button):
        button.config(
            bg="SteelBlue", fg="white", 
            font=('Segoe UI', 9, 'bold'),
            relief="raised", bd=2, padx=5, pady=2
        )

    tab_control = ttk.Notebook(window)
    allowed_tabs = {
        "admin": ["sach", "docgia", "thongke", "muontra"],
        "thuthu": ["sach", "docgia", "thongke", "muontra"],
        "docgia": ["sach", "docgia"]
    }

    # TAB SÁCH 
    if "sach" in allowed_tabs[user_role]:
        tab_sach = ttk.Frame(tab_control)
        tab_control.add(tab_sach, text='Quản lý Sách')

        labels_sach = ["Mã Sách", "Tên Sách", "Tác Giả", "Số Lượng", "Mã Phiếu Nhập", "Tình Trạng"]
        entries_sach = {}
        for i, label in enumerate(labels_sach):
           tk.Label(tab_sach, text=label).grid(row=i//4, column=(i%4)*2, padx=5, pady=5)
           entry = tk.Entry(tab_sach)
           entry.grid(row=i//4, column=(i%4)*2 +1, padx=5, pady=5)
           entries_sach[label] = entry

        tk.Label(tab_sach, text="Tìm sách:").grid(row=2, column=0, padx=5, pady=5)
        entry_search = tk.Entry(tab_sach)
        entry_search.grid(row=2, column=1, padx=5, pady=5)

        def on_tree_sach_select(event):
           selected = tree_sach.focus()  
           if not selected:
             return
           values = tree_sach.item(selected, 'values')
           for i, label in enumerate(labels_sach):
               entries_sach[label].delete(0, tk.END)
               entries_sach[label].insert(0, values[i])

        tree_sach = ttk.Treeview(tab_sach, columns=labels_sach, show="headings")
        for col in labels_sach:
           if col == "Tên Sách":
              tree_sach.column(col, width=250)
           elif col == "Tác Giả":
              tree_sach.column(col, width=200)
           elif col == "Mã Sách":
              tree_sach.column(col, width=100)
           elif col == "Mã Phiếu Nhập":
              tree_sach.column(col, width=150)
           else:
              tree_sach.column(col, width=120)
           tree_sach.heading(col, text=col)
        tree_sach.grid(row=4, column=0, columnspan=8, padx=10, pady=10)
        tree_sach.bind("<<TreeviewSelect>>", on_tree_sach_select)

        def show_all_books():
           tree_sach.delete(*tree_sach.get_children())
           for row in database.get_all_books():
              tree_sach.insert("", "end", values=row)
           apply_treeview_style(tree_sach)

        def add_book():
            try:
               book = Book(*(entries_sach[label].get() for label in labels_sach))
               book.so_luong = int(book.so_luong)
               database.insert_book(book)
               show_all_books()
               messagebox.showinfo("Thành công", "Đã thêm sách.")
            except Exception as e:
               messagebox.showerror("Lỗi", str(e))

        def update_book():
            try:
               book = Book(*(entries_sach[label].get() for label in labels_sach))
               book.so_luong = int(book.so_luong)
               database.update_book(book)
               show_all_books()
               messagebox.showinfo("Thành công", "Đã cập nhật sách.")
            except Exception as e:
               messagebox.showerror("Lỗi", str(e))
            
        def delete_book():
           ma = entries_sach["Mã Sách"].get()
           if messagebox.askyesno("Xác nhận", f"Xoá sách mã {ma}?"):
              database.delete_book(ma)
              show_all_books()

        def search_book():
            keyword = remove_diacritics(entry_search.get().strip())
            tree_sach.delete(*tree_sach.get_children())
            for row in database.get_all_books():
                row_no_accents = [remove_diacritics(str(col)) for col in row[:3]]  
                if any(keyword in field for field in row_no_accents):
                    tree_sach.insert("", "end", values=row)
            apply_treeview_style(tree_sach)

        def open_muon_sach_form():
            form = tk.Toplevel()
            form.title("Mượn sách")
            form.geometry("500x300")

            labels = ["Mã Độc Giả", "Tên", "Số Điện Thoại", "Ngày Sinh", "Số lượng mượn", "Ngày Cấp Thẻ"]
            form_entries = {}

            for i, label in enumerate(labels):
               tk.Label(form, text=label).grid(row=i, column=0, padx=10, pady=5, sticky="e")
               entry = tk.Entry(form, width=30)
               entry.grid(row=i, column=1, padx=10, pady=5)
               form_entries[label] = entry

            def muon_sach():
                try:
                    dg = DocGia(*(form_entries[label].get() for label in labels))
                    database_docgia.insert_docgia(dg)
                    show_all_docgia()  # Cập nhật bảng trong tab Độc Giả
                    messagebox.showinfo("Thành công", "Đã thêm độc giả và ghi nhận mượn sách.")
                    form.destroy()
                except Exception as e:
                    messagebox.showerror("Lỗi", str(e))

            btn_muon = tk.Button(form, text="Mượn Sách", command=muon_sach, bg="green", fg="white")
            btn_muon.grid(row=len(labels), column=0, columnspan=2, pady=15)        

        btn_add = tk.Button(tab_sach, text="Thêm", command=add_book)
        btn_update = tk.Button(tab_sach, text="Sửa", command=update_book)
        btn_delete = tk.Button(tab_sach, text="Xoá", command=delete_book)
        btn_show = tk.Button(tab_sach, text="Hiển thị", command=show_all_books)
        btn_search = tk.Button(tab_sach, text="Tìm kiếm", command=search_book)
        btn_muon_sach = tk.Button(tab_sach, text="Mượn sách", command=open_muon_sach_form)
        
        btn_add.grid(row=3, column=2)
        btn_update.grid(row=3, column=3)
        btn_delete.grid(row=3, column=4)
        btn_show.grid(row=3, column=5)
        btn_search.grid(row=2, column=2, padx=5, pady=5)
        btn_muon_sach.grid(row=3, column=6)

        for btn in [btn_add, btn_update, btn_delete, btn_show, btn_search, btn_muon_sach]:
           style_button(btn)

        show_all_books()

        if user_role=="docgia":
           btn_add.config(state="disabled")
           btn_update.config(state="disabled")        
           btn_delete.config(state="disabled")

    # TAB ĐỘC GIẢ 
    if "docgia" in allowed_tabs[user_role]:
        tab_docgia = ttk.Frame(tab_control)
        tab_control.add(tab_docgia, text='Quản lý Độc Giả')

        labels_docgia = ["Mã Độc Giả", "Tên", "Số Điện Thoại", "Ngày Sinh", "Số lượng mượn", "Ngày Cấp Thẻ"]
        entries_docgia = {}
        for i, label in enumerate(labels_docgia):
           tk.Label(tab_docgia, text=label).grid(row=i//3, column=(i%3)*2, padx=5, pady=5)
           entry = tk.Entry(tab_docgia)
           entry.grid(row=i//3, column=(i%3)*2+1, padx=5, pady=5)
           entries_docgia[label] = entry

        tk.Label(tab_docgia, text="Tìm tên:").grid(row=4, column=0, padx=5, pady=5, sticky="e")
        entry_search_name = tk.Entry(tab_docgia)
        entry_search_name.grid(row=4, column=1, padx=5, pady=5)

        def on_tree_docgia_select(event):
          selected = tree_docgia.focus()
          if not selected:
            return
          values = tree_docgia.item(selected, 'values')
          for i, label in enumerate(labels_docgia):
            entries_docgia[label].delete(0, tk.END)
            entries_docgia[label].insert(0, values[i])

        tree_docgia = ttk.Treeview(tab_docgia, columns=labels_docgia, show="headings")
        for col in labels_docgia:
           tree_docgia.heading(col, text=col)
           tree_docgia.column(col, width=150)
        tree_docgia.grid(row=3, column=0, columnspan=6, pady=10, padx=10)
        tree_docgia.bind("<<TreeviewSelect>>", on_tree_docgia_select)

        def show_all_docgia():
           tree_docgia.delete(*tree_docgia.get_children())
           for row in database_docgia.get_all_docgia():
               tree_docgia.insert("", "end", values=row)
           apply_treeview_style(tree_docgia)

        def add_docgia():
            try:
               dg = DocGia(*(entries_docgia[label].get() for label in labels_docgia))
               database_docgia.insert_docgia(dg)
               show_all_docgia()
               messagebox.showinfo("Thành công", "Đã thêm độc giả.")
            except Exception as e:
               messagebox.showerror("Lỗi", str(e))

        def update_docgia():
            try:
               dg = DocGia(*(entries_docgia[label].get() for label in labels_docgia))
               database_docgia.update_docgia(dg)
               show_all_docgia()
               messagebox.showinfo("Thành công", "Đã cập nhật độc giả.")
            except Exception as e:
               messagebox.showerror("Lỗi", str(e))

        def delete_docgia():
            ma = entries_docgia["Mã Độc Giả"].get()
            if messagebox.askyesno("Xác nhận", f"Xoá độc giả mã {ma}?"):
               database_docgia.delete_docgia(ma)
               show_all_docgia()

        def search_docgia_by_name():
            keyword = remove_diacritics(entry_search_name.get().strip().lower())
            tree_docgia.delete(*tree_docgia.get_children())
            for row in database_docgia.get_all_docgia():
               if keyword in remove_diacritics(row[1].lower()):  
                  tree_docgia.insert("", "end", values=row)

        btn_add_docgia = tk.Button(tab_docgia, text="Thêm", command=add_docgia)
        btn_update_doc_gia = tk.Button(tab_docgia, text="Sửa", command=update_docgia)
        btn_delete_doc_gia = tk.Button(tab_docgia, text="Xoá", command=delete_docgia)
        btn_show_doc_gia = tk.Button(tab_docgia, text="Hiển thị", command=show_all_docgia)
        btn_search_name = tk.Button(tab_docgia, text="Tìm kiếm", command=search_docgia_by_name)

        btn_add_docgia.grid(row=2, column=2)
        btn_update_doc_gia.grid(row=2, column=3)
        btn_delete_doc_gia.grid(row=2, column=4)
        btn_show_doc_gia.grid(row=2, column=5)
        btn_search_name.grid(row=4, column=2, padx=5, pady=5)

        for btn in [btn_add_docgia, btn_update_doc_gia, btn_delete_doc_gia, btn_show_doc_gia, btn_search_name]:
           style_button(btn)

        show_all_docgia()

        if user_role == "docgia":
           btn_add_docgia.config(state="disabled")
           btn_update_doc_gia.config(state="disabled")        
           btn_delete_doc_gia.config(state="disabled")

    # TAB THỐNG KÊ 
    if "thongke" in allowed_tabs[user_role]:
        tab_thongke = ttk.Frame(tab_control)
        tab_control.add(tab_thongke, text='Quản lý Thống Kê') 

        labels_thongke = ["Mã Sách","Số Lần Mượn","Tình Trạng","Số Lượng Đã Mượn","Số Lượng Còn Lại","Hạn Trả"] 
        entries_thongke = {}
        for i, label in enumerate(labels_thongke):
           tk.Label(tab_thongke, text=label).grid(row=i//2, column=(i%2)*2, padx=5, pady=5)
           entry = tk.Entry(tab_thongke)
           entry.grid(row=i//2, column=(i%2)*2+1, padx=5, pady=5)
           entries_thongke[label] = entry 

        tk.Label(tab_thongke, text="Tìm sách theo tình trạng:").grid(row=3, column=0, padx=5, pady=5)
        entry_search_phanloai = tk.Entry(tab_thongke)
        entry_search_phanloai.grid(row=3, column=1, padx=5, pady=5)

        tk.Label(tab_thongke, text="Tìm theo hạn trả:").grid(row=4, column=0, padx=5, pady=5)
        entry_search_hantra = tk.Entry(tab_thongke)
        entry_search_hantra.grid(row=4, column=1, padx=5, pady=5)

        def on_tree_thongke_select(event):
           selected = tree_thongke.focus()  
           if not selected:
             return
           values = tree_thongke.item(selected, 'values')
           for i, label in enumerate(labels_thongke):
               entries_thongke[label].delete(0, tk.END)
               entries_thongke[label].insert(0, values[i])

        tree_thongke = ttk.Treeview(tab_thongke, columns=labels_thongke, show="headings")
        for col in labels_thongke:
           tree_thongke.heading(col, text=col)
           tree_thongke.column(col, width=180)
        tree_thongke.grid(row=6, column=0, columnspan=4, pady=10, padx=10)
        tree_thongke.bind("<<TreeviewSelect>>", on_tree_thongke_select)

        def show_all_thongke():
           tree_thongke.delete(*tree_thongke.get_children())
           for row in database_thongke.get_all_thongke():
               tree_thongke.insert("", "end", values=row)
           apply_treeview_style(tree_thongke)

        def add_thongke():
            try:
               tg = Thongke(*(entries_thongke[label].get() for label in labels_thongke))
               database_thongke.insert_thongke(tg)
               show_all_thongke()
               messagebox.showinfo("Thành công")
            except Exception as e:
               messagebox.showerror("Lỗi", str(e))

        def update_thongke():
            try:
               tg = Thongke(*(entries_thongke[label].get() for label in labels_thongke))
               database_thongke.update_thongke(tg)
               show_all_thongke()
               messagebox.showinfo("Thành công", "Đã cập nhật.")
            except Exception as e:
               messagebox.showerror("Lỗi", str(e))

        def delete_thongke():
            ma = entries_thongke["Mã Sách"].get()
            hantra = entries_thongke["Hạn Trả"].get()
            if messagebox.askyesno("Xác nhận", f"Xoá thống kê mã {ma}? và hạn{hantra}?"):
               database_thongke.delete_thongke(ma, hantra)
               show_all_thongke()

        def search_thongke():
            keyword = remove_diacritics(entry_search_phanloai.get().strip())
            tree_thongke.delete(*tree_thongke.get_children())
            for row in database_thongke.get_all_thongke():
                row_no_accents = [remove_diacritics(str(col)) for col in row[:3]]  
                if any(keyword in field for field in row_no_accents):
                    tree_thongke.insert("", "end", values=row)
            apply_treeview_style(tree_thongke)

        def search_by_hantra():
            hantra = entry_search_hantra.get().strip().lower()
            tree_thongke.delete(*tree_thongke.get_children())
            for row in database_thongke.get_all_thongke():
                if hantra in str(row[5]).lower():
                    tree_thongke.insert("", "end", values=row)
            apply_treeview_style(tree_thongke)

        btn_add_thong_ke =  tk.Button(tab_thongke, text="Thêm", command=add_thongke)
        btn_update_thong_ke = tk.Button(tab_thongke, text="Sửa", command=update_thongke)
        btn_delete_thong_ke = tk.Button(tab_thongke, text="Xoá", command=delete_thongke)
        btn_show_thong_ke = tk.Button(tab_thongke, text="Hiển thị", command=show_all_thongke)
        btn_search_thongke = tk.Button(tab_thongke, text="Tìm kiếm", command=search_thongke)
        btn_search_hantra = tk.Button(tab_thongke, text="Tìm theo hạn", command=search_by_hantra)
    
        btn_add_thong_ke.grid(row=5, column=0)
        btn_update_thong_ke.grid(row=5, column=1)
        btn_delete_thong_ke.grid(row=5, column=2)
        btn_show_thong_ke.grid(row=5, column=3)
        btn_search_thongke.grid(row=3, column=2, padx=2, pady=5, sticky="w")
        btn_search_hantra.grid(row=4, column=2, padx=2, pady=5, sticky="w")

        for btn in [btn_add_thong_ke, btn_update_thong_ke, btn_delete_thong_ke, btn_show_thong_ke, btn_search_thongke, btn_search_hantra]:
           style_button(btn)

        show_all_thongke()

        if user_role=="thuthu":
           btn_add_thong_ke.config(state="disabled")
           btn_update_doc_gia.config(state="disabled")
           btn_delete_thong_ke.config(state="disabled")

    # TAB MƯỢN TRẢ 
    if "muontra" in allowed_tabs[user_role]:
        tab_muontra = ttk.Frame(tab_control)
        tab_control.add(tab_muontra, text='Quản lý Mượn Trả')

        labels_muontra = ["Mã Phiếu", "Mã Độc Giả", "Mã Sách", "Ngày Mượn", "Hạn Trả", 
                      "Ngày Trả", "Trạng Thái"]
        entries_muontra = {}
        for i, label in enumerate(labels_muontra):
           tk.Label(tab_muontra, text=label).grid(row=i//3, column=(i%3)*2, padx=5, pady=5)
           entry = tk.Entry(tab_muontra)
           entry.grid(row=i//3, column=(i%3)*2+1, padx=5, pady=5)
           entries_muontra[label] = entry

        tk.Label(tab_muontra, text="Tra cứu mã phiếu:").grid(row=3, column=0, padx=5, pady=5)
        entry_search_muontra = tk.Entry(tab_muontra)
        entry_search_muontra.grid(row=3, column=1, padx=5, pady=5)

        def on_tree_muontra_select(event):
           selected = tree_muontra.focus()
           if not selected:
             return
           values = tree_muontra.item(selected, 'values')
           for i, label in enumerate(labels_muontra):
             entries_muontra[label].delete(0, tk.END)
             entries_muontra[label].insert(0, values[i])

        tree_muontra = ttk.Treeview(tab_muontra, columns=labels_muontra, show="headings")
        for col in labels_muontra:
           tree_muontra.heading(col, text=col)
           tree_muontra.column(col, width=150)
        tree_muontra.grid(row=5, column=0, columnspan=6, padx=10, pady=10)
        tree_muontra.bind("<<TreeviewSelect>>", on_tree_muontra_select)

        def show_all_muontra():
           tree_muontra.delete(*tree_muontra.get_children())
           for row in database_muontra.get_all_muontra():
              tree_muontra.insert("", "end", values=row)
           apply_treeview_style(tree_muontra)

        def add_muontra():
            try:
               mt = MuonTra(*(entries_muontra[label].get() for label in labels_muontra))
               database_muontra.insert_muontra(mt)
               show_all_muontra()
               messagebox.showinfo("Thành công", "Đã thêm phiếu mượn.")
            except Exception as e:
               messagebox.showerror("Lỗi", str(e))

        def update_muontra():
            try:
               mt = MuonTra(*(entries_muontra[label].get() for label in labels_muontra))
               database_muontra.update_muontra(mt)
               show_all_muontra()
               messagebox.showinfo("Thành công", "Đã cập nhật phiếu.")
            except Exception as e:
               messagebox.showerror("Lỗi", str(e))

        def delete_muontra():
            ma = entries_muontra["Mã Phiếu"].get()
            if messagebox.askyesno("Xác nhận", f"Trả sách mã {ma}?"):
               database_muontra.delete_muontra(ma)
               show_all_muontra()

        def search_muontra_by_ma_docgia():
            keyword = entry_search_muontra.get().strip()
            tree_muontra.delete(*tree_muontra.get_children())
            for row in database_muontra.get_all_muontra():
                if str(row[0]) == keyword:
                   tree_muontra.insert("", "end", values=row)
            apply_treeview_style(tree_muontra)


        btn_add_muon_tra =  tk.Button(tab_muontra, text="Mượn sách", command=add_muontra)
        btn_update_muon_tra =  tk.Button(tab_muontra, text="Sửa", command=update_muontra)
        btn_delete_muon_tra =  tk.Button(tab_muontra, text="Trả sách", command=delete_muontra)
        btn_show_muon_tra =  tk.Button(tab_muontra, text="Hiển thị", command=show_all_muontra)
        btn_search_muontra = tk.Button(tab_muontra, text="Tìm kiếm", command=search_muontra_by_ma_docgia)
        
        btn_add_muon_tra.grid(row=4, column=2)
        btn_update_muon_tra.grid(row=4, column=3)
        btn_delete_muon_tra.grid(row=4, column=4)
        btn_show_muon_tra.grid(row=4, column=5)
        btn_search_muontra.grid(row=3, column=2, padx=5, pady=5)

        for btn in [btn_add_muon_tra, btn_update_muon_tra, btn_delete_muon_tra, btn_show_muon_tra, btn_search_muontra]:
           style_button(btn)

        show_all_muontra()

        if user_role == "docgia":
           btn_add_muon_tra.config(state="disabled")
           btn_update_muon_tra.config(state="disabled")
           btn_delete_muon_tra.config(state="disabled")

    def remove_diacritics(text):
      return ''.join(c for c in unicodedata.normalize('NFD', text)
                   if unicodedata.category(c) != 'Mn').lower()
    tab_control.pack(expand=1, fill="both")
    window.mainloop()
