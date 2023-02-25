from exts import db
from flask_security import UserMixin
from datetime import datetime
# 1.flask db init：这步只需要执行一次
# 2.flask db migrate：识别ORM模型的改变，生成迁移脚步
# 3.flask db upgrade：运行迁移脚本
class GoodsModel(db.Model):
    __tablename__ ="goods"
    id=db.Column(db.BigInteger, primary_key=True,unique=True,nullable=False)
    goodname=db.Column(db.String(100), nullable=False)
    goodproduce=db.Column(db.String(100), nullable=False)
    goodvalue=db.Column(db.Float, nullable=False)

class StoreModel(db.Model):
    __tablename__="store"
    id=db.Column(db.BigInteger, primary_key=True,unique=True,nullable=False)
    storename=db.Column(db.String(100), nullable=False)
    storeplace=db.Column(db.String(100), nullable=False)

# 登录时保存的类需要继承自UserMinin,且需要添加active属性，并且id属性需要命名为id否则需要重写回调函数
#active,如果这是一个活动用户且通过验证，账户也已激活，未被停用，也不符合任何你 的应用拒绝一个账号的条件，返回 True 。不活动的账号可能不会登入（当然， 是在没被强制的情况下）。
class StaffModel(db.Model,UserMixin):
    __tablename__ = "staff"
    id = db.Column(db.BigInteger, primary_key=True,unique=True,nullable=False)
    staffname = db.Column(db.String(100), nullable=False)
    stafftype = db.Column(db.Enum('售货员','商店经理',"管理员"))
    staffsex= db.Column(db.Enum('男','女'))
    staffsalary= db.Column(db.String(100), nullable=False)
    staffworkplace= db.Column(db.BigInteger, db.ForeignKey('store.id'),nullable=False)
    active = db.Column(db.Boolean())
    storename=db.relationship("StoreModel")
class UserModel(db.Model):
    __tablename__="user"
    id=db.Column(db.BigInteger, db.ForeignKey('staff.id'),primary_key=True,unique=True,nullable=False)
    password = db.Column(db.String(100), nullable=False)

class StorgeStoreModel(db.Model):
    __tablename__="storgestore"
    id = db.Column(db.BigInteger, primary_key=True, unique=True, nullable=False,autoincrement=True)
    storgestoregoodid=db.Column(db.BigInteger, db.ForeignKey('storge.id'),nullable=False)
    storgestoreid=db.Column(db.BigInteger, db.ForeignKey('store.id'),nullable=False)
    storgestoretime=db.Column(db.db.String(100), nullable=False)
    storgestorenumber=db.Column(db.BigInteger, nullable=False)
    storgename=db.relationship("StorgeModel")
    storename=db.relationship("StoreModel")

class StorgeModel(db.Model):
    __tablename__="storge"
    id = db.Column(db.BigInteger, primary_key=True, unique=True, nullable=False)
    storgename = db.Column(db.String(100), nullable=False)
    storgeproduce = db.Column(db.String(100), nullable=False)
    storgevalue = db.Column(db.Float, nullable=False)
    storgenumber = db.Column(db.BigInteger, nullable=False)

class RequestModel(db.Model):
    __tablename__="request"
    id = db.Column(db.BigInteger, primary_key=True, unique=True, nullable=False, autoincrement=True)
    requeststorgeid=db.Column(db.BigInteger, db.ForeignKey('storge.id'),nullable=False)
    requeststoreid=db.Column(db.BigInteger, db.ForeignKey('store.id'),nullable=False)
    requestnumber=db.Column(db.BigInteger, nullable=False)
    requestdealnumber = db.Column(db.BigInteger)
    requesttime=db.Column(db.db.String(100), nullable=False)
    requestdealtime=db.Column(db.db.String(100))
    requeststatus=db.Column(db.Boolean())
    deliverstatus = db.Column(db.Integer)
    deliverdealtime=db.Column(db.db.String(100))
    #采用关系获取商品名和商店名  requeststorgename返回的是对应id的一个元组
    requeststorgename=db.relationship("StorgeModel")
    requeststorename=db.relationship("StoreModel")

class SaleModel(db.Model):
    __tablename__ = "sale"
    id = db.Column(db.BigInteger, primary_key=True, unique=True, nullable=False, autoincrement=True)
    salestorgeid = db.Column(db.BigInteger, db.ForeignKey('storge.id'), nullable=False)
    salestoreid = db.Column(db.BigInteger, db.ForeignKey('store.id'), nullable=False)
    salenumber = db.Column(db.BigInteger, nullable=False)
    salevalue = db.Column(db.BigInteger, nullable=False)
    saletime = db.Column(db.db.String(100), nullable=False)
    # 采用关系获取商品名和商店名  requeststorgename返回的是对应id的一个元组
    salestorgename = db.relationship("StorgeModel")
    salestorename = db.relationship("StoreModel")