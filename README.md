# ihome

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
## 模型类和数据库创建
- 基本数据表的分析（start uml 保存文件）
- 
