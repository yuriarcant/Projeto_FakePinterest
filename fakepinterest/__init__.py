from flask import Flask
# criando branco de dados
from flask_sqlalchemy import SQLAlchemy
# flask bcrypt é quem vai fazer a criptografia da senha do usuario
from flask_bcrypt import Bcrypt
# flask login é quem vai gerenciar a nossa senha
from flask_login import LoginManager
import os


app = Flask(__name__)  # criando site
# configurar essa variavel
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('BANCO_DADOS_URL')
# fazendo uma senha secreta para a segurança do app
app.config['SECRET_KEY'] = "a3190c71717b80582c2b580d8bc02528"
# para armazenar a fotos na pasta fotos_posts
app.config['UPLOAD_FOLDER'] = 'static/fotos_posts'

# criando banco de dados
database = SQLAlchemy(app)
# criar o bcrypt para fazer a criptografia
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

# para caso o usuario não esteja logado ele vai ser direcionado para alguma pagina
login_manager.login_view = 'homepage'

from fakepinterest import routes # Essa linha deve ficar aqui mesmo para poder ser executada



