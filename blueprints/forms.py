# import wtforms
# from wtforms.validators import Email, Length, EqualTo, InputRequired
# from exts import db
#
#
# # Form：主要就是用来验证前端提交的数据是否符合要求
# class RegisterForm(wtforms.Form):
#     #用于验证前端给出用户名长度，最少为3位,最大为20位
#     username = wtforms.StringField(validators=[Length(min=3, max=20, message="用户编号格式错误！")])
#     password = wtforms.StringField()
#     #用于验证两次输入密码是否相等
#     password_confirm = wtforms.StringField(validators=[EqualTo("password", message="两次密码不一致！")])
#
#     # 自定义验证：
#     # 1. 邮箱是否已经被注册
#     def validate_username(self, field):
#         username = field.data
#         user = AdminiModel.query.filter_by(administratorsid=username).first()
#         if user and username!="":
#             raise wtforms.ValidationError(message="该管理员已存在！")
#
#
#
# class LoginForm(wtforms.Form):
#     username = wtforms.StringField()
#     password = wtforms.StringField()
#     type = wtforms.StringField()
#
#
# class QuestionForm(wtforms.Form):
#     title = wtforms.StringField(validators=[Length(min=3, max=100, message="标题格式错误！")])
#     content = wtforms.StringField(validators=[Length(min=3,message="内容格式错误！")])
#
#
# class AnswerForm(wtforms.Form):
#     content = wtforms.StringField(validators=[Length(min=3, message="内容格式错误！")])
#     question_id = wtforms.IntegerField(validators=[InputRequired(message="必须要传入问题id！")])