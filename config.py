import redis

class Config(object):
    """配置信息"""

    SECRET_KEY = "JGHKHSN*AKJAH1"

    #  数据库
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:123456@172.16.36.164:3306/ihome"
    # 将会追踪对象的修改并且发送信号。这需要额外的内存， 如果不必要的可以禁用它
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    # Redis 相关配置
    REDIS_HOST = "172.16.36.164"
    REDIS_PORT = 6379

    # flask-session 配置
    SESSION_TYPE = "redis"
    SESSION_REDIS = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT)
    # 对cookes中的session_id 进行隐藏
    SESSION_USER_SINGER = True
    # session 数据的有效期
    PERMANENT_SESSION_LIFETIME = 86400


class DevelopmentConfig(Config):
    """开发环境配置信息"""
    DEBUG = True


class ProductConfig(Config):
    """生产环境配置信息"""
    pass


config_map = {
    "develop": DevelopmentConfig,
    "product": ProductConfig
}