;; A file that make site views by flask

(import [. [user]])
(import [flask [url_for render_template request make_response redirect flash ]])
(setv req request)
(setv mkresp make_response)

(import [jeefies [Content]])
(import [jeefies.flask_self [protect get_user gravator permission]])

(import os) (import hashlib)
(setv base (os.path.abspath (os.path.dirname __file__)))
(setv conpath (get (os.path.split base) 0)) (print conpath)

(setv con (Content conpath "user"))
