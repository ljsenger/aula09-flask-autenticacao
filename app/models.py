from app import db
from app import login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

@login.user_loader
def load_user(id):
    return Usuario.query.get(int(id))

class Usuario(UserMixin, db.Model):
    __tablename__='usuario'
    id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String(64), index=True, unique=True)
    email   = db.Column(db.String(120), index=True, unique=True)
    senha   = db.Column(db.String(128))
    endereco = db.Column(db.String(128))
    funcao_id = db.Column(db.Integer, db.ForeignKey('funcao.id'))
    
    
    def __repr__(self):
        return '<Usuario {}>'.format(self.usuario)  

    def set_senha(self, senha):
        self.senha = generate_password_hash(senha)

    def verifique_senha(self, senha):
        return check_password_hash(self.senha, senha)

class Funcao(db.Model):
    __tablename__='funcao'
    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(120), index=True, unique=True)
    usuario = db.relationship('Usuario', backref='funcao', lazy='dynamic')

    def __repr__(self):
        return '<Funcao {}>'.format(self.descricao)  

