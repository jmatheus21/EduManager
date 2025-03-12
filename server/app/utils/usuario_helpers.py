from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

def gerar_hashing (senha: str):
    """
    Gera um hash seguro para a senha fornecida utilizando o Bcrypt.

    Essa função utiliza o método generate_password_hash do Flask-Bcrypt para criar um hash a partir da senha
    em texto plano. Em seguida, o hash gerado é decodificado para o formato UTF-8, retornando uma string.

    Args:
        senha (str): A senha em texto plano que será convertida em hash.

    Returns:
        str: O hash da senha, decodificado como uma string UTF-8.
    """
    return bcrypt.generate_password_hash(senha).decode('utf-8')

def checar_senha (senha: str, hashed: str):
    """
    Verifica se a senha fornecida corresponde ao hash armazenado.

    Essa função utiliza o método check_password_hash do Flask-Bcrypt para comparar uma senha em texto plano 
    com um hash previamente gerado. Retorna True se a senha corresponder ao hash e False caso contrário.

    Args:
        senha (str): A senha em texto plano que será verificada.
        hashed (str): O hash da senha com o qual a comparação será feita.

    Returns:
        bool: True se a senha corresponder ao hash, False caso contrário.
    """
    return bcrypt.check_password_hash(hashed, senha)

