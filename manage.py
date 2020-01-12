# 使用python2需要加上以下行，使用中文
# coding:utf-8
from ihome_db import create_app, db
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

# 创建flask 的应用对象
app = create_app("develop")
manager = Manager(app)
Migrate(app, db)
manager.add_command("db", MigrateCommand)


if __name__ == "__main__":
    manager.run()



