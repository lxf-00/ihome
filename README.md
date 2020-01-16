# ihome（前后端分离）

Renting house on mobile phone project based on flask 

## 创建项目工程
- 创建项目：ihome文件
- 创建启动文件, 通过此文件启动整体项目： manage.py 
- 逻辑整体简单实现：
    - 导入Flask(from flask import Flask);
    - 创建Flask应用对象（app = Flask(__name__)); 
    - 创建Config类包含相关配置信息：
        - DEBUG;
        - SECRET_KEY; 
        - Redis参数配置;
        - 数据库的配置(SQLALCHEMY/mysql+pymysql); 
        - flask_seesion配置；
        - csrf 防护扩展（flask_wtf);
    - 导入到app.config.from_object(Config);
    - 定义视图函数，app.route("")进行装饰;
    - 项目启动： app.run() ( if __name__ == "__main__");
- 项目工程的拆分整理： 
    - 新建config.py保存配置类信息;区分开发环境和线上环境；
    - 创建工厂函数：ceate_app()，根据输入develop进入开发环境，product进入线上环境；
    - 创建新的包：ihome_db 管理所有项目的逻辑；
    - 进行相应的移动到ihome_db,使得manage.py 为最简单的启动文件：
        - create_app --->;
        - db = SQLAlchemy() --->(先创建对象，在通过init_app()进行绑定)；
        - redis;
        - 蓝图和相应的包创建；
        - 数据库的迁移；
## 模型类，数据库创建与迁移
- 基本数据表的分析（start uml 保存文件）
- python manage.py db init(首次运行)； python manage.py db migrate -m "说明"（迁移）； python manage.py upgrade(升级)；
- models 数据库的完善;

## 提供静态文件
- 使用flask 提供静态文件；
- 新建蓝图--> 自定义正则转换器(BaseConverter,注册，使用)；

## CSRF 防护: 静态路由中添加生成csrf_token
- flask_wtf.csrf.generate_csrf(),生成一个csrf_token 的值；
- 设置cookies(make_response)
- 返回response

## 图片验证码
- 后端接口的实现(接口文档，RESTful)
- 前段功能的实现

## 短信验证码
- 