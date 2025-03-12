"""
Este módulo contém testes para as operações relacionadas a classe modelo `Usuario`.

Os testes verificam as operações básicas de CRUD (Create, Read, Update, Delete) para o modelo `Usuario`,
incluindo cadastro, listagem, busca, atualização e remoção de usuários no banco de dados.
"""

from app.models import Usuario
from app.extensions import db
from app.utils.usuario_helpers import gerar_hashing, checar_senha
from app.utils.date_helpers import string_para_data, data_para_string


def test_cadastrar_usuario(app):
    """Testa o cadastro de um usuário no banco de dados.

    Este teste verifica se um usuário pode ser cadastrado corretamente no banco de dados
    e se os dados do usuário cadastrada estão corretos.

    Args:
        app (Flask): Aplicação Flask para acessar o contexto da aplicação.
    """
    with app.app_context():
        usuario = Usuario(cpf="12345678901", nome="John Cena", email="jcena@hotmail.com", senha=gerar_hashing("bocaAberta123"), telefone="79 9 9988-7766", endereco="Rua das Flores, N° 124, Centro, Carira-Sergipe", horario_de_trabalho="Seg-Sex,13h-17h", data_de_nascimento=string_para_data("1990-04-02"), tipo="p", formacao="Licenciatura em Matemática" ,escolaridade=None, habilidades=None)
        db.session.add(usuario)
        db.session.commit()

        usuario_adicionado = db.session.get(Usuario, "12345678901")
        assert usuario_adicionado is not None
        assert usuario_adicionado.cpf == "12345678901"
        assert usuario_adicionado.nome == "John Cena"
        assert usuario_adicionado.email == "jcena@hotmail.com"
        assert checar_senha("bocaAberta123", usuario_adicionado.senha)
        assert usuario_adicionado.endereco == "Rua das Flores, N° 124, Centro, Carira-Sergipe"
        assert usuario_adicionado.horario_de_trabalho == "Seg-Sex,13h-17h"
        assert data_para_string(usuario_adicionado.data_de_nascimento) == "1990-04-02"
        assert usuario_adicionado.tipo == "p"
        assert usuario_adicionado.formacao == "Licenciatura em Matemática"
        assert usuario_adicionado.escolaridade == None
        assert usuario_adicionado.habilidades == None


def test_listar_usuarios(app):
    """Testa a listagem de todos os usuários cadastradas no banco de dados.

    Este teste verifica se a listagem de usuários retorna corretamente todas os usuários
    cadastradas e se os dados do primeiro usuário na lista estão corretos.

    Args:
        app (Flask): Aplicação Flask para acessar o contexto da aplicação.
    """
    with app.app_context():
        usuario = Usuario(cpf="12345678901", nome="John Cena", email="jcena@hotmail.com", senha=gerar_hashing("bocaAberta123"), telefone="79 9 9988-7766", endereco="Rua das Flores, N° 124, Centro, Carira-Sergipe", horario_de_trabalho="Seg-Sex,13h-17h", data_de_nascimento=string_para_data("1990-04-02"), tipo="p", formacao="Licenciatura em Matemática" ,escolaridade=None, habilidades=None)
        db.session.add(usuario)
        db.session.commit()

        usuarios = Usuario.query.all()
        assert usuarios[0] is not None
        assert usuarios[0].cpf == "12345678901"
        assert usuarios[0].nome == "John Cena"
        assert usuarios[0].email == "jcena@hotmail.com"
        assert checar_senha("bocaAberta123", usuarios[0].senha)
        assert usuarios[0].telefone == "79 9 9988-7766"
        assert usuarios[0].endereco == "Rua das Flores, N° 124, Centro, Carira-Sergipe"
        assert usuarios[0].horario_de_trabalho == "Seg-Sex,13h-17h"
        assert data_para_string(usuarios[0].data_de_nascimento) == "1990-04-02"
        assert usuarios[0].tipo == "p"
        assert usuarios[0].formacao == "Licenciatura em Matemática"
        assert usuarios[0].escolaridade == None
        assert usuarios[0].habilidades == None

def test_buscar_usuarios(app):
    """Testa a listagem de todos os usuários cadastradas no banco de dados.

    Este teste verifica se a listagem de usuários retorna corretamente todas os usuários
    cadastradas e se os dados do primeiro usuário na lista estão corretos.

    Args:
        app (Flask): Aplicação Flask para acessar o contexto da aplicação.
    """
    with app.app_context():
        usuario = Usuario(cpf="12345678901", nome="John Cena", email="jcena@hotmail.com", senha=gerar_hashing("bocaAberta123"), telefone="79 9 9988-7766", endereco="Rua das Flores, N° 124, Centro, Carira-Sergipe", horario_de_trabalho="Seg-Sex,13h-17h", data_de_nascimento=string_para_data("1990-04-02"), tipo="p", formacao="Licenciatura em Matemática" ,escolaridade=None, habilidades=None)
        db.session.add(usuario)
        db.session.commit()

        usuario_buscado = db.session.get(Usuario, "12345678901")
        assert usuario_buscado is not None
        assert usuario_buscado.cpf == "12345678901"
        assert usuario_buscado.nome == "John Cena"
        assert usuario_buscado.email == "jcena@hotmail.com"
        assert checar_senha("bocaAberta123", usuario_buscado.senha)
        assert usuario_buscado.telefone == "79 9 9988-7766"
        assert usuario_buscado.endereco == "Rua das Flores, N° 124, Centro, Carira-Sergipe"
        assert usuario_buscado.horario_de_trabalho == "Seg-Sex,13h-17h"
        assert data_para_string(usuario_buscado.data_de_nascimento) == "1990-04-02"
        assert usuario_buscado.tipo == "p"
        assert usuario_buscado.formacao == "Licenciatura em Matemática"
        assert usuario_buscado.escolaridade == None
        assert usuario_buscado.habilidades == None

