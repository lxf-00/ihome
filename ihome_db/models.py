from . import db
from datetime import datetime



class BaseModel(object):
    """基类"""
    create_time = db.Column(db.DateTime, default=datetime.now)   # 创建时间
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)  # 更新时间


class User(BaseModel, db.Model):
    """用户模型类"""
    __tablename__ = "ih_user_info"
    id = db.Column(db.Integer, primary_key=True)   # 用户id
    name = db.Column(db.String(32), unique=True, nullable=False)   # 用户昵称
    password_hash = db.Column(db.String(128), nullable=False)    # 加密密码
    phone = db.Column(db.String(11), unique=True, nullable=False)   # 用户手机
    avatar_url = db.Column(db.String(128))     # 用户头像路径
    real_name = db.Column(db.String(20), nullable=False)    # 真实姓名
    id_card = db.Column(db.String(20))     # 身份证号
    houses = db.relationship("House", backref="user")   # 用户发布的房屋
    orders = db.relationship("Order", backref="user")   # 用户下的订单

    # @property
    # def password(self):
    #     """读取属性的函数行为"""
    #     # print(user.password)  读取属性时被调用
    #     # 函数的返回值作为属性值
    #     # return xxx
    #     raise AttributeError("这个属性只能设置，不能读取")
    #
    # @password.setter
    # def password(self, value):
    #     """
    #     设置属性  user.password = xxx
    #     :param: value,设置属性时的数据，原始明文密码
    #     :return:
    #     """
    #     self.password_hash = generate_password_hash(value)


class Area(BaseModel, db.Model):
    """城区"""

    __tablename__ = "ih_area_info"

    id = db.Column(db.Integer, primary_key=True)   # 区域编号
    name = db.Column(db.String(20), nullable=False)  # 区域名称
    houses = db.relationship("House", backref="area")  # 区域内的房屋



# 房屋设施表，建立房屋和设施之间多对多的关系
house_facility = db.Table(
    "ih_house_facility",
    db.Column("house_id", db.Integer, db.ForeignKey("ih_house_info.id"), primary_key=True),   # 房屋编号
    db.Column("facility_id", db.Integer, db.ForeignKey("ih_facility_info.id"), primary_key=True)  # 设施编号
)


class House(BaseModel, db.Model):
    """房屋信息"""

    __tablename__ = "ih_house_info"

    id = db.Column(db.Integer, primary_key=True)   # 房屋编号
    user_id = db.Column(db.Integer, db.ForeignKey("ih_user_info.id"), nullable=False)   # 房屋所属用户的id
    area_id = db.Column(db.Integer, db.ForeignKey("ih_area_info.id"), nullable=False)   # 房屋所在区域的id
    title = db.Column(db.String(64), nullable=False)    # 标题
    price = db.Column(db.Integer, nullable=False)       # 价格
    address = db.Column(db.String(512), nullable=False)  # 地址
    room_count = db.Column(db.Integer, default=1)        # 房间数目
    acreage = db.Column(db.Integer, default=0)          # 房屋面积
    unit = db.Column(db.String(32), default="")          # 房屋单元，如几室几厅
    capacity = db.Column(db.Integer, default=1)         # 房屋最大容纳人数
    beds = db.Column(db.String(64), default="")         # 房屋床铺的配置
    deposit = db.Column(db.Integer, default=0)           # 房屋押金
    min_days = db.Column(db.Integer, default=1)         # 最少入住天数
    max_days = db.Column(db.Integer, default=0)         # 最多入住天数，0表示不限制
    order_count = db.Column(db.Integer, default=0)      # 房屋预定订单数
    index_image_url = db.Column(db.String(256), default="")  # 房屋 主图片路径
    facilities = db.relationship("Facility", secondary=house_facility)  # 房屋设施
    image = db.relationship("HouseImage")   # 房屋图片
    orders = db.relationship("Order", backref="house")   # 房屋的订单


class Facility(BaseModel, db.Model):
    """设施"""

    __tablename__ = "ih_facility_info"

    id = db.Column(db.Integer, primary_key=True)      # 设施编号
    name = db.Column(db.String(128), nullable=False)  # 设施名字


class HouseImage(BaseModel, db.Model):
    """房屋图片"""

    __tablename__ = "ih_house_image"

    id = db.Column(db.Integer, primary_key=True)
    house_id = db.Column(db.Integer, db.ForeignKey("ih_house_info.id"), nullable=False)  # 房屋编号
    url = db.Column(db.String(256), nullable=False)      # 房屋图片路径


class Order(BaseModel, db.Model):
    """房屋订单"""

    __tablename__ = "ih_order_info"

    id = db.Column(db.Integer, primary_key=True)     # 订单id
    user_id = db.Column(db.Integer, db.ForeignKey("ih_user_info.id"), nullable=False)   # 订单所属用户id
    house_id = db.Column(db.Integer, db.ForeignKey("ih_house_info.id"), nullable=False)  # 订单房间的id
    start_date = db.Column(db.DateTime, nullable=False)       # 预定的起始日期
    end_date = db.Column(db.DateTime, nullable=False)         # 预定的结束日期
    days = db.Column(db.Integer, nullable=False)              # 预定的总天数
    house_price = db.Column(db.Integer, nullable=False)       # 房屋的单价
    amonut = db.Column(db.Integer, nullable=False)            # 订单的总金额
    status = db.Column(   # 订单状态
        db.Enum(
            "WAIT_ACCEPT", # 待接单
            "WAIT_PAYMENT", # 待支付
            "PAID",         #  已支付
            "WAIT_COMMENT",    # 待评价
            "CANCELED",    # 已取消
            "REJECTED"     #  已拒单
        ),
        default="WAIT_ACCEPT", index=True)
    comment = db.Column(db.Text)    # 订单的评论信息或拒单理由