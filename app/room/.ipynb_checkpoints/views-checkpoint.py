import os
conpath = os.path.split(os.path.dirname(__file__))[0]
txtpath = os.path.join(os.path.dirname(__file__), 'contents')

from flask import url_for, Flask, render_template, redirect, session, flash, request, make_response
req = request; mkresp = make_response
from . import chat
from jeefies import Content, Hashsec, strtime, Hexsec
from jeefies.flask_self import get_user, protect, render, Chatting, Context
from .forms import ChatForm, RegForm, NameForm

def errors():
    flash("You must be logined")
    #print('not passed')
    return redirect(url_for("main.index"))


@chat.before_request
@protect(errors,conpath)
def no_use_function():
    #print('passed')
    pass

@chat.route('/')
def index():
    con = Content(conpath, 'room')
    #con = Context('room')
    #print('room call')
    rooms = con.allitem() # (roomname, [url, intruductions])
    #print(rooms)
    return render('chat/index.html', rooms = rooms)

tf = '%b %d, %A, %H.%M'

@chat.route('/<token>', methods=['GET', 'POST'])
def roomin(token):
    '''
    a function, site to redirect the page to the paged site
    '''
    return redirect(url_for('.paged', token=token, page=1))
    name = Hashsec.decrypt(Hexsec.decrypt(token))
    con = Content(conpath, 'room')
    form = ChatForm()
    if not con.has(name):
        flash('No such room')
        return redirect(url_for('.index'))
    chat = Chatting(name, txtpath)
    #print('chat init')
    if form.validate_on_submit():
        chat.add(get_user(), form.con.data, strtime.now(tf))
        return redirect(url_for('.roomin', token = token))
    con = chat.page(1) #  each is like [sayer, saying, saytime]
    #print('con init'); print(con)
    leng = range(len(chat)//50 + 1)
    return render('chat/chat.html', form=form, cons = con, leng=leng, token=token, roomname=name)

@chat.route('/<token>/<int:page>', methods=['GET', 'POST'])
def paged(token, page):
    #print(token)
    name = Hashsec.decrypt(Hexsec.decrypt(token))
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
    leng = len(chat)//50+1
    #print(leng)
    return render('chat/chat.html',form=form, cons=con, leng = range(leng), token=token, roomname = name)


@chat.route('/<token>/clean', methods=['GET', 'POST'])
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
        print(url)
        intro = form.intro.data
        con.add(name, [url, intro])
        flash('room created')
        return redirect(url_for('.index'))
    return render('chat/regist.html', form = form)

@chat.route('/delete', methods=['GET', 'POST'])
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
