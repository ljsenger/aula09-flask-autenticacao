from flask import Flask, render_template, request, json, url_for, redirect, make_response, flash, session
from config import Config
from app.forms import LoginForm
from app.forms import RegistroForm
from app.models import Usuario
from app import app
from app import db
from flask_login import current_user, login_user, logout_user, login_required

modelos = { "0":  {"nome": "pegasus", "preco": 500, "promocao": False},
            "1":  {"nome": "vintage", "preco": 1500, "promocao": False},
            "2":  {"nome": "sport",   "preco": 1500, "promocao": True},
            "3":  {"nome": "eco",     "preco": 759, "promocao": True}
}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/registro", methods=["GET", "POST"])
def registro():
    form = RegistroForm()
   # if request.method=='GET':
   #     return render_template("registro.html", form=form)
    if request.method != 'GET' and form.validate_on_submit():
        usuario = form.usuario.data
        senha = form.senha.data
        email = form.email.data
        existeU = Usuario.query.filter_by(usuario=usuario).first()
        existeEmail = Usuario.query.filter_by(email=email).first()
        if existeU == None and existeEmail == None:
            novoUsuario = Usuario(usuario=usuario, email=email)
            novoUsuario.set_senha(senha)
            db.session.add(novoUsuario)
            db.session.commit()
            flash("Usuario registrado com sucesso")
            return redirect(url_for('login'))
        else:
            flash("Nome de usuário ou email já registrado.")
    return render_template("registro.html", form=form)

        
@app.route("/user/<name>")
def user(name):
    return render_template("index.html", name=name, u=u)

@app.route("/modelos")
def produtos():
    return render_template("produtos.html", m=modelos)

@app.route("/promocoes")
def promocoes():
    return render_template("promocoes.html", m=modelos)    

@app.route('/favicon.ico')
def favicon():
    return redirect(url_for('static', filename='favicon.ico'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
   
    form = LoginForm()

    if form.validate_on_submit():
        flash('Requisição de login para  {}, lembre-me={}'.format(form.usuario.data, form.lembre_me.data))
        usuario = Usuario.query.filter_by(usuario=form.usuario.data).first()
        if usuario is None or not usuario.verifique_senha(form.senha.data):
            flash('Usuario ou senha invalida.')
            return redirect(url_for('login'))

        login_user(usuario, remember=form.lembre_me.data)
        
        return redirect(url_for('index'))

    return render_template('login.html', title='Entrar', form=form)
@login_required
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

