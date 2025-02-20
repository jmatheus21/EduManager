import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # SECRET_KEY = os.getenv('SECRET_KEY', 'uma_chave_secreta_muito_segura')

    # Configuração do SQLAlchemy
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@"
        f"{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False