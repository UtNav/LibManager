from database import connect
from database_docgia import connect_db_docgia
from database_thongke import connect_db_thongke
from database_muontra import connect_db_muontra
from login import show_login

connect()
connect_db_docgia()
connect_db_thongke()
connect_db_muontra()

show_login()
