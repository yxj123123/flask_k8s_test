# 这个文件存在的意义是为了解决循环引用问题
# 1.flask db init：这步只需要执行一次
# 2.flask db migrate：识别ORM模型的改变，生成迁移脚步
# 3.flask db upgrade：运行迁移脚本

from flask_sqlalchemy import SQLAlchemy
db=SQLAlchemy()