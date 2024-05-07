#Criar os formularios do nosso site
#permite criar a estrutura para nossos formularios
from flask_wtf import FlaskForm
#permite importar os campos da estrutura (texto, numero, data)
from wtforms import StringField, PasswordField, SubmitField , FileField
#validadores para ver se o campo ta preenchido, se um esta igual o outro no caso de senhas etc. (preencher campo, campo de email, verifica se um capo é igual outro, tamanho e error)
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from fakepinterest.models import Usuario


class FormLogin(FlaskForm):
    email= StringField('E-mail', validators=[DataRequired(), Email()])
    senha=PasswordField('Senha', validators=[DataRequired()])
    botao_confirmacao=SubmitField('Fazer Login')

    def validate_email(self, email):
        usuario = Usuario.query.filter_by(email=email.data).first() # esse usuario vem la do arquivo models, o primeiro email é o campo email que vem la dos usuarios, e o segundo e variavel email da função, que é a que foi prenchida no formulario.
        if not usuario:
            raise ValidationError('Usuario inexistente, crie ua conta!!')
    


class FormCriarConta(FlaskForm):
    email=StringField('E-mail', validators=[DataRequired(), Email()])
    username=StringField('Nome Usuario', validators=[DataRequired()])
    senha= PasswordField('Senha', validators=[DataRequired(), Length(6,20)])
    confirmacao_senha=PasswordField('Confirmção Senha', validators=[DataRequired(), EqualTo("senha")])
    botao_confirmacao=SubmitField('Criar Conta')


    #No arquivo models, no campo de email definimos que o email seria um campo unico, entao teremos que tratar aqui para ficar valido. aqui essa função deve começar com o validate_ + nome da variavel que voce quer validar, vamos filtrar a base de dados buscando o email e se ja tiver o email vai nos mostra um erro e nao deixara criar a conta com o msm email
    def validate_email(self, email):
        usuario = Usuario.query.filter_by(email=email.data).first() # esse usuario vem la do arquivo models, o primeiro email é o campo email que vem la dos usuarios, e o segundo e variavel email da função, que é a que foi prenchida no formulario.
        if usuario:
            raise ValidationError('E-mail ja cadastrado, faça login para continuar')


class FormFoto(FlaskForm):
    foto= FileField('foto', validators=[DataRequired()])
    botao_confirmacao = SubmitField('enviar')