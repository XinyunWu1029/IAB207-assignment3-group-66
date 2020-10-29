from flask import Blueprint,render_template, jsonify,request
from . import db
bp = Blueprint('main', __name__)
from flask_login import login_required,current_user,logout_user
import datetime
import os
from .models import Watch,WatchList,Cart,BidRecord,Reviews,User

@bp.route('/')
@bp.route('/index')
@bp.route('/home')
def index():
    username=''
    try:
        username=current_user.username
    except Exception as e:
        print(e)
        pass
    u1 = db.session.query(Watch.id,db.func.count(BidRecord.watchid),Watch.name,Watch.description,Watch.fileurl).outerjoin(BidRecord,Watch.id==BidRecord.watchid).filter(Watch.goline==True,Watch.status=='Bidding').group_by(BidRecord.watchid).paginate(1,4,False).items
    print(u1)
    u2 = db.session.query(Watch.id,db.func.count(BidRecord.watchid),Watch.name,Watch.description,Watch.fileurl).outerjoin(BidRecord,Watch.id==BidRecord.watchid).filter(Watch.goline==True,Watch.status=='Bidding').group_by(BidRecord.watchid).paginate(2,4,False).items
    return render_template('Home_Page.html',title='HomePage-watch auction store',subtitle='Luxury Watch Store',username=username,u1=u1,u2=u2)

@bp.route('/creation')
@login_required
def itemcreation():
    username=''
    try:
        username=current_user.username
    except Exception as e:
        print(e)
        pass
    return render_template('Item Creation.html',title='Watch detial page', subtitle='Listing Details',username=username))

@bp.route('/detial')
@login_required
def watchdetialpage():
    id=request.args.get('id')
    username=''
    try:
        username=current_user.username
    except Exception as e:
        print(e)
        pass
    if not id:
        u1 = db.session.query(Watch.id,db.func.count(BidRecord.watchid),Watch.name,Watch.description,Watch.fileurl).outerjoin(BidRecord,Watch.id==BidRecord.watchid).filter(Watch.goline==True,Watch.status=='Bidding').group_by(BidRecord.watchid).paginate(1,4,False).items
        print(u1)
        u2 = db.session.query(Watch.id,db.func.count(BidRecord.watchid),Watch.name,Watch.description,Watch.fileurl).outerjoin(BidRecord,Watch.id==BidRecord.watchid).filter(Watch.goline==True,Watch.status=='Bidding').group_by(BidRecord.watchid).paginate(2,4,False).items
        return render_template('Home_Page.html',title='HomePage-watch auction store',subtitle='Luxury Watch Store',username=username,u1=u1,u2=u2)
    
    detail=Watch.query.filter(Watch.id==id).first()
    comment=db.session.query(Reviews.id,Reviews.watchid,Reviews.userid,Reviews.comment,Reviews.createtime,User.username).join(User,User.id==Reviews.userid).filter(Reviews.watchid==id).order_by(Reviews.createtime.desc()).all()
    print(comment)
    return render_template('Watch detial page.html',title='Watch detail page',subtitle='Luxury Watch Store',username=username,detail=detail,comment=comment)


@bp.route('/list')
@login_required
def watchlist():
    username=''
    try:
        username=current_user.username
    except Exception as e:
        print(e)
        pass
    userid=current_user.get_id()
    # watchlist=WatchList.query.filter(WatchList.userid==userid).all()
    # print(watchlist)
    # u1 = Watch.query.filter().order_by(Watch.id.desc()).all()
    u1=db.session.query(Watch.id,Watch.name,Watch.description,Watch.fileurl,WatchList.userid).join(WatchList,Watch.id==WatchList.watchid).filter(WatchList.userid==userid).all()
    # print(u1)
    return render_template('Watchlist.html',title='Wantchlist',subtitle='Watchlist',username=username,datalist=u1)


@bp.route('/createwatch', methods=['POST'])
@login_required
def createwatch():
    result=''
    try:
        form=request.form
        name=form['name']
        categortid=form['categortid']
        brand=form['brand']
        size=form['size']
        price=form['price']
        condition=form['condition']
        quantity=form['quantity']
        goline=True if form['goline'] and 'Yes' in form['goline'] else False
        description=form['description']
        fileurl=form['fileurl']
        u2=Watch(categortid,name,brand,size,price,condition,quantity,goline,description,fileurl)
        u2.savebyadd()
        result='success'
        pass
    except Exception as e:
        result='fail'
        print(e)
        pass
    return jsonify(result)

@bp.route('/addwatchlist', methods=['POST'])
@login_required
def addWatchlist():
    result=''
    try:
        form=request.form
        id=form['id']
        userid=current_user.get_id()
        res=WatchList.query.filter(WatchList.watchid==id,WatchList.userid==userid).first()
        if not res is None:
            db.session.delete(res)
            db.session.commit()
        u2=WatchList(id,userid)
        u2.savebyadd()
        result='success'
        pass
    except Exception as e:
        result='fail'
        print(e)
        pass
    return jsonify(result)

@bp.route('/removewatchlist', methods=['POST'])
@login_required
def removeWatchlist():
    result=''
    try:
        form=request.form
        id=form['id']
        userid=current_user.get_id()
        res=WatchList.query.filter(WatchList.watchid==id,WatchList.userid==userid).first()
        if not res is None:
            db.session.delete(res)
            db.session.commit()
        result='success'
        pass
    except Exception as e:
        result='fail'
        print(e)
        pass
    return jsonify(result)

@bp.route('/addcart', methods=['POST'])
@login_required
def addCart():
    result=''
    try:
        form=request.form
        id=form['id']
        userid=current_user.get_id()
        res=Cart.query.filter(Cart.watchid==id,Cart.userid==userid).first()
        if not res is None:
            db.session.delete(res)
            db.session.commit()
        u2=Cart(id,userid)
        u2.savebyadd()
        result='success'
        pass
    except Exception as e:
        result='fail'
        print(e)
        pass
    return jsonify(result)

@bp.route('/bidwatch', methods=['POST'])
@login_required
def bidWatch():
    result=''
    try:
        form=request.form
        id=form['id']
        price=form['price']
        userid=current_user.get_id()
        res=BidRecord.query.filter(BidRecord.watchid==id,BidRecord.userid==userid).first()
        if not res is None:
            db.session.delete(res)
            db.session.commit()
        u2=BidRecord(id,userid,price)
        u2.savebyadd()
        result='success'
        pass
    except Exception as e:
        result='fail'
        print(e)
        pass
    return jsonify(result)

@bp.route('/addreviews', methods=['POST'])
@login_required
def addReviews():
    result=''
    try:
        form=request.form
        id=form['id']
        comment=form['comment']
        userid=current_user.get_id()
        u2=Reviews(id,userid,comment)
        u2.savebyadd()
        result='success'
        pass
    except Exception as e:
        result='fail'
        print(e)
        pass
    return jsonify(result)

@bp.route('/logout', methods=['POST'])
@login_required
def logout():
    result=''
    try:
        logout_user()
        result='success'
        pass
    except Exception as e:
        result='fail'
        print(e)
        pass
    return jsonify(result)

@bp.route('/upload', methods=['POST'])
def UpLoad():  # upload images
    filename=''
    try:
        ufile = request.files['file']
        if not allowed_file(ufile.filename):
            return jsonify(filename)
        format = "%Y%m%d%H%M%S"
        now = datetime.datetime.utcnow().strftime(format)
        filename = now + '_' + ufile.filename
        imgpath=os.path.join(os.getcwd()+'\\auction\\static\\datas', filename)
        ufile.save(imgpath)
        return jsonify(filename)
    except Exception as e:
        print(e)
        filename=''
        return jsonify(filename)


def allowed_file(filename):
    ALLOWED_EXTENSIONS=['jpg','png']
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@bp.route('/create_db')
def create_db():
    db.create_all()
    return "db create"

@bp.route("/drop_db")
def drop_db():
    db.drop_all()
    return "db drop"
