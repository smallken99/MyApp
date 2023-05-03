import eel
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from config import DB_URI,WORK_FILE,DB_URI_MYSQL
from model.userVO import User
from model.orderFormatVO import OrderFormat
import base64


engine = create_engine(DB_URI, echo=True)
Session = sessionmaker(bind=engine)

# Create a declarative base object
Base = declarative_base()
# Add User Object to Base and create the table
Base.metadata.create_all(bind=engine, tables=[User.__table__,OrderFormat.__table__])

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