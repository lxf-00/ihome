# 自定义转换器，供蓝图路由提取文件
from werkzeug.routing import BaseConverter

# 定义正则转换器
class ReConverter(BaseConverter):
    """"""

    def __init__(self, url_map, regex):
        # 调用父类的初始化方法
        super().__init__(url_map)
        # 保存正则表达式，flask会去使用这个属性来进行路由的正则匹配
        self.regex = regex