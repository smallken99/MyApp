import pandas as pd
import base64
from model.orderFormatController import OrderFormatCtrl
from model.orderFormatVO import OrderFormat

# 蝦皮訂單轉檔


class TransferOrderEel:
    def __init__(self, session):
        self.orderFormatDAO = OrderFormatCtrl(session)

    def transferOrder(self, base64_string, filenName):
        # print(base64_string)
        # uploadFile = Uploadfile().upload_file(base64_string,filenName)
        # 解碼base64字串
        excel_bytes = base64.b64decode(base64_string)
        # 使用pandas讀取Excel數據
        df = pd.read_excel(excel_bytes, sheet_name='orders')

        # 創建一個空的DataFrame
        newdf = pd.DataFrame(columns=['訂單編號', '發票類型', '載具', '載具顯碼', '載具隱碼', '捐贈對象', '買方統編', '買方名稱', '買方地址',
                             '買方電話', '買方電子信箱', '品名', '課稅別', '數量', '單價(含稅)', '小計金額(含稅)', '商品備註(最多40個字)', '總備註(最多200個字)'])

        # 現在您可以對讀取的數據進行處理
        
        orderRecordList = []
        preOrderNo = ''  # 上一筆訂單編號
        for index, row in df.iterrows():
            orderNo = row['訂單編號']

            # 判斷沒有重覆的資料再繼續轉檔
            if self.orderFormatDAO.isDuplicate(orderNo): continue

            # 發票類型
            invoiceType = 'B2C' if preOrderNo != orderNo else ''

            # 載具
            carrier = '不使用' if preOrderNo != orderNo else ''

            # 買方名稱
            buyerName = row['買家帳號'] if preOrderNo != orderNo else ''

            # 品名
            productItem = row['商品選項名稱']+f'[{orderNo}]' if preOrderNo != orderNo else row['商品選項名稱']

            # 數量
            quantity = int(row['數量'])

            # 單價(含稅)
            unitPrice = int(row['商品活動價格'])

            # 折扣為負數金額,整筆不用出現
            if unitPrice < 0: continue

            # 小計金額(含稅)
            SubtotalAmount = (unitPrice)*(quantity)

            # 添加一行新的數據            
            new_data = {'訂單編號':orderNo, '發票類型': invoiceType, '載具': carrier,'買方名稱': buyerName, 
                        '品名': productItem, '課稅別': '應稅', '數量': quantity , '單價(含稅)': unitPrice, 
                        '小計金額(含稅)': SubtotalAmount}
            # print(row['商品選項名稱'], row['商品原價'], row['數量'])


            # 先保存資料,最後再一起存資料庫
            orderRecordList.append(OrderFormat(orderNo,buyerName,productItem,quantity,unitPrice,SubtotalAmount))
            # 保存上一筆資料
            preOrderNo = orderNo
            # 保存在excel資料表
            newdf.loc[index] = new_data

        # 批次新增資料庫
        self.orderFormatDAO.add_all(orderRecordList)
        # 打印新的DataFrame
        print(newdf.head())

        # 將數據保存為Excel文件
        newFileName = '轉檔後_'+filenName
        newdf.to_excel(f'web/{newFileName}', sheet_name='Worksheet', index=False)

        return newFileName