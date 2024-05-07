#Criar as rotas do nosso site (links)

#o render templates  vai rodar um template, ele vai basicamente procurar uma pasta templates e vai rodar isso ao se codigo.

# url_for vai direcionar o link, atras do nome da função criada para aquela pagina, nao pelo rota '/' , '/perfil/<usuario> e etc>
from flask import render_template, url_for, redirect
from fakepinterest import app, database, bcrypt
#para fazer com que apenas usuarios logados acessem alguma pagina
from flask_login import login_required, login_user, logout_user, current_user
#importando as classes para criar os formularios
from fakepinterest.forms import FormLogin, FormCriarConta, FormFoto
from fakepinterest.models import Usuario, Foto
#vamos usar apra mudar o nome do arquivo pra que nao tenha problema de ter caracteres especiais
from werkzeug.utils import secure_filename
import os

@app.route('/', methods=["GET", "POST"]) #criando a rota do nosso site
def homepage():
    formlogin = FormLogin()
    #aqui estamos verificando o sistema de login, entao vamos encontrar o usuario no banco de dados pra ele fazer login, verificar se ja e cadastrado.
    if formlogin.validate_on_submit():
        usuario= Usuario.query.filter_by(email=formlogin.email.data).first()
        #dps vamos verificar se a senha ta certa ou não, pra isso precisamos da senha criptografada e dps a que ele colocou no campo.
        if usuario and bcrypt.check_password_hash(usuario.senha, formlogin.senha.data):
            login_user(usuario)
            return redirect(url_for('perfil', id_usuario= usuario.id))
    return render_template('homepage.html', form=formlogin)


@app.route('/criarconta', methods=["GET", "POST"])
def criarconta():
    formcriarconta= FormCriarConta()
    if formcriarconta.validate_on_submit(): #verifica se cliclou no botao e se ta tudo preenchido
        senha= bcrypt.generate_password_hash(formcriarconta.senha.data)
        usuario = Usuario(username=formcriarconta.username.data, senha=senha, email=formcriarconta.email.data)

        #agora temos q armazernar esse usuario criado acima no banco de dados
        database.session.add(usuario)
        database.session.commit()
        login_user(usuario, remember= True)

        #redirecionar para qual home
        return redirect(url_for('perfil', id_usuario= usuario.id))
    return render_template('criarconta.html', form=formcriarconta)


@app.route('/perfil/<id_usuario>', methods=["GET", "POST"])
@login_required
def perfil(id_usuario):
    
    #aqui o usuario ta vendo o perfil  dele, current_user verifica quem ta logado no moenteo
    if int(id_usuario) == int(current_user.id):
        formfoto = FormFoto()
        if formfoto.validate_on_submit():
            arquivo = formfoto.foto.data
            nome_seguro = secure_filename(arquivo.filename)
            #salvar arquivo na pasta fotopost, caminho = caminho do arquivo / onde vai ficar as fotos, app do init / nome da foto
            caminho= os.path.join(os.path.abspath(os.path.dirname(__file__)) , app.config['UPLOAD_FOLDER'] ,nome_seguro)
            arquivo.save(caminho)
            #registrar esse arquivo no baco de dados(colocar nome do arquivo no banco)
            foto = Foto(imagem=nome_seguro, id_usuario=current_user.id)
            database.session.add(foto)
            database.session.commit()
        return render_template('perfil.html',  usuario=current_user, form= formfoto)
    #aqui vendo perfil de outro
    else:
        usuario= Usuario.query.get(int(id_usuario))
        return render_template('perfil.html',  usuario=usuario, form= None)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('homepage'))

@app.route('/feed')
@login_required
def feed():
    fotos= Foto.query.order_by(Foto.data_criacao).all() #vai fazer uma busca e ordenar as fotos pela data de criação
    return render_template('feed.html', fotos= fotos)