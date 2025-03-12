from app.utils.validators import validar_usuario, validar_cargo

def test_validar_usuario(app):
    with app.app_context():
        data = {
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
            "cargos": [{"nome": "Professor", "salario": 3060.00, "data_contrato": "2027-12-31"}, {"nome": "Administrador de Recursos", "salario": 1040.00, "data_contrato": "2027-12-31"}]
        }

        erros = validar_usuario(cpf=data['cpf'], nome=data['nome'], email=data['email'], senha=data['senha'], telefone=data['telefone'], endereco=data['endereco'], horario_de_trabalho=data['horario_de_trabalho'], data_de_nascimento=data['data_de_nascimento'], tipo=data['tipo'], formacao=data['formacao'], escolaridade=data['escolaridade'], habilidades=data['habilidades'], disciplinas=data['disciplinas'], cargos=data['cargos'])

        assert erros == [], "Não deve ter nenhum erro"

def test_validar_cargo(app):
    with app.app_context():
        cargo_valido = {
            "nome": "Professor",
            "salario": 3060.0,
            "data_contrato": "2024-12-31"
        }

        erros = validar_cargo(nome=cargo_valido["nome"], salario=cargo_valido["salario"], data_contrato=cargo_valido["data_contrato"])

        assert erros == ["O atributo 'data_contrato' é obrigatório e precisa ser uma data futura"], "Erro na data do contrato"