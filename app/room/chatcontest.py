import os
import sys

from faker import Faker
from jeefies import strtime, Content, Hexsec, Hashsec
from jeefies.flask_self import Chatting

base = os.path.dirname(os.path.abspath(__file__))
txtpath = os.path.join(base, 'contents')
conpath = os.path.split(base)[0]
print(conpath, txtpath, base)


if __name__ == '__main__':
    con = Content(conpath, 'room')
    con.add('example', [Hexsec.encrypt(Hashsec.encrypt(
        'example')), 'This is a test room made by faker\nSo every thing in it is not true just a example', ''])

ft = '%b %d, %A, %H:%M'
chat = Chatting('example', txtpath)


def say():
    fk = Faker()
    return fk.user_name(), fk.text(), strtime.now(ft)


if __name__ == '__main__':
    chat.reset()
    chat.add('t', 'date one', strtime.now())
    from faker import Faker
    fk = Faker()
    sys.argv.append('')
    try:
        num = int(sys.argv[-1])
    except:
        num = 140
    for a in range(140):
        arg = [fk.user_name(), fk.text()]
        chat.add(*arg, strtime.now(ft))
