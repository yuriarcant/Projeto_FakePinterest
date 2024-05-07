#esse arquivo a gente vai crialo  apenas para fazer o banco de dados, mas depois que o branco de dados for criado basicamente ele pode ser excluido, estamos fazendo isso pois posteriormente vamos excluir o banco de dados e ai fica mais faci so rodar o codigo aqui pra crialo.

from fakepinterest import app, database
from fakepinterest.models import Usuario, Foto

with app.app_context():
    database.create_all()