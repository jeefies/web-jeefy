;; A file that make site views by flask

(import [. [user]])
(import [.forms [EditForm]])
(import [..sdmail [send-email]])
(import [flask [url_for render_template request make_response redirect flash ]])
(setv req request)
(setv mkresp make_response)

(import [jeefies [Content]])
(import [jeefies.flask_self [protect get_user gravatar permission User emailmsg]])

(import os) (import hashlib)
(setv base (os.path.abspath (os.path.dirname __file__)))
(setv conpath (get (os.path.split base) 0)) (print conpath)

(setv con (Content conpath "user"))
(setv ucon (User conpath))

(defn not-logined []
	(flash "You must be logined to see your account")
	(return (redirect (urk_for "main.login")))
)

#@((user.route "/u" :methods ["GET" "POST"])
#@((protect not-logined conpath)
(defn acc []
	"Edit yourself's profile"
	(setv form (EditForm) user (ucon.get (get_user)))
	(if* (form.validate_on_submit)
		(do (setv user.name form.name.data
			  user.full-name form.realname.data
			  user.pl form.country.data
			  user.des form.description.data
		    )
		(ucon.add-user user)
		(flash "You've change your account info")
		(send-email (emailmsg user.email "Account Changing" "email/chgacc" :name user.name :user user))
		(return (redirect (url_for ".acc")))
		)
	)
	(setv 	form.name.data user.name
		form.realname.data user.full-name
		form.country.data user.pl
		form.description.data user.des
	)
	(return (render_template "user/change_account.html" :form form :img user.gravatar))
)))
