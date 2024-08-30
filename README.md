# Projeto final 🎉 do Curso de FastAPI do ZERO com o 🦖 Dunossauro

__status em andamento__

FastAPI é um framework Python moderno, projetado para simplicidade, velocidade e eficiência, facilitando o desenvolvimento de APIs.

## 01 Entendimento do Negócio
O objetivo do projeto é criarmos uma gerenciador de livros e relacionar com seus autores. Tudo isso em um contexto bastante simplificado. 

A implementação será baseada em 3 pilares:
![alt text](image.png)

A API dividiremos os endpoints em três routers:
1. contas: Gerenciamento de contas e de acesso à API
2. livros: Gerenciamento de livros
3. romancistas: Gerenciamento de romancistas

Demais detalhes em: https://fastapidozero.dunossauro.com/14/#o-projeto


## 02 Configurando o Ambiente de Desenvolvimento
1. definindo a ferramenta ou IDE de desenvolvimento <br>
    1. VSCode + Terminal (Windows)
1. no terminal verificar a instalação e versão do Python
1. Se necessário, instalação do pyenv, recomendado usar o pyenv-windows
    1. verificar qual versão do python deseja e instalar
    2. atualizar o pyenv
    3. instalar uma versão do python com o pyenv
    4. definir a versão globao do python
1. Instalação de ferramentas / bibliotecas recomendadas<br>
    1. pipx (O pipx é uma ferramenta para instalar e gerenciar aplicativos Python isoladamente, ou seja, ela permite que você instale pacotes Python que são aplicativos de linha de comando em ambientes virtuais próprios, sem interferir no ambiente global de pacotes do Python instalado no seu sistema.) 
    2. poetry
1. poetry <br>
    1. após instalado, executar o comando "pipx ensurepath", fechar e reabrir o terminal
    2. entrar no diretório onde se deseja criar o projeto e criá-lo com o poetry
    3. definir qual a versão do Python será utilizada nesse projeto/diretório "pyenv local 3.12.5"
    4. criar o ambiente virtual (venv), que criará um arquivo oculto chamado `.python-version` na raiz do projeto, este deve ser alterado para 
    [tool.poetry.dependencies]
    python = "3.12.*"

    o * quer dizer qualquer versão da 3.12

    5. inicializar o ambiente virtual
1. escrevendo no `README.MD` (atualizando sempre)
1. instalando a biblioteca do FastAPI

### Execução dos comandos em ordem conforme necessidade
~~~shell
python --version
pyenv --version
pyenv update
pyenv versions # verifica as versões no sistema e qual está setado como principal
pyenv install --list # verifica a lista das versões Python disponível e pode pegar a útlima "lberada"
pyenv install 3.12.5
pyenv versions
pyenv global 3.12.5
pyenv versions

pip install pipx
pipx install poetry
pipx install ignr
pipx ensurepath # executar após poetry instalado, fechar e reabrir o terminal

cd C:\projetos\projetos-GIT\

# Criando o projeto
poetry new mada
cd mada
pyenv local 3.12.5 # dizer ao pyenv qual versão do python será usada nesse diretório
poetry install # Cria o ambiente virtual (venv)
~~~

### Primeira Execução de um "Hello, World!" teste no terminal

~~~shell
poetry shell
poetry add fastapi # Adiciona o FastAPI no nosso ambiente virtual
poetry add fastapi[standard] # deu erro só com o comando acima e pediu esse

# Criando a aplicação e testando
echo > mada/app.py
~~~

Arquivo inicial `app.py`

~~~python
from fastapi import FastAPI

app = FastAPI()


@app.get('/')
def read_root():
    return {'message': 'Olá Mundo!'}
~~~

Executar a função pelo terminal em modo interativo para chamar a função.
~~~shell
python -i .\mada\app.py
>>> read_root()
~~~

### Testando o ambiente web: iniciar nosso servidor FastAPI para iniciar nossa aplicação
~~~shell
fastapi dev mada/app.py
~~~

Com os testes no terminal e na web ok, próximo passo:

#### Instalando + ferramentas de desenvolvimento
~~~shell
poetry add --group dev pytest pytest-cov taskipy ruff httpx
~~~

Após a instalação das ferramentas de desenvolvimento, precisamos definir as configurações de cada uma individualmente no arquivo `pyproject.toml`.

~~~toml
[tool.ruff]
line-length = 79
extend-exclude = ['migrations']
~~~

~~~toml
[tool.ruff.lint]
preview = true
select = ['I', 'F', 'E', 'W', 'PL', 'PT']
~~~

~~~toml
[tool.ruff.format]
preview = true
quote-style = 'single'
~~~

~~~toml
[tool.pytest.ini_options]
pythonpath = "."
addopts = '-p no:warnings'
~~~

~~~toml
[tool.taskipy.tasks]
lint = 'ruff check . && ruff check . --diff'
format = 'ruff check . --fix && ruff format .'
run = 'fastapi dev mada/app.py'
pre_test = 'task lint'
test = 'pytest -s -x --cov=mada -vv'
post_test = 'coverage html'
~~~

__OBS.:__ atentar para os nomes dos projetos que influencia neste arqvuivo.

Após arquivo configurado, pode testar os comandos criados para o taskipy:
~~~shell
task lint
task format
task lint
~~~

## Introdução ao Pytest: Testando o "Hello, World!"
~~~shell
task test
~~~

As linhas no terminal são referentes ao pytest, que disse que coletou 0 itens. Nenhum teste foi executado.

Por não encontrar nenhum teste, o pytest retornou um "erro". Isso significa que nossa tarefa post_test não foi executada. Podemos executá-la manualmente:

~~~shell
task post_test
~~~

O comando acima gera um relatório de cobertura de testes em formato HTML no diretório `htmlcov.html`. Pode abrir esse arquivo no navegador e entender exatamente quais linhas do código não estão sendo testadas em `htmlcov\index.html`.
~~~shell
coverage html # Wrote HTML report to htmlcov\index.html
~~~

### Escrevendo o teste
Criação dos arquivos de teste.
~~~shell
echo > tests/test_app.py
~~~

Conteúdo do arquivo:
~~~python
from fastapi.testclient import TestClient  

from mada.app import app  

client = TestClient(app)
~~~

~~~shell
task format
task test 
~~~

Por não coletar nenhum teste, o pytest ainda retornou um "erro". Para ver a cobertura, precisaremos executar novamente o post_test manualmente:
~~~shell
task post_test
~~~

Para resolver isso, temos que criar um teste de fato, fazendo uma chamada para nossa API usando o cliente de teste que definimos e testar novamente.

![alt text](image.png)

Com base nesse código, podemos observar as três fases:

__Fase 1 - Organizar (Arrange)__
Nesta primeira etapa, estamos preparando o ambiente para o teste. No exemplo, a linha com o comentário Arrange não é o teste em si, ela monta o ambiente para que o teste possa ser executado. Estamos configurando um client de testes para fazer a requisição ao app.

__Fase 2 - Agir (Act)__
Aqui é a etapa onde acontece a ação principal do teste, que consiste em chamar o Sistema Sob Teste (SUT). No nosso caso, o SUT é a rota /, e a ação é representada pela linha response = client.get('/'). Estamos exercitando a rota e armazenando sua resposta na variável response. É a fase em que o código de testes executa o código de produção que está sendo testado. Agir aqui significa interagir diretamente com a parte do sistema que queremos avaliar, para ver como ela se comporta.

__Fase 3 - Afirmar (Assert)__
Esta é a etapa de verificar se tudo correu como esperado. É fácil notar onde estamos fazendo a verificação, pois essa linha sempre tem a palavra reservada assert. A verificação é booleana, ou está correta, ou não está. Por isso, um teste deve sempre incluir um assert para verificar se o comportamento esperado está correto.

### Criando o repositório no git

[... deu muito ruim nessa parte do git, refazer outro projeto com cuidado. no próximo, testar sem definir "-b main"]

Criar um arquivo `.gitignore` para não adicionar o ambiente virtual e outros arquivos desnecessários no versionamento de código.
~~~shell
ignr -p python > .gitignore
~~~

Criar um novo repositório no Git local para versionar o código e definir a branch main como padrão. Caso não coloque a branch como main, está criando como master.
~~~shell
git init -b main
~~~


Para criar um repositório remoto no GitHub externo caso não exista, usar o comando abaixo:
~~~shell
gh repo create
~~~

#### Respostas do gh
~~~shell
- Create a new repository on GitHub from scratch # ok (Enter)
- mada_sync
- Projeto Final do curso do Dunossauro (FASTAPI)
- Public
- N
- N
- y
- GNU General Public License v3.0
- Y
- Y
~~~

Imagem abaixo com resultado da criação do repositório
![alt text](image-1.png)

__Atualizando o repositório - Commit__ <br>
Se for um novo repositório, deve-se adicionar o endereço de origem no local com o comando abaixo:

~~~shell
git remote add origin https://github.com/LuizPerciliano/mada_sync
~~~

Caso seja um repositório de desenvolvimento compartilhado, verificar se no repositório remoto há algo novo e pedir para baixar.
~~~shell
git pull
~~~

Verificar o status do repositório para ver as mudanças realizadas:
~~~shell
git status
~~~

Se tudo estiver ok, adicionar os arquivos, comitar e por fim enviar para o repositório remoto.
~~~shell
git add . 
git commit -m "Criado o projeto final do curso de FastAPI do Dunossauro"
git push --set-upstream origin main 
~~~

~~~shell
git push --force origin main # deu problema para subir, com isso foi
~~~

Conferindo se subiu tudo ok
~~~shell
git log
~~~

__Instalações se necessário__
~~~shell
Invoke-WebRequest -UseBasicParsing -Uri "https://raw.githubusercontent.com/pyenv-win/pyenv-win/master/pyenv-win/install-pyenv-win.ps1" -OutFile "./install-pyenv-win.ps1"; &"./install-pyenv-win.ps1"
~~~


## 03 Desenvolvendo a aplicação ⚠ :bowtie:

### Pydantic 
No universo de APIs e contratos de dados, especialmente ao trabalhar com Python, o Pydantic se destaca como uma ferramenta poderosa e versátil. Essa biblioteca, altamente integrada ao ecossistema Python, especializa-se na criação de schemas de dados e na validação de tipos. Com o Pydantic, é possível expressar schemas JSON de maneira elegante e eficiente através de classes Python, proporcionando uma ponte robusta entre a flexibilidade do JSON e a segurança de tipos de Python.

Por exemplo, o schema JSON {'message': 'Olá mundo!'}. Com o Pydantic, podemos representar esse schema na forma de uma classe Python chamada Message.

Para iniciar o desenvolvimento com schemas no contexto do FastAPI, podemos criar um arquivo chamado mada/schemas.py e definir a classe Message. Vale ressaltar que o Pydantic é uma dependência integrada do FastAPI (não precisa ser instalado), refletindo a importância dessa biblioteca no processo de validação de dados e na geração de documentação automática para APIs, como a documentação OpenAPI.

~~~shell
echo > mada/schemas.py
~~~

### Criando Rotas CRUD
1. criar o diretório de rotas
1. criar as rotas necessárias
1. criar o esquema do pydantic
1. criar o modelo
1. criar a base de dados
1. criar a segurança 
1. definir as configurações

~~~shell
mkdir mada/routers
~~~

~~~shell
echo > mada/routers/usuario.py
echo > mada/routers/livro.py
echo > mada/routers/autor.py
~~~

## Criando um banco de dados falso

### Modelo de dados
Arquivo `mada/schemas.py`.
~~~python
class UserSchema(BaseModel):
    username: str
    email: str
    password: str
~~~

## Validação e pydantic

Validação de email
Instalando + ferramentas de desenvolvimento 
~~~shell
poetry add "pydantic[email]"
~~~

# Configurando o Banco de Dados e Gerenciando Migrações com Alembic

Instalando + ferramentas de desenvolvimento 
~~~shell
poetry add sqlalchemy
~~~

~~~shell
poetry add pydantic-settings
~~~

Agora definiremos nosso modelo User. No diretório mada, crie um novo arquivo chamado models.py.

## Testando as Tabelas
Criaremos uma fixture para a conexão com o banco de dados chamada session no arquivo `tests/conftest.py`.

### Criando um Teste para a Nossa Tabela
Agora, no arquivo test_db.py, escreveremos um teste para a criação de um usuário. Este teste adiciona um novo usuário ao banco de dados, faz commit das mudanças, e depois verifica se o usuário foi devidamente criado consultando-o pelo nome de usuário. Se o usuário foi criado corretamente, o teste passa. Caso contrário, o teste falha, indicando que há algo errado com nossa função de criação de usuário.

~~~shell
echo > tests/test_db.py
~~~

#### Executando o teste

## Configuração do ambiente do banco de dados
~~~shell
echo > mada/settings.py
~~~

Agora, definiremos o DATABASE_URL no nosso arquivo de ambiente `.env`. Crie o arquivo na raiz do projeto e adicione a seguinte linha:
~~~shell
echo > .env
~~~

~~~shell
echo 'database.db' >> .gitignore
~~~

## Instalando o Alembic e Criando a Primeira Migração
~~~shell
poetry add alembic
~~~

Após a instalação do Alembic, precisamos iniciá-lo em nosso projeto. O comando de inicialização criará um diretório migrations e um arquivo de configuração alembic.ini:
~~~shell
alembic init migrations
~~~

### Criando uma migração automática
Com o Alembic devidamente instalado e iniciado, agora é o momento de gerar nossa primeira migração. Mas, antes disso, precisamos garantir que o Alembic consiga acessar nossas configurações e modelos corretamente. Para isso, faremos algumas alterações no arquivo migrations/env.py.

Para criar a migração, utilizamos o seguinte comando:
~~~shell
alembic revision --autogenerate -m "create users table"
~~~

### Analisando a migração automática
Vamos abrir e analisar o arquivo de migração `migrations/versions/f3577cecc9f1_create_users_table.py`.

Vamos acessar o console do sqlite e verificar se isso foi feito. Precisamos chamar sqlite3 nome_do_arquivo.db ou usar uma aplicativo que abre diversos tipos de banco de dados como o DBeaver:
~~~shell
sqlite3 database.db
~~~

Para aplicar as migrações, usamos o comando upgrade do CLI Alembic. O argumento head indica que queremos aplicar todas as migrações que ainda não foram aplicadas:
~~~shell
alembic upgrade head
~~~

# Integrando Banco de Dados a API
Para isso, criaremos a função get_session e também definiremos Session no arquivo `database.py`.
~~~shell
echo > .\mada\database.py
~~~

## Modificando o Endpoint POST /users

### Testando o Endpoint POST /users com Pytest e Fixtures
Alteraremos a nossa fixture client para substituir a função get_session que estamos injetando no endpoint pela sessão do banco em memória que já tínhamos definido para banco de dados.

### Integrando o Schema ao Model
ajustando o arquivo `mada/schemas.py` <p>

# Autenticação e Autorização com JWT
## Gerando tokens JWT
Para gerar tokens JWT, precisamos de duas bibliotecas extras: pyjwt e pwdlib. A primeira será usada para a geração do token, enquanto a segunda será usada para criptografar as senhas dos usuários. Para instalá-las, execute o seguinte comando no terminal:
~~~shell
poetry add pyjwt "pwdlib[argon2]"
~~~

Agora, criaremos uma função para gerar nossos tokens JWT. Criaremos um novo arquivo para gerenciar a segurança: security.py. Nesse arquivo iniciaremos a geração dos tokens:

~~~shell
echo > .\mada\security.py
~~~

## Testando a geração de tokens
~~~shell
echo > .\tests\test_security.py
~~~

## Modificando o endpoint de POST para encriptar a senha

## Criando um endpoint de geração do token
### Utilizando OAuth2PasswordRequestForm
~~~shell
poetry add python-multipart
~~~

# Refatorando a Estrutura do Projeto

## Criando Routers
Criaremos inicialmente uma nova estrutura de diretórios chamada routers dentro do seu projeto mada. Aqui, teremos subaplicativos dedicados a funções específicas, como gerenciamento de usuários e autenticação.

├── mada  
│  ├── app.py  
│  ├── database.py  
│  ├── models.py  
│  ├── routers  
│  │  ├── auth.py  
│  │  └── users.py  


#### Alteração no teste do token
Arquivo `tests/test_app.py`

## Reestruturando os arquivos de testes
#### Executando os testes
~~~shell
task test
~~~

# Tornando o sistema de autenticação robusto

## Testes para autenticação

### Testando a alteração de um usuário não autorizado

#### Criando modelos por demanda com factory-boy
O factory-boy é uma biblioteca que nos permite criar objetos de modelo de teste de forma rápida e fácil. Com ele, podemos criar uma "fábrica" de usuários que produzirá novos objetos de usuário sempre que precisarmos. Isso nos permite criar múltiplos usuários de teste com facilidade, o que é perfeito para nosso cenário atual.

~~~shell
poetry add --group dev factory-boy
~~~

Executando os testes abaixo em diante, o meu deu erro em alguns, logo, os testes seguintes não foi possível avaliar, verificar* (No final copiei tudo e vi que um arquivo precisava estar diferente, porém preciso rever sobre o token, pois isso está quebrando meus testes)

### Testes gerais
## Implementando o refresh do token

~~~shell
poetry add --group dev freezegun
~~~

## Estrutura inicial do código
Primeiro, criaremos um novo arquivo chamado todos.py no diretório de routers:
~~~shell
echo > mada\routers\livros.py
~~~

## Implementação da tabela no Banco de dados

## Criando a migração da nova tabela
~~~shell
alembic revision --autogenerate -m "create livro table"
~~~

Depois que a migração for criada, precisamos aplicá-la ao nosso banco de dados. Execute o comando alembic upgrade head para aplicar a migração.

~~~shell
alembic upgrade head
~~~

Agora que a migração foi aplicada, nosso banco de dados deve ter uma nova tabela de tarefas. Para verificar, você pode abrir o banco de dados com o comando sqlite3 database.db e depois executar o comando .schema para ver o esquema do banco de dados.

~~~shell
sqlite3 database.db
# ...
sqlite> .schema
# ...
~~~

### Endpoint de listagem

# Dockerizando a nossa aplicação e introduzindo o PostgreSQL
### pré-requisitos
Para este caso específico, tenho o Docker Desktop instalado no windows com o serviço sempre parado, logo, precisa iniciar o serviço do docker.

## Criando nosso Dockerfile

### Introduzindo o postgreSQL
#### Usar a Sintaxe Correta para cada SO Continuação de Linhas no PowerShell
~~~shell
# Sintaxe para windows
docker run `
    --name app_database_v2 `
    -e POSTGRES_USER=app_user `
    -e POSTGRES_DB=app_db `
    -e POSTGRES_PASSWORD=app_password `
    -p 5432:5432 `
    postgres
~~~

Com o banco de dados criado, que pode ser verificado no Docker Desktop, vamos testar acesso com uma ferramenta de BD, neste caso é o DBeaver.

Verificando o banco de dados docker via linha de comando:
~~~shell
docker ps -a -q # verifica os containers existentes inclusive os desligados
docker container start 6c13bcfa5e5f # iniciar o container
docker ps # verifica os containers iniciados
~~~

### Adicionando o suporte ao PostgreSQL na nossa aplicação
~~~shell
poetry add "psycopg[binary]"
~~~

Para ajustar a conexão com o PostgreSQL, modifique seu arquivo `.env` para incluir a seguinte string de conexão:
~~~shell
DATABASE_URL="postgresql+psycopg://app_user:app_password@localhost:5432/app_db"
~~~

Atualizar o banco de dados com suas respectivas tabelas com o comando abaixo.
~~~shell
alembic upgrade head
~~~

Abrir o Dbeaver para ver o banco de dados e as tabelas

Agora testar ver se a aplicação está rodando.
~~~shell
task run
~~~

## Resolvendo os testes que estavam rodando no sqlite
### Ajustando o arquivo `conftest.py`
Agora todos os meus testes passaram, mas dependem do banco de dados em pé.

### Testando com Docker
Existe uma biblioteca python que gerencia as dependências de containers externos
para que a aplicação seja executada. O TestContainers
~~~shell
poetry add --group dev testcontainers
~~~

## Parte 2 - Criando a imagem do nosso projeto
Criando na raiz o arquivo `Dockerfile`
~~~shell
echo > Dockerfile
~~~

Aqui está um exemplo de Dockerfile para criar o ambiente e executar nossa aplicação:
~~~docker
FROM python:3.12-slim
ENV POETRY_VIRTUALENVS_CREATE=false

WORKDIR app/
COPY . .

RUN pip install poetry

RUN poetry config installer.max-workers 10
RUN poetry install --no-interaction --no-ansi

EXPOSE 8000
CMD poetry run uvicorn --host 0.0.0.0 mada.app:app
~~~

## Criando a imagem
Para criar uma imagem Docker a partir do Dockerfile, usamos o comando docker build. O comando a seguir cria uma imagem chamada "mada":
~~~shell
docker build -t "mada" .
~~~

Então verificaremos se a imagem foi criada com sucesso usando o comando:
~~~shell
docker images
~~~

## Executando o container
~~~shell
docker run -it --name mada -p 8000:8000 mada:latest
~~~

~~~shell
curl http://localhost:8000
~~~

## Parte 3 - Simplificando nosso fluxo com docker-compose
Criação do compose.yaml
~~~shell
echo > compose.yaml
~~~

~~~yaml
services:
  fastzero_database:
    image: postgres
    volumes:
      - pgdata:/var/lib/postgresql/data
    environment:
      POSTGRES_USER: app_user
      POSTGRES_DB: app_db
      POSTGRES_PASSWORD: app_password
    ports:
      - "5432:5432"

  fastzero_app:
    image: mada_app
    entrypoint: ./entrypoint.sh
    build: .
    ports:
      - "8000:8000"
    depends_on:
      - mada_database
    environment:
      DATABASE_URL: postgresql+psycopg://app_user:app_password@mada_database:5432/app_db

volumes:
  pgdata:
~~~

~~~shell
docker-compose up
~~~

Caso dê algum erro de porta, derrube as imagens e crie o compose novamente.

## Implementando o Entrypoint
Criamos um script chamado entrypoint.sh que irá preparar nosso ambiente antes de a aplicação iniciar:
~~~shell
echo > entrypoint.sh
~~~

~~~shell
#!/bin/sh

# Executa as migrações do banco de dados
poetry run alembic upgrade head

# Inicia a aplicação
poetry run uvicorn --host 0.0.0.0 --port 8000 mada.app:app
~~~

## Adicionando o Entrypoint ao Docker Compose:

Incluímos o entrypoint no nosso serviço no arquivo compose.yaml, garantindo que esteja apontando para o script correto:

~~~shell
docker-compose up --build
~~~

Caso dê algum erro de execução no arquivo entrypoint, precisa dar poder de execução no mesmo.

~~~shell
docker-compose up -d mada_database
~~~

~~~shell
poetry add --group dev testcontainers
~~~


# Automatizando os testes com Integração Contínua (CI)
Criando os diretórios
~~~shell
mkdir .github
~~~

~~~shell
mkdir .github/workflows
~~~

~~~shell
echo > .github/workflows/pipeline.yaml
~~~

Configurando o workflow de CI
As configurações dos workflows no GitHub Actions são definidas em um arquivo YAML localizado em um path especificado pelo github no repositório .github/workflows/. Dentro desse diretório podemos criar quantos workflows quisermos. Iniciaremos nossa configuração com um único arquivo que chamaremos de pipeline.yaml:

Atualizando as dependencias de arquivos do projeto `.github/workflows/pipeline.yaml`

Atualizando o repositório e ver se executou os testes
~~~shell
git add .
git commit -m "Executando os testes no CI" 
git push 
~~~

## Configuração de variáveis de ambiente no Actions
Com erro nos testes precisa configurar as variáveis de ambiente usando o gh. No código abaixo ele vai criar segredo para todas as variáveis do arquivo.

~~~shell
gh secret set -f .env
~~~

Verificando os segredos
~~~shell
cat .env
~~~

Agora ir no repositório https://github.com/LuizPerciliano/madaxxx e atualizar "Re-run jobs" apertando o botão na aplicação.

Deu erro pois faltou atualizar os segredos no `.github/workflows/pipeline.yaml`

# Fazendo deploy no Fly.io
## O Fly.io
O Fly.io é uma plataforma de deploy que nos permite lançar nossas aplicações na nuvem e que oferece serviços para diversas linguagens de programação e frameworks como Python e Django, PHP e Laravel, Ruby e Rails, Elixir e Phoenix, etc.

~~~shell
flyctl version
~~~

Agora precisa auntenticar no flyctl


## Configurações para o deploy
Agora com o flyctl devidamente configurado. Podemos iniciar o processo de lançamento da nossa aplicação. O flyctl tem um comando específico para lançamento, o launch. Contudo, o comando launch é bastante interativo e ao final dele, o deploy da aplicação é executado. Colocar a memória de 512 para cima.
Para evitar o deploy no primeiro momento, pois ainda existem coisas para serem configuradas, vamos executá-lo da seguinte forma:

~~~shell
flyctl launch --no-deploy
~~~

Acessos:
- Admin URL: https://fly.io/apps/fastxxx


## Configuração dos segredos
Para que nossa aplicação funcione de maneira adequada, todas as variáveis de ambiente precisam estar configuradas no ambiente. O flyctl tem um comando para vermos as variáveis que já foram definidas no ambiente e também para definir novas. O comando secrets.

Para vermos as variáveis já configuradas no ambiente, podemos executar o seguinte comando:
~~~shell
flyctl secrets list
~~~

Uma coisa que podemos notar na resposta do secrets é que ele leu nosso arquivo .env e adicionou a variável de ambiente DATABASE_URL com base no postgres que foi criado durante o comando launch. Um ponto de atenção que devemos tomar nesse momento, é que a variável criada é iniciada com o prefixo postgres://. Para que o sqlalchemy reconheça esse endereço como válido, o prefixo deve ser alterado para postgresql+psycopg://. Para isso, usaremos a url fornecida pelo comando launch e alterar o prefixo.

Desta forma, podemos registar a variável de ambiente DATABASE_URL novamente. Agora com o valor correto:

~~~shell
flyctl secrets set ALGORITHM="HS256"
~~~

~~~shell
flyctl secrets set ACCESS_TOKEN_EXPIRE_MINUTES=300
~~~

Para secret_key, tem que ter uma ou gerar. Como gerar uma?

~~~shell
python
import secrets
secrets.token_hex(32)
~~~

Com o comando acima será gerado um segredo, basta copiar no comando abaixo e voilá.

~~~shell
flyctl secrets set SECRET_KEY="your-secret-key"
~~~


Podemos registar a variável de ambiente DATABASE_URL novamente, agora a correta fornecida pelo fly.io. Agora com o valor correto:


~~~shell
flyctl secrets set DATABASE_URL="postgresql+psycopg://postgres:nome-user-do-app:senhageradanofly@nome-da-maquina-db.flycast:5432/nome-app”
~~~

## Deploy da aplicação
Para efetuarmos o deploy da aplicação, podemos usar o comando deploy doflyctl. Uma coisa interessante nessa parte do processo é que o Fly pode fazer o deploy de duas formas:

Copiar seus arquivos e fazer o build do docker na nuvem;
Você pode fazer o build localmente e subir apenas o container para um repositório disponível no Fly.
Optaremos por fazer o build localmente para não serem alocadas duas máquinas em nossa aplicação1. Para executar o build localmente usamos a flag --local-only.

O Fly sobre duas instâncias por padrão da nossa aplicação para melhorar a disponibilidade do app. Como vamos nos basear no uso gratuito, para todos poderem executar o deploy, adicionaremos a flag --ha=false ao deploy. Para desativamos a alta escalabilidade:

~~~shell
fly deploy --local-only --ha=false
~~~

Verificando o log da aplicação.
~~~shell
fly logs -a mada
ou 
fly logs -a mada | tl # tem que ter a biblioteca tl instalada
ou site app
~~~

## Migrations
Agora que nosso container já está em execução no fly, podemos executar o comando de migração dos dados, pois ele está na mesma rede do postgres configurado pelo Fly2. Essa conexão é feita via SSH e pode ser efetuada com o comando ssh do flyctl.

Podemos fazer isso de duas formas, acessando efetivamente o container remotamente ou enviando somente um comando para o Fly. Optarei pela segunda opção, pois ela não é interativa e usará somente uma única chamada do shell. Desta forma:

Entrando na máquina no fly.io
~~~shell
flyctl ssh console
~~~

Colocar no dockeringone:
tests
imagens

Dentro do console é possível rodar a migração (alembic), pois as tabelas não foram criadas.

~~~shell
alembic upgrade head
~~~

ou rodar diretamente o comando abaixo:

~~~shell
flyctl ssh console -a mada -C "poetry run alembic upgrade head"
~~~

## Atualizando o repositório - Commit
Caso seja um repositório de desenvolvimento compartilhado, verificar se no repositório remoto há algo novo e pedir para baixar.
~~~shell
git pull
~~~

Verificar o status do repositório para ver as mudanças realizadas:
~~~shell
git status
~~~

Se tudo estiver ok, adicionar os arquivos, comitar e por fim enviar para o repositório remoto.
~~~shell
git add . 
git commit -m "Adicionando arquivos gerados pelo Fly"
git push --set-upstream origin main 
~~~

Conferindo se subiu tudo ok
~~~shell
git log