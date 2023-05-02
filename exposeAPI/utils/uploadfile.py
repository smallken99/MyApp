from config import WORK_FILE
import base64

# 上傳檔案
class Uploadfile:
    def __init__(self):
        pass

    def upload_file(self,base64_string,filenName):
        #print(base64_string)
        fileFullPath = WORK_FILE + filenName
        with open(fileFullPath, "wb") as f:
            f.write(base64.b64decode(base64_string))               
        return fileFullPath 
    
 