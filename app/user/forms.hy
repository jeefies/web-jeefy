;; Flask forms based on hy Lisp

(import [flask_wtf [FlaskForm]]) (import [wtforms [StringField SubmitField BooleanField PasswordField TextAreaField]])
(import [wtforms.validators [DataRequired Email EqualTo Length]])

(defclass EditForm [FlaskForm]
	(setv name (StringField "Account Name"
		    :validators
		     [(DataRequired) (Length 3 10 :message "name must longer than 3 and shorter than 10 leters")]))
	(setv realname (StringField "Real Name"))
	(setv country (StringField))
	(setv description (TextAreaField "Decribe your self with some sentences"))
	(setv submit (SubmitField "Submit"))
)

(defclass PasswdForm [FlaskForm]
	(setv passwd (PasswordField "Your passwd"))
	(setv submit (SubmitField "Submit"))
)

(defclass StrForm [FlaskForm]
	(setv title "String")
	(setv data (StringField title ))
)
