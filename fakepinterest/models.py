#criar a estrutura do banco de dados 

#para criar as tabelas  do banco de dados, para isso vamos criar as classe que tera como parametro o database.model o que significa que nosso database(banco de dados)conseguirar entender.
from fakepinterest import database, login_manager
from datetime import datetime  # Retirei a importação do UTC
#diz qual a classe vai gerenciar a estrutura de login
from flask_login import UserMixin

#toda vez que criar um sitema de login essa class é obrigatoria
@login_manager.user_loader
def load_usuario(id_usuario):
    return Usuario.query.get(int(id_usuario)) #buscando informação do banco de dados

class Usuario(database.Model, UserMixin):
    id = database.Column(database.Integer, primary_key= True)
    username = database.Column(database.String, nullable= False)
    email = database.Column(database.String, nullable= False, unique= True)
    senha = database.Column(database.String, nullable= False)
    fotos = database.relationship('Foto', backref = 'usuario', lazy=True)

class Foto(database.Model):
    id = database.Column(database.Integer, primary_key= True)
    imagem = database.Column(database.String, default='default.png')
    data_criacao =  database.Column(database.DateTime, nullable= False , default= datetime.utcnow()) # Alterei essa linha
    id_usuario =  database.Column(database.Integer, database.ForeignKey('usuario.id'), nullable=False,)