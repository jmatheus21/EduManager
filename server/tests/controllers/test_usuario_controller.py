"""
Este módulo contém testes para as rotas e as operações relacionadas a classe de controle `usuario_controller`.

Os testes verificam as operações básicas de CRUD (Create, Read, Update, Delete) para o controle `usuario_controller`,
incluindo cadastro, listagem, busca, atualização e remoção de usuários no banco de dados.
"""

from app.models import Usuario, Disciplina, Cargo
from app.utils.usuario_helpers import checar_senha
from app.extensions import db
from app.utils.date_helpers import string_para_data
from tests.user_event import usuario_entra_no_sistema

def test_cadastrar_usuario_valido_do_tipo_professor(client, app):
    """Testa o cadastro de um usuário do tipo professor com dados válidos.

    Este teste verifica se:
    1. A requisição POST para a rota '/usuario' retorna o status code 201 (Created).
    2. A resposta contém uma mensagem indicando sucesso.
    3. Os dados do usuário cadastrado são retornados corretamente.

    Args:
        client (FlaskClient): Cliente de teste do Flask para simular requisições HTTP.
        app (Flask): Aplicação Flask para acessar o contexto da aplicação.
    """
    with app.app_context():

        usuario_entra_no_sistema(client, app)

        dados_validos = {
            "cpf": "12345678901",
            "nome": "John Cena",
            "email": "jcena@hotmail.com",
            "senha": "bocaAberta123",
            "telefone": "79 9 9988-7766",
            "endereco": "Rua das Flores, N° 124, Centro, Carira-Sergipe",
            "horario_de_trabalho": "Seg-Sex,13h-17h",
            "data_de_nascimento": "1990-04-02",
            "tipo": "p",
            "formacao": "Licenciatura em Matemática",
            "escolaridade": "Superior Completo",
            "habilidades": None,
            "disciplinas": ["MAT123", "FIS789"],
            "cargos": [{"nome": "Professor", "salario": 3060.0, "data_contrato": "2027-12-31"}, {"nome": "Administrador de Recursos", "salario": 1040.0, "data_contrato": "2027-12-31"}]
        }

        disciplina1 = Disciplina(codigo="MAT123", nome="Matemática", carga_horaria=60, ementa=None, bibliografia=None)
        disciplina2 = Disciplina(codigo="FIS789", nome="Física", carga_horaria=60, ementa=None, bibliografia=None)

        db.session.add_all([disciplina1, disciplina2])
        db.session.commit()

        response = client.post('/usuario/', json=dados_validos)

        assert response.status_code == 201, "O status code deve ser 201 (Created)."
        assert "mensagem" in response.json, "A resposta deve conter uma mensagem."
        assert "data" in response.json, "A resposta deve conter os dados do usuário."
        usuario = response.json["data"]

        assert usuario["data_de_nascimento"] == "1990-04-02", f"A data de nascimento do usuário deve ser '1990-04-02', mas foi '{usuario["data_de_nascimento"]}'."
        assert usuario["cpf"] == "12345678901", "O CPF do usuário deve ser '12345678901'."
        assert usuario["nome"] == "John Cena", "O nome do usuário deve ser 'John Cena'."
        assert usuario["email"] == "jcena@hotmail.com", "O email do usuário deve ser 'jcena@hotmail.com'."
        assert checar_senha("bocaAberta123", usuario["senha"]), "A senha do usuário não está correta."
        assert usuario["telefone"] == "79 9 9988-7766", "O telefone do usuário deve ser '79 9 9988-7766'."
        assert usuario["endereco"] == "Rua das Flores, N° 124, Centro, Carira-Sergipe", "O endereço do usuário deve ser 'Rua das Flores, N° 124, Centro, Carira-Sergipe'."
        assert usuario["horario_de_trabalho"] == "Seg-Sex,13h-17h", "O horário de trabalho do usuário deve ser 'Seg-Sex,13h-17h'."
        assert usuario["tipo"] == "p", "O tipo do usuário deve ser 'p', ou seja, um professor."
        assert usuario["formacao"] == "Licenciatura em Matemática", "A formação do usuário deve ser 'Licenciatura em Matemática'."
        assert usuario["escolaridade"] == None, "A escolaridade do usuário deve ser 'None'."
        assert usuario["habilidades"] == None, "As habilidades do usuário deve ser 'None'."
        assert usuario["disciplinas"] == ["MAT123", "FIS789"], "Os códigos das disciplinas devem ser '['MAT123', 'FIS789']'."

        for cargo in usuario["cargos"]:
            cargo["data_contrato"] = cargo["data_contrato"]
            cargo["salario"] = float(cargo["salario"])

        assert usuario["cargos"] == [{"nome": "Professor", "salario": 3060.0, "data_contrato": "2027-12-31"}, 
                                      {"nome": "Administrador de Recursos", "salario": 1040.0, "data_contrato": "2027-12-31"}], \
            f"Os cargos não coincidem. Resposta: {usuario['cargos']}"


def test_cadastrar_usuario_dados_invalidos_do_tipo_professor(client, app):
    """Testa o cadastro de um usuário do tipo professor com dados inválidos.

    Este teste verifica se a requisição POST para a rota '/usuario' retorna o status code 400 (Bad Request)
    e se a resposta contém mensagens de erro para cada campo inválido.

    Args:
        client (FlaskClient): Cliente de teste do Flask para simular requisições HTTP.
        app (Flask): Aplicação Flask para acessar o contexto da aplicação.
    """
    with app.app_context():

        usuario_entra_no_sistema(client, app)

        dados_invalidos = {
            "cpf": "123456789012", 
            "nome": "John Cena",
            "email": "jcenahotmail.com",
            "senha": "bocaAberta123",
            "telefone": "(79) 9 9988-7766",
            "endereco": "Rua das Flores, N° 124, Centro, Carira-Sergipe",
            "horario_de_trabalho": "Seg-Sex,08h-17h",
            "data_de_nascimento": "1990-04-02",
            "tipo": "p",
            "formacao": None,
            "escolaridade": "Superior Completo",
            "habilidades": None,
            "disciplinas": ["MAT123", "FIS78965432"],
            "cargos": [{"nome": "Professor", "salario": 3060.0, "data_contrato": "2024-05-27"}, {"nome": "Administrador de Recursos", "salario": 1040.0, "data_contrato": "2027-12-31"}]
        }
         
        response = client.post('/usuario/', json=dados_invalidos)

        assert response.status_code == 400, "O status code deve ser 400 (Bad Request)."
        assert "erro" in response.json, "A resposta deve conter mensagens de erro."
        assert len(response.json["erro"]) == 6, "Deve haver 6 erros de validação."

def test_cadastrar_usuario_disciplina_inexistente_do_tipo_professor(client, app):
    """Testa o cadastro de um usuário do tipo professor com disciplina inexistente.

    Este teste verifica se a requisição POST para a rota '/usuario' retorna o status code 400 (Bad Request)
    e se a resposta contém mensagens de erro para cada campo inválido.

    Args:
        client (FlaskClient): Cliente de teste do Flask para simular requisições HTTP.
        app (Flask): Aplicação Flask para acessar o contexto da aplicação.
    """
    with app.app_context():

        usuario_entra_no_sistema(client, app)

        dados_invalidos = {
            "cpf": "12345678901",
            "nome": "John Cena",
            "email": "jcena@bol.com",
            "senha": "bocaAberta123",
            "telefone": "79 9 9988-7766",
            "endereco": "Rua das Flores, N° 124, Centro, Carira-Sergipe",
            "horario_de_trabalho": "Seg-Sex,13h-17h",
            "data_de_nascimento": "1990-04-02",
            "tipo": "p",
            "formacao": "Licenciatura em Matemática",
            "escolaridade": None,
            "habilidades": None,
            "disciplinas": ["MAT123"],
            "cargos": [{"nome": "Professor", "salario": 3060.0, "data_contrato": "2028-05-27"}, {"nome": "Administrador de Recursos", "salario": 1040.0, "data_contrato": "2027-12-31"}]
        }
         
        response = client.post('/usuario/', json=dados_invalidos)

        assert response.status_code == 400, "O status code deve ser 400 (Bad Request)."
        assert "erro" in response.json, "A resposta deve conter mensagens de erro."
        assert len(response.json["erro"]) == 1, "Deve haver 1 erro na saída"
        erros = response.json["erro"]

        assert "Disciplinas inválidas: MAT123" in erros, "Deve haver um erro de disciplina inválida"

def test_cadastrar_usuario_existente(client, app):
    """Testa o cadastro de um usuário do tipo professor com dados inválidos.

    Este teste verifica se a requisição POST para a rota '/usuario' retorna o status code 400 (Bad Request)
    e se a resposta contém mensagens de erro para cada campo inválido.

    Args:
        client (FlaskClient): Cliente de teste do Flask para simular requisições HTTP.
        app (Flask): Aplicação Flask para acessar o contexto da aplicação.
    """
    with app.app_context():

        usuario_entra_no_sistema(client, app)

        dados_invalidos = {
            "cpf": "12345678901",
            "nome": "John Cena",
            "email": "jcena@bol.com",
            "senha": "bocaAberta123",
            "telefone": "79 9 9988-7766",
            "endereco": "Rua das Flores, N° 124, Centro, Carira-Sergipe",
            "horario_de_trabalho": "Seg-Sex,13h-17h",
            "data_de_nascimento": "1990-04-02",
            "tipo": "p",
            "formacao": "Licenciatura em Matemática",
            "escolaridade": None,
            "habilidades": None,
            "disciplinas": ["MAT123"],
            "cargos": [{"nome": "Professor", "salario": 3060.0, "data_contrato": "2027-05-27"}, {"nome": "Administrador de Recursos", "salario": 1040.0, "data_contrato": "2027-12-31"}]
        }

        usuario_existente = Usuario(cpf=dados_invalidos['cpf'], nome=dados_invalidos['nome'], email=dados_invalidos['email'], senha=dados_invalidos['senha'], telefone=dados_invalidos['telefone'], endereco=dados_invalidos['endereco'], horario_de_trabalho=dados_invalidos['horario_de_trabalho'], data_de_nascimento=string_para_data(dados_invalidos['data_de_nascimento']), tipo=dados_invalidos['tipo'], formacao=dados_invalidos['formacao'], escolaridade=dados_invalidos['escolaridade'], habilidades=dados_invalidos['habilidades'])
        db.session.add(usuario_existente)
        db.session.commit()
         
        response = client.post('/usuario/', json=dados_invalidos)

        assert response.status_code == 400, "O status code deve ser 400 (Bad Request)."
        assert "erro" in response.json, "A resposta deve conter mensagens de erro."
        assert len(response.json["erro"]) == 1, "Deve haver 1 erros na saída."
        erro = response.json["erro"]

        assert "Usuário já existe" in erro, "Deve haver um erro de usuário existente"


def test_cadastrar_usuario_valido_do_tipo_funcionario(client, app):
    """Testa o cadastro de um usuário do tipo funcionário com dados válidos.

    Este teste verifica se:
    1. A requisição POST para a rota '/usuario' retorna o status code 201 (Created).
    2. A resposta contém uma mensagem indicando sucesso.
    3. Os dados do usuário cadastrado são retornados corretamente.

    Args:
        client (FlaskClient): Cliente de teste do Flask para simular requisições HTTP.
        app (Flask): Aplicação Flask para acessar o contexto da aplicação.
    """
    with app.app_context():

        usuario_entra_no_sistema(client, app)

        dados_validos = {
            "cpf": "98765432108",
            "nome": "Randy Orton",
            "email": "rnorton@hotmail.com",
            "senha": "bocaAberta123",
            "telefone": "16 9 9944-5533",
            "endereco": "Rua das Nuvens, N° 99, Bairro Industrial, Araraquara-São Paulo",
            "horario_de_trabalho": "Seg-Sex,07h-12h",
            "data_de_nascimento": "1995-08-17",
            "tipo": "f",
            "formacao": None,
            "escolaridade": "Ensino Médio Completo",
            "habilidades": "Ferramentas do pacote office (Word, Excel...)",
            "disciplinas": None,
            "cargos": [{"nome": "Funcionário", "salario": 2030.0, "data_contrato": "2027-12-31"}, {"nome": "Administrador de Recursos", "salario": 1040.0, "data_contrato": "2027-12-31"}]
        }

        response = client.post('/usuario/', json=dados_validos)

        assert response.status_code == 201, "O status code deve ser 201 (Created)."
        assert "mensagem" in response.json, "A resposta deve conter uma mensagem."
        assert "data" in response.json, "A resposta deve conter os dados do usuário."
        usuario = response.json["data"]

        assert usuario["data_de_nascimento"] == "1995-08-17", f"A data de nascimento do usuário deve ser '1995-08-17', mas foi '{usuario["data_de_nascimento"]}'."
        assert usuario["cpf"] == "98765432108", "O CPF do usuário deve ser '98765432108'."
        assert usuario["nome"] == "Randy Orton", "O nome do usuário deve ser 'Randy Orton'."
        assert usuario["email"] == "rnorton@hotmail.com", "O email do usuário deve ser 'rnorton@hotmail.com'."
        assert checar_senha("bocaAberta123", usuario["senha"]), "A senha do usuário não está correta."
        assert usuario["telefone"] == "16 9 9944-5533", "O telefone do usuário deve ser '16 9 9944-5533'."
        assert usuario["endereco"] == "Rua das Nuvens, N° 99, Bairro Industrial, Araraquara-São Paulo", "O endereço do usuário deve ser 'ua das Nuvens, N° 99, Bairro Industrial, Araraquara-São Paulo'."
        assert usuario["horario_de_trabalho"] == "Seg-Sex,07h-12h", "O horário de trabalho do usuário deve ser 'Seg-Sex,08h-12h'."
        assert usuario["tipo"] == "f", "O tipo do usuário deve ser 'f', ou seja, um funcionário."
        assert usuario["formacao"] == None, "A formação do usuário deve ser 'None'."
        assert usuario["escolaridade"] == "Ensino Médio Completo", "A escolaridade do usuário deve ser 'Ensino Médio Completo'."
        assert usuario["habilidades"] == "Ferramentas do pacote office (Word, Excel...)", "As habilidades do usuário deve ser 'Ferramentas do pacote office (Word, Excel...)'."
        assert usuario["disciplinas"] == [], "O(s) código(s) da(s) disciplina(s) deve(m) ser '[]'."

        for cargo in usuario["cargos"]:
            cargo["data_contrato"] = cargo["data_contrato"]
            cargo["salario"] = float(cargo["salario"])
        
        assert usuario["cargos"] == [{"nome": "Funcionário", "salario": 2030.0, "data_contrato": "2027-12-31"}, 
                                      {"nome": "Administrador de Recursos", "salario": 1040.0, "data_contrato": "2027-12-31"}], \
            f"Os cargos não coincidem. Resposta: {usuario['cargos']}"


def test_cadastrar_usuario_dados_invalidos_do_tipo_funcionario(client, app):
    """Testa o cadastro de um usuário do tipo funcionário com dados inválidos.

    Este teste verifica se a requisição POST para a rota '/usuario' retorna o status code 400 (Bad Request)
    e se a resposta contém mensagens de erro para cada campo inválido.

    Args:
        client (FlaskClient): Cliente de teste do Flask para simular requisições HTTP.
        app (Flask): Aplicação Flask para acessar o contexto da aplicação.
    """
    with app.app_context():

        usuario_entra_no_sistema(client, app)

        dados_invalidos = {
            "cpf": "987654321081",
            "nome": "Randy Orton",
            "email": "rnorton@hotmail.com",
            "senha": "eazy",
            "telefone": "16 9 99445533",
            "endereco": "Rua das Nuvens, N° 99, Bairro Industrial, Araraquara-São Paulo",
            "horario_de_trabalho": "Seg-Sex,07h-12h",
            "data_de_nascimento": "2028-08-17",
            "tipo": "f",
            "formacao": None,
            "escolaridade": "Ensino Médio Completo",
            "habilidades": "Ferramentas do pacote office (Word, Excel...)",
            "disciplinas": None,
            "cargos": [{"nome": "Funcionário", "salario": 30.0, "data_contrato": "2021-12-31"}, {"nome": "Administrador de Recursos", "salario": 1040.0, "data_contrato": "2027-12-31"}]
        }
         
        response = client.post('/usuario/', json=dados_invalidos)

        assert response.status_code == 400, "O status code deve ser 400 (Bad Request)."
        assert "erro" in response.json, "A resposta deve conter mensagens de erro."
        assert len(response.json["erro"]) == 6, "Deve haver 6 erros de validação."

def test_alterar_usuario_cpf_duplicado(client, app):
    """Testa a atualização dos dados de um usuário com um cpf de outro usuário.

    Este teste verifica se a requisição PUT para a rota '/usuario/{cpf}' retorna o status code 400 (Bad Request)
    e se a resposta contém mensagens de erro para cada campo inválido.

    Args:
        client (FlaskClient): Cliente de teste do Flask para simular requisições HTTP.
        app (Flask): Aplicação Flask para acessar o contexto da aplicação.
    """
    with app.app_context():

        usuario_entra_no_sistema(client, app)

        cargo1 = Cargo(nome="Funcionário", salario=2060.0, data_contrato="2027-12-31")
        cargo2 = Cargo(nome="Administrador de Recursos", salario=1040.0, data_contrato="2027-12-31")

        usuario1 = Usuario(
                            cpf="98765432108",
                            nome="Randy Orton",
                            email="rnorton@hotmail.com",
                            senha="bocaAberta123",
                            telefone="16 9 9944-5533",
                            endereco="Rua das Flores, N° 124, Centro, Carira-Sergipe",
                            horario_de_trabalho="Seg-Sex,13h-17h",
                            data_de_nascimento="1990-04-02",
                            tipo="f",
                            formacao=None,
                            escolaridade="Ensino Médio Completo",
                            habilidades="Ferramentas do pacote office (Word, Excel...)",
                            disciplinas=[],
                            cargos=[cargo1]
                        )
        
        usuario2 = Usuario(
                            cpf="12345678901",
                            nome="John Cena",
                            email="jcena@gmail.com",
                            senha="bocaAberta123",
                            telefone="79 9 9988-7766",
                            endereco="Rua das Flores, N° 123, Centro, Carira-Sergipe",
                            horario_de_trabalho="Seg-Sex,13h-17h",
                            data_de_nascimento="1990-04-02",
                            tipo="f",
                            formacao=None,
                            escolaridade="Ensino Médio Completo",
                            habilidades="Ferramentas do pacote office (Word, Excel...)",
                            disciplinas=[],
                            cargos=[cargo2]
                        )
    
        db.session.add_all([cargo1, cargo2, usuario1, usuario2])
        db.session.commit()

        # Dados para atualização
        dados_atualizacao = {
            "cpf": "98765432108",
            "nome": "John Cena",
            "email": "jcena@gmail.com",
            "senha": "bocaAberta123",
            "telefone": "79 9 9988-7766",
            "endereco": "Rua das Flores, N° 124, Centro, Carira-Sergipe",
            "horario_de_trabalho": "Seg-Sex,13h-17h",
            "data_de_nascimento": "1990-04-02",
            "tipo": "f",
            "formacao": None,
            "escolaridade": "Ensino Médio Completo",
            "habilidades": "Ferramentas do pacote office (Word, Excel...)",
            "disciplinas": [],
            "cargos": [{"nome": "Administrador de Recursos", "salario": 1040.0, "data_contrato": "2027-12-31"}]
        }

        response = client.put(f'/usuario/{usuario2.cpf}', json=dados_atualizacao)

        assert response.status_code == 400, "O status code deve ser 400 (Bad Request)."
        assert "erro" in response.json, "A resposta deve conter mensagens de erro."
        assert len(response.json["erro"]) == 1, "Deve haver 1 erros na saída."
        erro = response.json["erro"]

        assert "Usuário já existe" in erro, "Deve haver um erro de usuário existente"

def test_alterar_usuario_do_tipo_professor(client, app):
    """Testa a atualização dos dados de um usuário do tipo professor.

    Este teste verifica se a requisição PUT para a rota '/usuario/{cpf}' retorna o status code 200 (OK),
    se a resposta contém uma mensagem de sucesso e se os dados do usuário foram atualizados corretamente.

    Args:
        client (FlaskClient): Cliente de teste do Flask para simular requisições HTTP.
        app (Flask): Aplicação Flask para acessar o contexto da aplicação.
    """
    with app.app_context():

        usuario_entra_no_sistema(client, app)

        disciplina1 = Disciplina(codigo="MAT123", nome="Matemática", carga_horaria=60, ementa=None, bibliografia=None)
        disciplina2 = Disciplina(codigo="FIS789", nome="Física", carga_horaria=60, ementa=None, bibliografia=None)

        cargo1 = Cargo(nome="Professor", salario=3060.0, data_contrato="2027-12-31")
        cargo2 = Cargo(nome="Administrador de Recursos", salario=1040.0, data_contrato="2027-12-31")

        usuario = Usuario(
                            cpf="12345678901",
                            nome="John Cena",
                            email="jcena@hotmail.com",
                            senha="bocaAberta123",
                            telefone="79 9 9988-7766",
                            endereco="Rua das Flores, N° 124, Centro, Carira-Sergipe",
                            horario_de_trabalho="Seg-Sex,13h-17h",
                            data_de_nascimento="1990-04-02",
                            tipo="p",
                            formacao="Licenciatura em Matemática",
                            escolaridade="Superior Completo",
                            habilidades=None,
                            disciplinas=[disciplina1, disciplina2],
                            cargos=[cargo1, cargo2]
                        )
    
        db.session.add_all([disciplina1, disciplina2, cargo1, cargo2, usuario])
        db.session.commit()

        # Dados para atualização
        dados_atualizacao = {
            "cpf": "12345678901",
            "nome": "John Cena",
            "email": "jcena@gmail.com",
            "telefone": "79 9 9988-7766",
            "endereco": "Rua das Flores, N° 124, Centro, Carira-Sergipe",
            "horario_de_trabalho": "Seg-Sex,13h-17h",
            "data_de_nascimento": "1990-04-02",
            "tipo": "p",
            "formacao": "Licenciatura em Matemática",
            "escolaridade": "Superior Completo",
            "habilidades": None,
            "disciplinas": ["MAT123", "FIS789"],
            "cargos": [{"nome": "Professor", "salario": 3060.0, "data_contrato": "2027-12-31"}, {"nome": "Administrador de Recursos", "salario": 1040.0, "data_contrato": "2027-12-31"}]
        }

        response = client.put(f'/usuario/{usuario.cpf}', json=dados_atualizacao)
        assert response.status_code == 200, "O status code deve ser 200 (OK)."
        assert response.json["mensagem"] == "Usuário atualizado com sucesso!"
        dados = response.json["data"]

        assert dados["data_de_nascimento"] == "1990-04-02", f"A data de nascimento do usuário deve ser '1990-04-02', mas foi '{dados["data_de_nascimento"]}'."
        assert dados["cpf"] == "12345678901", "O CPF do usuário deve ser '12345678901'."
        assert dados["nome"] == "John Cena", "O nome do usuário deve ser 'John Cena'."
        assert dados["email"] == "jcena@gmail.com", "O email do usuário deve ser 'jcena@gmail.com'."
        assert dados["telefone"] == "79 9 9988-7766", "O telefone do usuário deve ser '79 9 99887766'."
        assert dados["endereco"] == "Rua das Flores, N° 124, Centro, Carira-Sergipe", "O endereço do usuário deve ser 'Rua das Flores, N° 124, Centro, Carira-Sergipe'."
        assert dados["horario_de_trabalho"] == "Seg-Sex,13h-17h", "O horário de trabalho do usuário deve ser 'Seg-Sex,13h-17h'."
        assert dados["tipo"] == "p", "O tipo do usuário deve ser 'p', ou seja, um professor."
        assert dados["formacao"] == "Licenciatura em Matemática", "A formação do usuário deve ser 'Licenciatura em Matemática'."
        assert dados["escolaridade"] == None, "A escolaridade do usuário deve ser 'None'."
        assert dados["habilidades"] == None, "As habilidades do usuário deve ser 'None'."
        assert dados["disciplinas"] == ["MAT123", "FIS789"], "Os códigos das disciplinas devem ser '['MAT123', 'FIS789']'."

        for cargo in dados["cargos"]:
            cargo["salario"] = float(cargo["salario"])

        assert dados["cargos"] == [{"nome": "Professor", "salario": 3060.0, "data_contrato": "2027-12-31"}, 
                                      {"nome": "Administrador de Recursos", "salario": 1040.0, "data_contrato": "2027-12-31"}], \
            f"Os cargos não coincidem. Resposta: {dados['cargos']}"
        

def test_alterar_usuario_do_tipo_funcionario(client, app):
    """Testa a atualização dos dados de um usuário do tipo funcionario.

    Este teste verifica se a requisição PUT para a rota '/usuario/{cpf}' retorna o status code 200 (OK),
    se a resposta contém uma mensagem de sucesso e se os dados do usuário foram atualizados corretamente.

    Args:
        client (FlaskClient): Cliente de teste do Flask para simular requisições HTTP.
        app (Flask): Aplicação Flask para acessar o contexto da aplicação.
    """
    with app.app_context():

        usuario_entra_no_sistema(client, app)

        cargo1 = Cargo(nome="Funcionário", salario=2060.0, data_contrato="2027-12-31")
        cargo2 = Cargo(nome="Administrador de Recursos", salario=1040.0, data_contrato="2027-12-31")

        usuario = Usuario(
                            cpf="98765432108",
                            nome="Randy Orton",
                            email="rnorton@hotmail.com",
                            senha="bocaAberta123",
                            telefone="16 9 9944-5533",
                            endereco="Rua das Flores, N° 124, Centro, Carira-Sergipe",
                            horario_de_trabalho="Seg-Sex,13h-17h",
                            data_de_nascimento="1990-04-02",
                            tipo="f",
                            formacao=None,
                            escolaridade="Ensino Médio Completo",
                            habilidades="Ferramentas do pacote office (Word, Excel...)",
                            disciplinas=[],
                            cargos=[cargo1, cargo2]
                        )
    
        db.session.add_all([cargo1, cargo2, usuario])
        db.session.commit()

        # Dados para atualização
        dados_atualizacao = {
            "cpf": "98765432108",
            "nome": "Randy Orton",
            "email": "rnorton@hotmail.com",
            "telefone": "21 9 9944-5533",
            "endereco": "Rua das Flores, N° 123, Centro, Carira-Sergipe",
            "horario_de_trabalho": "Seg-Sex,12h-17h",
            "data_de_nascimento": "1990-07-15",
            "tipo": "f",
            "formacao": None,
            "escolaridade": "Ensino Médio Completo",
            "habilidades": "Ferramentas do pacote office (Word, Excel...)",
            "disciplinas": [],
            "cargos": [{"nome": "Funcionário", "salario": 2000.0, "data_contrato": "2027-12-31"}, {"nome": "Administrador de Recursos", "salario": 1040.0, "data_contrato": "2027-12-31"}, {"nome": "Cargo teste", "salario": 5040.0, "data_contrato": "2027-12-31"}]
        }

        response = client.put(f'/usuario/{usuario.cpf}', json=dados_atualizacao)
        assert response.status_code == 200, "O status code deve ser 200 (OK)."
        assert response.json["mensagem"] == "Usuário atualizado com sucesso!"
        dados = response.json["data"]

        assert dados["data_de_nascimento"] == "1990-07-15", f"A data de nascimento do usuário deve ser '1990-07-15', mas foi '{dados["data_de_nascimento"]}'."
        assert dados["cpf"] == "98765432108", "O CPF do usuário deve ser '98765432108'."
        assert dados["nome"] == "Randy Orton", "O nome do usuário deve ser 'Randy Orton'."
        assert dados["email"] == "rnorton@hotmail.com", "O email do usuário deve ser 'rnorton@hotmail.com'."
        assert dados["telefone"] == "21 9 9944-5533", "O telefone do usuário deve ser '21 9 9944-5533'."
        assert dados["endereco"] == "Rua das Flores, N° 123, Centro, Carira-Sergipe", "O endereço do usuário deve ser 'Rua das Flores, N° 123, Centro, Carira-Sergipe'."
        assert dados["horario_de_trabalho"] == "Seg-Sex,12h-17h", "O horário de trabalho do usuário deve ser 'Seg-Sex,12h-17h'."
        assert dados["tipo"] == "f", "O tipo do usuário deve ser 'f', ou seja, um funcionário."
        assert dados["formacao"] == None, "A formação do usuário deve ser 'None'."
        assert dados["escolaridade"] == "Ensino Médio Completo", "A escolaridade do usuário deve ser 'Ensino Médio Completo'."
        assert dados["habilidades"] == "Ferramentas do pacote office (Word, Excel...)", "As habilidades do usuário deve ser 'Ferramentas do pacote office (Word, Excel...)'."
        assert dados["disciplinas"] == [], "Os códigos das disciplinas devem ser '[]'."

        for cargo in dados["cargos"]:
            cargo["salario"] = float(cargo["salario"])
        
        assert {"nome": "Funcionário", "salario": 2000.0, "data_contrato": "2027-12-31"} in dados["cargos"], "Faltando cargo"
        assert {"nome": "Administrador de Recursos", "salario": 1040.0, "data_contrato": "2027-12-31"} in dados["cargos"], "Faltando cargo"
        assert {"nome": "Cargo teste", "salario": 5040.0, "data_contrato": "2027-12-31"} in dados["cargos"], "Faltando cargo"

def test_deletar_usuario_do_tipo_professor(client, app):
    """Testa a exclusão de um usuário do tipo professor.

    Este teste verifica se a requisição DELETE para a rota '/usuario/{cpf}' retorna o status code 200 (OK)
    e se a resposta contém uma mensagem de sucesso.

    Args:
        client (FlaskClient): Cliente de teste do Flask para simular requisições HTTP.
        app (Flask): Aplicação Flask para acessar o contexto da aplicação.
    """
    with app.app_context():

        usuario_entra_no_sistema(client, app)

        disciplina1 = Disciplina(codigo="MAT123", nome="Matemática", carga_horaria=60, ementa=None, bibliografia=None)
        disciplina2 = Disciplina(codigo="FIS789", nome="Física", carga_horaria=60, ementa=None, bibliografia=None)

        cargo1 = Cargo(nome="Professor", salario=3060.0, data_contrato="2027-12-31")
        cargo2 = Cargo(nome="Administrador de Recursos", salario=1040.0, data_contrato="2027-12-31")

        usuario = Usuario(
                            cpf="12345678901",
                            nome="John Cena",
                            email="jcena@hotmail.com",
                            senha="bocaAberta123",
                            telefone="79 9 9988-7766",
                            endereco="Rua das Flores, N° 124, Centro, Carira-Sergipe",
                            horario_de_trabalho="Seg-Sex,13h-17h",
                            data_de_nascimento="1990-04-02",
                            tipo="p",
                            formacao="Licenciatura em Matemática",
                            escolaridade="Superior Completo",
                            habilidades=None,
                            disciplinas=[disciplina1, disciplina2],
                            cargos=[cargo1, cargo2]
                        )
    
        db.session.add_all([disciplina1, disciplina2, cargo1, cargo2, usuario])
        db.session.commit()

        response = client.delete(f'/usuario/{usuario.cpf}')
        assert response.status_code == 200, "O status code deve ser 200 (OK)."
        assert response.json["mensagem"] == "Usuário deletado com sucesso!"


def test_deletar_usuario_do_tipo_funcionario(client, app):
    """Testa a exclusão de um usuário do tipo funcionário.

    Este teste verifica se a requisição DELETE para a rota '/usuario/{cpf}' retorna o status code 200 (OK)
    e se a resposta contém uma mensagem de sucesso.

    Args:
        client (FlaskClient): Cliente de teste do Flask para simular requisições HTTP.
        app (Flask): Aplicação Flask para acessar o contexto da aplicação.
    """
    with app.app_context():

        usuario_entra_no_sistema(client, app)
        
        cargo1 = Cargo(nome="Funcionário", salario=2060.0, data_contrato="2027-12-31")
        cargo2 = Cargo(nome="Administrador de Recursos", salario=1040.0, data_contrato="2027-12-31")

        usuario = Usuario(
                            cpf="98765432108",
                            nome="Randy Orton",
                            email="rnorton@hotmail.com",
                            senha="bocaAberta123",
                            telefone="16 9 9944-5533",
                            endereco="Rua das Flores, N° 124, Centro, Carira-Sergipe",
                            horario_de_trabalho="Seg-Sex,13h-17h",
                            data_de_nascimento="1990-04-02",
                            tipo="f",
                            formacao=None,
                            escolaridade="Ensino Médio Completo",
                            habilidades="Ferramentas do pacote office (Word, Excel...)",
                            disciplinas=[],
                            cargos=[cargo1, cargo2]
                        )
    
        db.session.add_all([cargo1, cargo2, usuario])
        db.session.commit()

        response = client.delete(f'/usuario/{usuario.cpf}')
        assert response.status_code == 200, "O status code deve ser 200 (OK)."
        assert response.json["mensagem"] == "Usuário deletado com sucesso!"