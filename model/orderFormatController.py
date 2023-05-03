from model.orderFormatVO import OrderFormat


class OrderFormatCtrl:
    def __init__(self, Session):
        self.session = Session()

    def add_orderFormat(self,OrderFormat):
        self.session.add(OrderFormat)
        self.session.commit()
        return "新增資料成功!"  

    def add_all(self, data_list):
        self.session.add_all(data_list) 
        self.session.commit()
        return "批次新增資料成功!" 

   # 是否已經存在資料庫中了
    def isDuplicate(self, orderNo):
        result = self.session.query(OrderFormat).filter_by(order_no=orderNo).first()
        return result is not None
    
    # 查詢OrderFormat資料表中,所有的order_no
    def queryAllOrderNoList(self):
        return [str(Orders.order_no).strip() for Orders in self.session.query(OrderFormat).all()]
 