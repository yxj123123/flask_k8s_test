from flask import Flask
from flask_security import SQLAlchemyUserDatastore, Security
import config
from exts import db
#from models import UserModel
from blueprints.auth import bp as auth_bp
from flask_login import LoginManager
from flask_migrate import Migrate
from flask import Flask,render_template
from flask import redirect
from flask import url_for
from flask import request
#before_request/before_first_rqquest/after_request
#pip freeze 导出该项目使用的所有依赖包
app= Flask(__name__)
#绑定配置文件
app.config.from_object(config)
#可以使db不在创建时就进行绑定
db.init_app(app)
#通过migrate可以动态更改数据库中表的列
migrate=Migrate(app,db)
# 若要使用cureent_user则需要先采用login_manager对app进行初始化
app.register_blueprint(auth_bp)

login_manager = LoginManager(app)
#login_manager.init_app(app)
security = Security(app)

@login_manager.user_loader
def load_user(user_id):  # 创建用户加载回调函数，接受用户ID作为参数
    from models import StaffModel
    user = StaffModel.query.get(user_id)  # 用ID作为user模型的主键查询对应的用户
    print(user)
    return user  # 返回用户对象

if __name__=="__main__":
    app.run(debug=1,port=5003)
