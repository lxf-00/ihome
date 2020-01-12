from flask import Flask
from config import config_map
from flask_sqlalchemy import SQLAlchemy         # 数据库扩展
import redis
from flask_session import Session               # session 扩展
from flask_wtf import CSRFProtect               # csrf 保护
import logging
from logging.handlers import RotatingFileHandler


# 数据库 （1,先创建数据库对象）
db = SQLAlchemy()

# 创建redis连接对象
redis_store = None


# 设置日志记录的等级
logging.basicConfig(level=logging.DEBUG)    # 调试debug等级
# 创建日志记录器，知名日志保存的路径，每个日志文件的最大大小， 保存日志文件个数的上限
file_log_handler = RotatingFileHandler("logs/log", maxBytes=1024*1024*100, backupCount=10)
# 创建日志记录的格式                  日志等级        输入日志信息的文件名      日志信息
formatter = logging.Formatter("%(levelname)s %(filename)s:%(lineno)d %(message)s")
# 为创建的日志记录器设置日志记录格式
file_log_handler.setFormatter(formatter)
# 为全局日志对象（flask app) 添加日志记录器
logging.getLogger().addHandler(file_log_handler)


# 工厂模式
def create_app(config_name):
    """
    创建flask的应用对象
    :param config_name: str  配置模式的名字 （"develop", "product")
    :return:
    """
    app = Flask(__name__)

    # 根据config_name 从config_map中获取相关配置信息
    config_class = config_map.get(config_name)

    # 导入到flask配置信息中
    app.config.from_object(config_class)

    # 使用app初始化db: 数据库和flask 进行绑定（2, app 创建后使用init_app()进行绑定）
    db.init_app(app)

    # 初始化redis工具
    global redis_store
    redis_store = redis.StrictRedis(host=config_class.REDIS_HOST, port=config_class.REDIS_PORT)

    # 利用flask-session 将session 保存到redis中
    Session(app)

    # 为flask 补充csrf防护机制
    CSRFProtect(app)


    # 注册蓝图
    from ihome_db import api_1_0
    app.register_blueprint(api_1_0.api, url_prefix="/api/v1.0")

    return app