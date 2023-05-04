import eel
from sqlalchemy import create_engine,text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from config import DB_URI,WORK_FILE,DB_URI_MYSQL
from model.userVO import User
from model.orderFormatVO import OrderFormat
from sqlalchemy.engine.reflection import Inspector
import base64


engine = create_engine(DB_URI, echo=True)
Session = sessionmaker(bind=engine)

# 初始化資料表
# Create a declarative base object
Base = declarative_base()
# Add User Object to Base and create the table
Base.metadata.create_all(bind=engine, tables=[User.__table__,OrderFormat.__table__])


# 以下建立欄位
# 檢查欄位是否已經存在
# table_name = 'orderformat'
# column_name = 'created_at'
# inspector = Inspector.from_engine(engine)
# if 'orderformat' in inspector.get_table_names():
#     columns = [c['name'] for c in inspector.get_columns(table_name)]
#     if column_name not in columns:
#         # 新增 created_at 欄位
#         print(f'新增 {column_name} 欄位')
#         with engine.connect() as conn:
#             stmt = text("ALTER TABLE orderformat ADD COLUMN created_at DATETIME DEFAULT NOW()")
#             conn.execute(stmt)


from exposeAPI.userEel import UserAPI
user_eel = UserAPI(Session)
eel.expose(user_eel.add_user)
eel.expose(user_eel.get_users)

# 蝦皮訂單轉檔
from exposeAPI.transferOrderEel import TransferOrderEel
transferOrderEel_eel = TransferOrderEel(Session)
eel.expose(transferOrderEel_eel.transferOrder)


@eel.expose
def download_file1():
    filename = "order.xlsx" # 此方法也可以用在純文字檔
    fileFullPath = WORK_FILE + filename
    with open(fileFullPath, 'rb') as f:
        excel_data = f.read()
        excel_b64 = base64.b64encode(excel_data).decode('utf-8')
        return {"name": filename, "data": excel_b64, "type": 'application/octet-stream'}
    

@eel.expose
def download_file2():
    filename = "example.txt"
    fileFullPath = WORK_FILE + filename
    with open(fileFullPath, "r",encoding="utf-8") as f:
        content = f.read()
    file_type = "text/plain"
    #file_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    return {"name": filename, "data": content, "type": file_type}





eel.init('web')
eel.start('index.html', size=(1000, 800))