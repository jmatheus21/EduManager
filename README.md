# Sistema de Gestão Escolar (EduManager)
## Equipe
Os desenvolvedores integrantes desse projeto são: 
- EDGAR DE SOUZA DIAS
- ISAAC LEVI LIRA DE OLIVEIRA
- JOÃO EMANUEL MENDONÇA APÓSTOLO
- JOSÉ MATHEUS RIBEIRO DOS SANTOS
- MARIA EDUARDA PIRES POSSARI DOS SANTOS
- RAFAEL LIMA DANTAS
- ULISSES DE JESUS CAVALCANTE

## Instruções para desenvolvedores

### Instalação do Backend

Para instalar todas as dependências do servidor, navegue até a pasta *server*, a partir do diretório raíz do projeto,com o comando no terminal:
```
cd server
```
Após isso, você deve criar um ambiente virtual:
```
python3 -m venv venv
```
Ative o ambiente virtual (Windows):
```
venv\Scripts\activate
```
Depois, instale todas as dependências com o comando:
```
pip install -r requirements.txt
```
O backend utiliza variáveis de ambiente para armazenar informações sensíveis ou específicas do ambiente. Crie um arquivo **.env** na pasta *server* com o seguinte conteúdo:
```
# Variáveis de ambiente para o banco de dados
DB_USER=
DB_PASSWORD=
DB_HOST=localhost
DB_PORT=5432
DB_NAME=
SECRET_KEY=
DEBUG=True
```
**Observação:** *Certifique-se de preencher os valores pelas configurações adequadas ao seu ambiente.*

Para iniciar o servidor **Flask**, execute o seguinte comando:
```
python run.py
```
Por padrão, o servidor estará disponível em **http://localhost:5000**.

### Instalação do Frontend
Para instalar todas as dependências do cliente, navegue até a pasta *client*, a partir do diretório raíz do projeto, com o comando no terminal:
```
cd client
```
Para instalar todas as dependências do projeto **node.js**, execute o comando:
```
npm install
```
Para iniciar o servidor de desenvolvimento do **React.js**, execute o seguinte comando:
```
npm run dev
```
Por padrão, o frontend estará disponível em **http://localhost:5173**.
