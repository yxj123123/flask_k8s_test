from flask import Blueprint, render_template, jsonify, redirect, url_for, session,flash
from flask_login import current_user, logout_user, login_user, login_required
from exts import db
from flask_mail import Message
from flask_login import LoginManager
from flask import request
import datetime
import string
import random
#from models import EmailCaptchaModel
#from .forms import RegisterForm,LoginForm
from models import *
from werkzeug.security import generate_password_hash, check_password_hash

#blueprint是flask的子模块
#url_prefix 代表路由前缀
#cookie 中只适合少量的数据，一般用来存放登录授权的东西
#flask中的session，是经过加密后存储在cookie中的

bp=Blueprint("auth",__name__,url_prefix="/")
#定义时间格式
ISOTIMEFORMAT = '%Y-%m-%d %H:%M:%S'
#/grant/login
# @bp.route("/login")
# def login():
#     pass



@bp.route("/")
def index():
    return render_template("index.html")

@bp.route("/register",methods=['GET', 'POST'])
def register():
    if not current_user.is_anonymous:
        return redirect(url_for('auth.index'))
    if request.method == 'POST':
        userID = request.form.get('userID')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        if password1 != password2:
            flash('两次输入的密码不同')
            return redirect(url_for('auth.register'))
        staff = StaffModel.query.filter_by(id=userID).first()
        if staff is None:
            flash('员工号错误')
            return redirect(url_for('auth.register'))
        user = UserModel.query.filter_by(id=userID).first()
        if user is not None:
            flash('用户已注册')
            return redirect(url_for('auth.register'))

        user=UserModel(id=userID,password=password1)
        db.session.add(user)
        db.session.commit()
        flash('注册成功')
        return redirect(url_for('auth.index'))
    return render_template('register.html')

@bp.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("login.html")
    else:
        userID = request.form.get('userID')
        password = request.form.get('password')

        if not userID or not password:
            flash('请输入')
            return redirect(url_for('auth.login'))

        staff = StaffModel.query.filter_by(id=userID).first()
        user = UserModel.query.filter_by(id=userID).first()
        if user is None:
            flash('员工号错误')
            return redirect(url_for('auth.login'))
        if not user.password==password:
            flash('密码错误')
            return redirect(url_for('auth.login'))
        flash('登录成功')
        login_user(staff)
        return redirect(url_for('auth.index'))
"""
    商店管理
    商店列表
    商店的增删改查
"""
@bp.route("/storelist", methods=['GET', 'POST'])
def storelist():
    if request.method == 'POST':
        info = request.form.get('info')
        date = request.form.get('date')
        if info == 'storeid':
            stores = StoreModel.query.filter_by(id=date).first()
            if stores is None:
                flash('该商店不存在')
                return redirect(url_for('auth.sotrelist'))
            return render_template('storelist.html', stores=stores, info=info)
        if info == 'storename':
            stores = StoreModel.query.filter_by(storename=date).first()
            if stores is None:
                flash('该商店不存在')
                return redirect(url_for('auth.storelist'))
            return render_template('storelist.html', stores=stores, info=info)

    stores =StoreModel.query.all()
    return render_template('storelist.html', stores=stores, info=1)

#后端采用<int:storeid>语法接受前端发送的storeid信息
@bp.route('/store_delete/<int:storeid>',methods=['POST'])
@login_required  # 登录保护
def store_delete(storeid):
    staff =StaffModel.query.filter_by(staffworkplace=storeid).first()
    if staff is not None:
        flash('该商店内存在员工 无法删除')
        return redirect(url_for('auth.storelist'))
    storgestore=StorgeStoreModel.query.filter_by(storgestoreid=storeid).first()
    request=RequestModel.query.filter_by(requeststoreid=storeid).first()
    sale=SaleModel.query.filter_by(salestoreid=storeid).first()
    if (storgestore is not  None) or (request is not None) or (sale is not  None):
        flash('仍存在关于该商店的记录 无法删除')
        return redirect(url_for('auth.storelist'))
    store=StoreModel.query.get_or_404(storeid)
    db.session.delete(store)
    db.session.commit()
    flash('删除成功')
    return redirect(url_for('auth.storelist'))

@bp.route('/store_alter/<int:storeid>',methods=['GET','POST'])
@login_required
def store_alter(storeid):
    store= StoreModel.query.get_or_404(storeid)
    if request.method == 'POST':
        storename = request.form.get('storename')
        storeplace= request.form.get('storeplace')
        store.storename = storename
        store.storeplace = storeplace
        db.session.commit()
        flash('更新成功')
        return redirect(url_for('auth.storelist'))

    return render_template('store_alter.html', store=store)


@bp.route('/store_add', methods=['GET', 'POST'])
@login_required
def store_add():
    if request.method == 'POST':
        storeid= request.form.get('storeid')
        storename = request.form.get('storename')
        storeplace = request.form.get('storeplace')
        store=StoreModel.query.filter_by(id=storeid).first()
        print(store)
        if store is None:
            store = StoreModel(id=storeid,storename=storename,storeplace=storeplace)
            db.session.add(store)
            db.session.commit()
            flash('添加成功')
            return redirect(url_for('auth.storelist'))
        else:
            flash('该商店已存在')
            return redirect(url_for('auth.storelist'))
    return render_template('store_add.html')

"""
    员工管理
    员工列表
    增删改查
"""
@bp.route("/stafflist", methods=['GET', 'POST'])
def stafflist():
    if request.method == 'POST':
        #info中存放查询的类型
        #date中存放查询的依据
        info = request.form.get('info')
        date = request.form.get('date')
        if info == 'staffid':
            staffs = StaffModel.query.filter_by(id=date).first()
            if staffs is None:
                flash('该员工不存在')
                return redirect(url_for('auth.stafflist'))
            return render_template('stafflist.html', staffs=staffs, info=info)
        if info == 'staffname':
            staffs = StaffModel.query.filter_by(staffname=date).first()
            if staffs is None:
                flash('该员工不存在')
                return redirect(url_for('auth.stafflist'))
            return render_template('stafflist.html', staffs=staffs, info=info)

    staffs = StaffModel.query.all()
    return render_template('stafflist.html', staffs=staffs, info=1)

@bp.route('/staff_delete/<int:staffid>',methods=['POST'])
@login_required  # 登录保护
def staff_delete(staffid):
    staff =StaffModel.query.filter_by(id=staffid).first()
    user=UserModel.query.filter_by(id=staffid).first()
    if user is not None:
        db.session.delete(user)
        db.session.commit()
    db.session.delete(staff)
    db.session.commit()
    flash('删除成功')
    return redirect(url_for('auth.stafflist'))

@bp.route('/staff_alter/<int:staffid>',methods=['GET','POST'])
@login_required
def staff_alter(staffid):
    staff= StaffModel.query.get_or_404(staffid)
    stores = StoreModel.query.all()
    if request.method == 'POST':
        staffsalary = request.form.get('staffsalary')
        staffworkplace= request.form.get('staffworkplace')
        staff.staffsalary = staffsalary
        staff.staffworkplace = staffworkplace
        db.session.commit()
        flash('更新成功')
        return redirect(url_for('auth.stafflist'))

    return render_template('staff_alter.html', staff=staff,stores=stores)


@bp.route('/staff_add', methods=['GET', 'POST'])
@login_required
def staff_add():
    if request.method == 'POST':
        staffid= request.form.get('staffid')
        staffname = request.form.get('staffname')
        stafftype=request.form.get('stafftype')
        staffsex=request.form.get('staffsex')
        staffsalary=request.form.get('staffsalary')
        staffworkplace = request.form.get('staffworkplace')
        active=1
        staff=StaffModel.query.filter_by(id=staffid).first()
        if staff is None:
            staff = StaffModel(id=staffid,staffname=staffname,stafftype=stafftype,staffsex=staffsex,staffsalary=staffsalary,staffworkplace=staffworkplace,active=active)
            db.session.add(staff)
            db.session.commit()
            flash('添加成功')
            return redirect(url_for('auth.stafflist'))
        else:
            flash('该员工已存在')
            return redirect(url_for('auth.stafflist'))
    stores = StoreModel.query.all()
    return render_template('staff_add.html',stores=stores)

@bp.route("/storgelist", methods=['GET', 'POST'])
def storgelist():
    if request.method == 'POST':
        #info中存放查询的类型
        #date中存放查询的依据
        info = request.form.get('info')
        date = request.form.get('date')
        if info == 'storgeid':
            storges = StorgeModel.query.filter_by(id=date).first()
            if storges is None:
                flash('该商品不存在')
                return redirect(url_for('auth.storgelist'))
            return render_template('storgelist.html', storges=storges, info=info)
    storges = StorgeModel.query.all()
    return render_template('storgelist.html', storges=storges, info=1)

@bp.route('/storge_add', methods=['GET', 'POST'])
@login_required
def storge_add():
    if request.method == 'POST':
        storgeid= request.form.get('storgeid')
        storgename = request.form.get('storgename')
        storgeproduce = request.form.get('storgeproduce')
        storgevalue = request.form.get('storgevalue')
        storgenumber = request.form.get('storgenumber')
        storge=StorgeModel.query.filter_by(id=storgeid).first()
        if storge is None:
            storge = StorgeModel(id=storgeid,storgename=storgename,storgeproduce=storgeproduce,storgevalue=storgevalue,storgenumber=storgenumber)
            db.session.add(storge)
            db.session.commit()
            flash('添加成功')
            return redirect(url_for('auth.storgelist'))
        else:
            flash('该商品已存在')
            return redirect(url_for('auth.storgelist'))
    return render_template('storge_add.html')

@bp.route('/storge_add_1/<int:storgeid>',methods=['GET','POST'])
@login_required  # 登录保护
def storge_add_1(storgeid):
    if request.method == 'POST':
        storge=StorgeModel.query.get_or_404(storgeid)
        storgenumber=request.form.get('storgenumber')
        storge.storgenumber=storge.storgenumber+int(storgenumber)
        db.session.commit()
        flash('补货成功')
        return redirect(url_for('auth.storgelist'))

    return render_template('storge_add_1.html')

@bp.route('/storge_request/<int:storgeid>/<int:storeid>', methods=['GET', 'POST'])
@login_required
def storge_request(storgeid,storeid):
    if request.method == 'POST':
        storge = StorgeModel.query.filter_by(id=storgeid).first()
        storgenumber = request.form.get('storgenumber')
        if int(storgenumber)>storge.storgenumber:
            flash('申请数量请勿超过库存')
            return redirect(url_for('auth.storgelist'))
        requeststorgeid=storgeid
        requeststoreid=storeid
        requestnumber=int(storgenumber)
        requesttime=datetime.now().strftime(ISOTIMEFORMAT)
        requeststatus=0
        deliverstatus=0
        requeststorge = RequestModel(requeststorgeid=requeststorgeid,requeststoreid=requeststoreid,requestnumber=requestnumber,requesttime=requesttime,requeststatus=requeststatus,deliverstatus=deliverstatus)
        db.session.add(requeststorge)
        db.session.commit()
        flash('申请成功')
        return redirect(url_for('auth.storgelist'))
    storge = StorgeModel.query.filter_by(id=storgeid).first()
    return render_template('storge_request.html',storge=storge)

@bp.route('/storge_delete/<int:storgeid>',methods=['POST'])
@login_required  # 登录保护
def storge_delete(storgeid):
    storge=StorgeModel.query.get_or_404(storgeid)
    storgestore = StorgeStoreModel.query.filter_by(storgestoregoodid=storgeid).first()
    request = RequestModel.query.filter_by(requeststorgeid=storgeid).first()
    sale = SaleModel.query.filter_by(salestorgeid=storgeid).first()
    if (storgestore is not None) or (request is not None) or (sale is not None):
        flash('仍存在关于该商品的记录 无法删除')
        return redirect(url_for('auth.storgelist'))
    db.session.delete(storge)
    db.session.commit()
    flash('删除成功')
    return redirect(url_for('auth.storgelist'))
# 不加get方法会导致无法找到路由
@bp.route('/request_answer/<int:requestid>',methods=['GET','POST'])
@login_required  # 登录保护
def request_answer(requestid):
    if request.method == 'POST':
        request1 =RequestModel.query.filter_by(id=requestid).first()
        requestnumber=request.form.get("requestnumber")
        storgeid=request1.requeststorgeid
        storge =StorgeModel.query.filter_by(id=storgeid).first()
        if storge.storgenumber<int(requestnumber):
            flash("库存不足无法配送")
            return redirect(url_for('auth.requestlist'))
        elif request1.requestnumber<int(requestnumber):
            flash("配送数量请勿超出订单需求")
            return redirect(url_for('auth.requestlist'))
        storge.storgenumber=storge.storgenumber-int(requestnumber)
        request1.requestdealtime=datetime.now().strftime(ISOTIMEFORMAT)
        request1.requestdealnumber=int(requestnumber)
        request1.requeststatus=1
        db.session.commit()
        flash('配送成功')
        return redirect(url_for('auth.requestlist'))
    request1 = RequestModel.query.filter_by(id=requestid).first()
    storgeid = request1.requeststorgeid
    storge = StorgeModel.query.filter_by(id=storgeid).first()
    return render_template('request_deal.html',storge=storge)

@bp.route("/requestlist", methods=['GET', 'POST'])
def requestlist():
    if request.method == 'POST':
        #info中存放查询的类型
        #date中存放查询的依据
        info = request.form.get('info')
        date = request.form.get('date')
        if info == 'requestid':
            requests = RequestModel.query.filter_by(id=date).first()
            if requests is None:
                flash('该申请不存在')
                return redirect(url_for('auth.requestlist'))
            return render_template('requestlist.html', requests=requests, info=info)

    requests = RequestModel.query.all()
    return render_template('requestlist.html', requests=requests, info=1)

@bp.route('/request_back/<int:requestid>',methods=['POST'])
@login_required  # 登录保护
def request_back(requestid):
    request=RequestModel.query.get_or_404(requestid)
    db.session.delete(request)
    db.session.commit()
    flash('撤回成功')
    return redirect(url_for('auth.requestlist'))

@bp.route('/request_delete/<int:requestid>',methods=['POST'])
@login_required  # 登录保护
def request_delete(requestid):
    request=RequestModel.query.get_or_404(requestid)
    db.session.delete(request)
    db.session.commit()
    flash('删除成功')
    return redirect(url_for('auth.requestlist'))

@bp.route("/deliverlist", methods=['GET', 'POST'])
def deliverlist():
    if request.method == 'POST':
        #info中存放查询的类型
        #date中存放查询的依据
        info = request.form.get('info')
        date = request.form.get('date')
        if info == 'requestid':
            requests = RequestModel.query.filter_by(id=date).first()
            if requests is None:
                flash('该配送记录不存在')
                return redirect(url_for('auth.deliverlist'))
            return render_template('deliverlist.html', requests=requests, info=info)

    requests = RequestModel.query.all()
    return render_template('deliverlist.html', requests=requests, info=1)

@bp.route('/deliver_back/<int:requestid>',methods=['POST'])
@login_required  # 登录保护
def deliver_back(requestid):
    request=RequestModel.query.get_or_404(requestid)
    request.deliverstatus=2;
    request.deliverdealtime=datetime.now().strftime(ISOTIMEFORMAT);
    storgeid = request.requeststorgeid
    storge = StorgeModel.query.filter_by(id=storgeid).first()
    request.deliverdealtime=datetime.now().strftime(ISOTIMEFORMAT)
    storge.storgenumber=storge.storgenumber+int(request.requestdealnumber)
    db.session.commit()
    flash('退货成功')
    return redirect(url_for('auth.deliverlist'))

@bp.route('/deliver_get/<int:requestid>',methods=['GET','POST'])
@login_required  # 登录保护
def deliver_get(requestid):
    request=RequestModel.query.get_or_404(requestid)
    request.deliverstatus=1;
    storgeid = request.requeststorgeid
    storge = StorgeModel.query.filter_by(id=storgeid).first()
    request.deliverdealtime=datetime.now().strftime(ISOTIMEFORMAT)
    storgestore = StorgeStoreModel(storgestoregoodid=storge.id, storgestoreid=request.requeststoreid,
                                   storgestoretime=request.deliverdealtime, storgestorenumber=int(request.requestdealnumber))
    db.session.add(storgestore)
    db.session.commit()
    flash('收货成功')
    return redirect(url_for('auth.deliverlist'))

@bp.route("/storgestorelist", methods=['GET', 'POST'])
def storgestorelist():
    if request.method == 'POST':
        #info中存放查询的类型
        #date中存放查询的依据
        info = request.form.get('info')
        date = request.form.get('date')
        if info == 'storgestoreid':
            storgestores = StorgeStoreModel.query.filter_by(id=date).first()
            if storgestores is None:
                flash('该库存不存在')
                return redirect(url_for('auth.storgestorelist'))
            return render_template('storgestorelist.html',storgestores=storgestores, info=info)

    storgestores = StorgeStoreModel.query.all()
    return render_template('storgestorelist.html', storgestores=storgestores, info=1)

@bp.route('/storgestore_sale/<int:storgestoreid>',methods=['GET','POST'])
@login_required
def storgestore_sale(storgestoreid):
    if request.method == 'POST':
        storge = StorgeStoreModel.query.get_or_404(storgestoreid)
        storgenumber = request.form.get('storgestorenumber')
        storgevalue=request.form.get('storgestorevalue')
        if storge.storgestorenumber<int( storgenumber):
            flash("库存不足")
            return redirect(url_for('auth.storgestorelist'))
        storge.storgestorenumber=storge.storgestorenumber-int(storgenumber)
        sale = SaleModel(salestorgeid=storge.storgestoregoodid, salestoreid=storge.storgestoreid,
                         salenumber=int(storgenumber), saletime=datetime.now().strftime(ISOTIMEFORMAT),salevalue=storgevalue)
        if storge.storgestorenumber==0:
            db.session.add(sale)
            db.session.delete(storge)
            db.session.commit()
            flash('该批次货物已售空，删除记录')
            return redirect(url_for('auth.storgestorelist'))
        db.session.add(sale)
        db.session.commit()
        flash('出库成功')
        return redirect(url_for('auth.storgestorelist'))
    storge = StorgeStoreModel.query.filter_by(id=storgestoreid).first()
    goodid=storge.storgestoregoodid
    good=StorgeModel.query.filter_by(id=goodid).first()
    return render_template('storgestore_sale.html',storge=good)

@bp.route('/storgestore_delete/<int:storgestoreid>',methods=['POST'])
@login_required  # 登录保护
def storgestore_delete(storgestoreid):
    storgestore=StorgeStoreModel.query.get_or_404(storgestoreid)
    db.session.delete(storgestore)
    db.session.commit()
    flash('清理成功')
    return redirect(url_for('auth.storgestorelist'))

@bp.route("/salelist", methods=['GET', 'POST'])
def salelist():
    if request.method == 'POST':
        #info中存放查询的类型
        #date中存放查询的依据
        info = request.form.get('info')
        date = request.form.get('date')
        if info == 'saleid':
            sales = SaleModel.query.filter_by(id=date).first()
            if sales is None:
                flash('该出库记录不存在')
                return redirect(url_for('auth.salelist'))
            return render_template('salelist.html', sales=sales, info=info)

    sales = SaleModel.query.all()
    return render_template('salelist.html', sales=sales, info=1)

@bp.route('/sale_delete/<int:saleid>',methods=['POST'])
@login_required  # 登录保护
def sale_delete(saleid):
    sale=SaleModel.query.get_or_404(saleid)
    db.session.delete(sale)
    db.session.commit()
    flash('删除成功')
    return redirect(url_for('auth.salelist'))

@bp.route('/logout')
@login_required
def logout():  # 登出
    logout_user()
    flash('登出')
    return redirect(url_for('auth.index'))