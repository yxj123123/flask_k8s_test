SECRET_KEY = "asdfasdfjasdfjasd;lf"
#数据库配置
HOSTNAME = '127.0.0.1'
PORT     = '3306'
DATABASE = 'database_experiment'
USERNAME = 'root'
PASSWORD = 'root'
DB_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(USERNAME,PASSWORD,HOSTNAME,PORT,DATABASE)
SQLALCHEMY_DATABASE_URI = DB_URI