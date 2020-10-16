import os
conpath = os.path.split(os.path.dirname(__file__))[0]
txtpath = os.path.join(os.path.dirname(__file__), 'contents')

from flask import url_for, Flask, render_template, redirect, session, flash, request, make_response
req = request; mkresp = make_response
from . import chat
from jeefies import Content, Hashsec, strtime, Hexsec
from jeefies.flask_self import get_user, protect, Chatting, permission, cookie_req
from .forms import ChatForm, RegForm, NameForm, PasswdForm

def errors():
    flash("You must be logined")
    #print('not passed')
    return redirect(url_for("main.index"))


@chat.before_request
@protect(errors,conpath)
def no_use_function():
    #print('passed')
    print(get_user())
    pass

def render(filename, **kwargs):
    rooms = []
    con = Content(conpath, 'room')
    for c in req.cookies:
        if req.cookies.get(c) == 'in':
            rooms.append(con.get(Hashsec.decrypt(Hexsec.decrypt(c))))
    while None in rooms:
        rooms.pop(rooms.index(None))
    kwargs['loginroom'] = rooms
    return render_template(filename, **kwargs)

@chat.route('/')
def index():
    con = Content(conpath, 'room')
    rooms = con.allitem() # (roomname, [url, intruductions, passwd])
    return render('chat/index.html', rooms = rooms)

tf = '%b %d, %A, %H.%M'

@chat.route('/<token>', methods=['GET', 'POST'])
def roomin(token):
    '''
    a function, site to redirect the page to the paged site
    '''
    con = Content(conpath, 'room')
    try:
        room = con.get(Hashsec.decrypt(Hexsec.decrypt(token)))
    except:
        return roomerror()
    if req.cookies.get(token) == get_uesr() + 'in':
        pass
    elif room is None:
        flash('site error, url wrong')
        return redirect('.index')
    elif room[1][2]:
        form = PasswdForm()
        if form.validate_on_submit():
            passwd = form.passwd.data
            if not passwd == room[1][2]:
                flash('Passwd wrong')
                return redirect(url_for('.roomin', token=token))
        else:
            return render('chat/roomin.html', form=form)
    resp = mkresp(redirect(url_for('.paged', token=token, page=1)))
    resp.set_cookie(token, get_user() + 'in')
    return resp

def cookerror():
    flash('Please giet in from the index page')
    return redirect(url_for('.index'))

def roomerror():
    flash('url(website) is not validate')
    return redirect(url_for('.index'))

@chat.route('/<token>/<int:page>', methods=['GET', 'POST'])
@cookie_req(('token', 'in'), cookerror)
def paged(token, page):
    #print(token)
    try:name = Hashsec.decrypt(Hexsec.decrypt(token))
    except:return roomerror()
    con = Content(conpath, 'room')
    form = ChatForm()
    
    if not con.has(name):
        flash('No such room')
        return redirect(url_for('.index'))
    
    chat = Chatting(name, txtpath)
    if form.validate_on_submit():
        chat.add(get_user(), form.con.data, strtime.now(tf))
        return redirect(url_for('.paged', page=page, token=token))
    
    con = chat.page(page) # each is like [sayer, saying, saytime]
    leng = len(chat)//50+1 # pages num
    return render('chat/chat.html',form=form, cons=con, leng = range(leng), token=token, roomname = name)


def perror():
    return render('chat/perm.html')

@chat.route('/<token>/clean', methods=['GET', 'POST'])
@permission(16, perror, conpath)
def clean_datas(token):
    name = Hashsec.decrypt(Hexsec.decrypt(token))
    chat = Chatting(name, txtpath)
    chat.reset()
    return '<h1>RESET FINISH, ALL CLAEN</h1>'

@chat.route('/regist', methods=['GET', 'POST'])
def regist():
    form = RegForm()
    con = Content(conpath, 'room')
    if form.validate_on_submit():
        name = form.name.data
        if con.has(name):
            flash('Room exists, please change a name and try again')
            return redirect(url_for('.regist'))
        url = Hexsec.encrypt(Hashsec.encrypt(name))
        intro = form.intro.data
        passwd = form.passwd.data
        if passwd:
            con.add(name, [url, intro, passwd])
        else:
            con.add(name, [url, intro, ''])
        flash('room created')
        return redirect(url_for('.index'))
    return render('chat/regist.html', form = form)

@chat.route('/delete', methods=['GET', 'POST'])
@permission(16, perror, conpath)
def delroom():
    form = NameForm()
    con = Content(conpath, 'room')
    rooms = con.allname()
    if form.validate_on_submit():
        roomname = form.name.data
        chat = Chatting(roomname, txtpath)
        con.rm(roomname)
        chat.reset()
        return redirect(url_for('.delroom'))
    return render('chat/del.html', form=form, rooms = rooms)
