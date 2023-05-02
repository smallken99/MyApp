from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class OrderFormat(Base):
    __tablename__ = 'orderformat'

    id = Column(Integer, primary_key=True, autoincrement=True)
    order_no = Column(String(20), nullable=False)
    buyer_name = Column(String(50), nullable=False)
    product_name = Column(String(200), nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_price_tax_included = Column(Float, nullable=False)
    subtotal_tax_included = Column(Float, nullable=False)

    def __init__(self, order_no, buyer_name, product_name, quantity, unit_price_tax_included, subtotal_tax_included):
        self.order_no = order_no
        self.buyer_name = buyer_name
        self.product_name = product_name
        self.quantity = quantity
        self.unit_price_tax_included = unit_price_tax_included
        self.subtotal_tax_included = subtotal_tax_included

    def to_dict(self):
        return {
            'id': self.id,
            'order_no': self.order_no,
            'buyer_name': self.buyer_name,
            'product_name': self.product_name,
            'quantity': self.quantity,
            'unit_price_tax_included': self.unit_price_tax_included,
            'subtotal_tax_included': self.subtotal_tax_included
        }