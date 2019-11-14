from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo


class LoginForm(FlaskForm):
	usuario = StringField(u'Nome de usuário', validators=[DataRequired()])
	senha = PasswordField(u'Senha', validators=[DataRequired(message="Campo não deve ser vazio")])
	lembre_me = BooleanField(u'Lembre-me')
	submit = SubmitField(u'Entrar')

class RegistroForm(FlaskForm):
	usuario = StringField(u'Nome de usuário', validators=[DataRequired()])
	senha = PasswordField(u'Senha', validators=[DataRequired(message="Campo não deve ser vazio"), EqualTo('confirma', message='Senhas devem ser iguais')])
	confirma = PasswordField(u'Confirme a senha', validators=[DataRequired(message="Campo não deve ser vazio")])
	email = StringField("Email", validators=[DataRequired(), Email()])
	submit = SubmitField(u'Registre-se!')