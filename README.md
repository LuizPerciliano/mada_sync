# Projeto final 🎉 do Curso de FastAPI do ZERO com o 🦖 Dunossauro
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





3. ignr


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
pipx ensurepath # executar após poetry instalado, fechar e reabrir o terminal

cd C:\projetos\projetos-GIT\

# Criando o projeto
poetry new mada
cd mada
pyenv local 3.12.5 # dizer ao pyenv qual versão do python será usada nesse diretório
poetry install # Cria o ambiente virtual (venv)
~~~




*********************

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

[... deu muito ruim nessa parte do git, refazer outro projeto com cuidado]

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

Conferindo se subiu tudo ok
~~~shell
git log
~~~







~~~shell
git pull origin main
~~~

~~~shell
git add .
~~~

~~~shell
git commit -m "Configuração inicial do projeto"
~~~

~~~shell
git push
~~~

<!-- https://github.com/markdown-templates/markdown-emojis -->
Deu muito ruim nessa parte do git, refazer outro projeto com cuidado e anotar corretamente os passos ⚠ :bowtie:















### Instalações se necessário
~~~shell
Invoke-WebRequest -UseBasicParsing -Uri "https://raw.githubusercontent.com/pyenv-win/pyenv-win/master/pyenv-win/install-pyenv-win.ps1" -OutFile "./install-pyenv-win.ps1"; &"./install-pyenv-win.ps1"
~~~


~~~shell
pipx install ignr
~~~

---











# Aula 02 Introdução ao desenvolvimento WEB

## Usando o fastapi na rede local
~~~shell
fastapi dev fast_zero_v2/app.py --host 0.0.0.0
~~~

ou com o comando abaixo para o mesmo resultado
~~~shell
task run --host 0.0.0.0
~~~

Assim, você pode acessar a aplicação de outro computador na sua rede usando o endereço IP da sua máquina.

Descobrindo o ip local no Windows
~~~shell
ipconfig
~~~

Descobrindo o seu endereço local usando python pelo interpretador
~~~shell
python
~~~

~~~python
import socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
s.getsockname()[0]
~~~


Agora basta acessar a aplicação pelo endereço: http://192.168.0.5:8000/, ficando acessível também por outras máquinas dentro dessa rede, assim como o celular.

Criando novo arquivo para testes e aprendizado de endpoints.
~~~shell
type nul > fast_zero_v2/aula_00.py
~~~

Abrir o arquivo `fast_zero_v2/aula_00.py` e copiar o script abaixo.
~~~python
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()


@app.get('/')
def read_root():
    return {'message': 'Olá Mundo!'}
~~~

Executar o arquivo específico.
~~~shell
fastapi dev fast_zero_v2/aula_00.py
~~~

## Pydantic
~~~shell
echo > fast_zero_v2/schemas.py
~~~


# Aula 03 Estruturando o Projeto e Criando Rotas CRUD
## Implementando endpoints

### Rota do POST
Arquivo `fast_zero_v2/app.py`.
~~~python
@app.post('/users/', status_code=HTTPStatus.CREATED)
def create_user():
    ...
~~~

### Modelo de dados
Arquivo `fast_zero_v2/schemas.py`.
~~~python
class UserSchema(BaseModel):
    username: str
    email: str
    password: str
~~~

<!-- ... desenvolvendo e incrementando o projeto ... estudar mais esta aula]-->

## Validação e pydantic

Validação de email
Instalando + ferramentas de desenvolvimento 
~~~shell
poetry add "pydantic[email]"
~~~

## Criando um banco de dados falso


### Não se repita (DRY)
Arquivo `tests/conftest.py`.

~~~shell
echo > tests/conftest.py
~~~

## Implementando a Rota GET


## Implementando a Rota PUT

## Implementando a Rota DELETE

# Aula 04 Configurando o Banco de Dados e Gerenciando Migrações com Alembic

Instalando + ferramentas de desenvolvimento 
~~~shell
poetry add sqlalchemy
~~~

~~~shell
poetry add pydantic-settings
~~~

Agora definiremos nosso modelo User. No diretório fast_zero, crie um novo arquivo chamado models.py e incluiremos o seguinte código no arquivo:

~~~shell
echo > fast_zero_v2/models.py
~~~

## Testando as Tabelas
Criaremos uma fixture para a conexão com o banco de dados chamada session no arquivo `tests/conftest.py`.

### Criando um Teste para a Nossa Tabela
Agora, no arquivo test_db.py, escreveremos um teste para a criação de um usuário. Este teste adiciona um novo usuário ao banco de dados, faz commit das mudanças, e depois verifica se o usuário foi devidamente criado consultando-o pelo nome de usuário. Se o usuário foi criado corretamente, o teste passa. Caso contrário, o teste falha, indicando que há algo errado com nossa função de criação de usuário.

~~~shell
echo > tests/test_db.py
~~~

#### Executando o teste

~~~shell
exit
~~~

~~~shell
task format
~~~

~~~shell
task test
~~~

O ideal é ter pelo menos dois terminais ativos, um para rodar a aplicação e outro para os testes e demais comandos.
~~~shell
task run
~~~

## Configuração do ambiente do banco de dados
~~~shell
echo > fast_zero_v2/settings.py
~~~


Agora, definiremos o DATABASE_URL no nosso arquivo de ambiente .env. Crie o arquivo na raiz do projeto e adicione a seguinte linha:
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

~~~shell
code migrations/versions/f3577cecc9f1_create_users_table.py
~~~

Vamos acessar o console do sqlite e verificar se isso foi feito. Precisamos chamar sqlite3 nome_do_arquivo.db ou usar uma aplicativo que abre diversos tipos de banco de dados como o DBeaver:
~~~shell
sqlite3 database.db
~~~

Para aplicar as migrações, usamos o comando upgrade do CLI Alembic. O argumento head indica que queremos aplicar todas as migrações que ainda não foram aplicadas:
~~~shell
alembic upgrade head
~~~

Agora, se examinarmos nosso banco de dados novamente:

## Commit
Primeiro, verificaremos o status do nosso repositório para ver as mudanças que fizemos:
~~~shell
git status
~~~

~~~shell
git add . 
~~~

~~~shell
git commit -m "Adicionada a primeira migração com Alembic. Criada tabela de usuários."
~~~

~~~shell
git push
~~~


# Aula 05 Integrando Banco de Dados a API
Para isso, criaremos a função get_session e também definiremos Session no arquivo `database.py`.
~~~shell
echo > .\fast_zero_v2\database.py
~~~

## Modificando o Endpoint POST /users

### Testando o Endpoint POST /users com Pytest e Fixtures
Alteraremos a nossa fixture client para substituir a função get_session que estamos injetando no endpoint pela sessão do banco em memória que já tínhamos definido para banco de dados.


## Modificando o Endpoint GET /users

### Testando o Endpoint GET /users

### Criando uma fixture para User

### Integrando o Schema ao Model
ajustando o arquivo `fast_zero/schemas.py` <p>

## Modificando o Endpoint PUT /users

### Adicionando o teste do PUT

## Modificando o Endpoint DELETE /users

### Adicionando testes para DELETE


## Atualizando o repositório - Commit
Primeiro, verificar o status do repositório para ver as mudanças realizadas:
~~~shell
git status
~~~

Se tudo estiver ok, adicionar os arquivos, comitar e por fim enviar para o repositório remoto.
~~~shell
git add . 
git commit -m "Revisando as aulas com um novo projeto criado.Atualizando endpoints para usar o banco de dados real."
git push
~~~



# Aula 06 Autenticação e Autorização com JWT
## Gerando tokens JWT
Para gerar tokens JWT, precisamos de duas bibliotecas extras: pyjwt e pwdlib. A primeira será usada para a geração do token, enquanto a segunda será usada para criptografar as senhas dos usuários. Para instalá-las, execute o seguinte comando no terminal:
~~~shell
poetry add pyjwt "pwdlib[argon2]"
~~~

Agora, criaremos uma função para gerar nossos tokens JWT. Criaremos um novo arquivo para gerenciar a segurança: security.py. Nesse arquivo iniciaremos a geração dos tokens:

~~~shell
echo > .\fast_zero_v2\security.py
~~~

## Testando a geração de tokens
~~~shell
echo > .\tests\test_security.py
~~~

## Modificando o endpoint de POST para encriptar a senha

### Sobre o teste da POST /users/


## Modificando o endpoint de atualização de usuários

## Criando um endpoint de geração do token
### Utilizando OAuth2PasswordRequestForm
~~~shell
poetry add python-multipart
~~~

### Criando um endpoint de geração do token

### Testando /token

## Protegendo os Endpoints

### Aplicação da proteção ao endpoint

## Atualizando os Testes



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
git commit -m "Revisando as aulas com um novo projeto criado. Aula 06. Protege os endpoints PUT e DELETE com autenticação"
git push
~~~




# Aula 07 Refatorando a Estrutura do Projeto

## Criando Routers
Criaremos inicialmente uma nova estrutura de diretórios chamada routers dentro do seu projeto fast_zero. Aqui, teremos subaplicativos dedicados a funções específicas, como gerenciamento de usuários e autenticação.

├── fast_zero  
│  ├── app.py  
│  ├── database.py  
│  ├── models.py  
│  ├── routers  
│  │  ├── auth.py  
│  │  └── users.py  

### Implementando um Router para Usuários
~~~shell
mkdir routers
~~~

~~~shell
echo > fast_zero_v2\routers\users.py
~~~

### Criando um router para Auth
~~~shell
echo > fast_zero_v2\routers\auth.py
~~~


O comando abaixo deu erro, verificar*
~~~shell
task serve
~~~

#### Alteração no teste do token
Arquivo `tests/test_app.py`



## Plugando as rotas em app

## Reestruturando os arquivos de testes

### Ajustando os testes para Auth
~~~shell
echo > tests\test_auth.py
~~~


### Ajustando os testes para User
~~~shell
echo > tests\test_users.py
~~~


#### Executando os testes
~~~shell
task test
~~~

## Refinando a Definição de Rotas com Annotated

## Movendo as constantes para variáveis de ambiente

### Adicionando as constantes a Settings

### Removendo as constantes do código

## Testando se tudo funciona
~~~shell
task test
~~~

erro, meu Swagger não aparece usuários, verificar*
![alt text](image-2.png)

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
git commit -m "Refatorando estrutura do projeto: Criado routers para Users e Auth; movido constantes para variáveis de ambiente." 
git push 
~~~



# Aula 08 Tornando o sistema de autenticação robusto

## Testes para autenticação

### Testando a alteração de um usuário não autorizado

#### Criando modelos por demanda com factory-boy

O factory-boy é uma biblioteca que nos permite criar objetos de modelo de teste de forma rápida e fácil. Com ele, podemos criar uma "fábrica" de usuários que produzirá novos objetos de usuário sempre que precisarmos. Isso nos permite criar múltiplos usuários de teste com facilidade, o que é perfeito para nosso cenário atual.

~~~shell
poetry add --group dev factory-boy
~~~

Executando os testes abaixo em diante, o meu deu erro em alguns, logo, os testes seguintes não foi possível avaliar, verificar* (No final copiei tudo e vi que um arquivo precisava estar diferente, porém preciso rever sobre o token, pois isso está quebrando meus testes)

![alt text](image-3.png)


### Testando o DELETE com o usuário errado


### Testando a expiração do token


### Testando o usuário não existente e senha incorreta


#### Testando a exceção para um usuário inexistente


#### Testando a exceção para uma senha incorreta



## Implementando o refresh do token



~~~shell
poetry add --group dev freezegun
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
git commit -m "Implementando o refresh do token e testes de autorização." 
git push --set-upstream origin main 
~~~


# Aula 09 Criando Rotas CRUD para Gerenciamento de Tarefas em FastAPI
## Criando a migração da nova tabela

- Criação das rotas para as operações CRUD das tarefas
- Fazer com só o usuário dono da tarefa possa acessar e modificar suas tarefas
- Escrita e execução dos testes para cada operação das tarefas

## Estrutura inicial do código
Primeiro, criaremos um novo arquivo chamado todos.py no diretório de routers:
~~~shell
echo > fast_zero_v2\routers\todos.py
~~~

## Implementação da tabela no Banco de dados

### Testando as novas implementações do banco de dados

como verificar o coverage html?*


## Schemas para Todos


## Endpoint de criação

### Testando o endpoint de criação
~~~shell
echo > .\tests\test_todos.py
~~~

Para executar este teste, você deve usar o comando abaixo no terminal:
~~~shell
task test tests/test_todos.py
~~~

Deu erro no teste, verificar

![alt text](image-4.png)


## Criando a migração da nova tabela
~~~shell
alembic revision --autogenerate -m "create todos table"
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

## Endpoint de listagem

### Criando uma factory para simplificar os testes

#### Testes para esse endpoint

#### Testando a Paginação

#### Testando o Filtro por Título

#### Testando o Filtro por Descrição

#### Testando o Filtro por Estado

#### Testando a Combinação de Filtros de Estado, Título e Descrição

#### Executando os testes
~~~shell
task format  
task test tests/test_todos.py  
~~~

Meu teste deu erro, depois voltar aqui e rever o código*


## Endpoint de Alteração

### Testes para o Endpoint de Alteração
~~~shell
task format  
task test tests/test_todos.py  
~~~

Meu teste deu erro, depois voltar aqui e rever o código*

## Endpoint de Deleção

### Testes para o Endpoint de Deleção

~~~shell
task format  
task test tests/test_todos.py  
~~~

Meu teste deu erro, depois voltar aqui e rever o código* (não dá para executar todas as aulas sem o vídeo, essa aqui por exemplo cria o arquivo `tests.factories` e não vi no documento)
~~~shell
echo > .\tests\factories.py
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
git commit -m "Implementado os endpoints de tarefas." 
git push --set-upstream origin main 
~~~



<!--
Rememorar como é para se autenticar e talvez por isso não aparece o swgger com [users] usuários*
-->

# Aula 10 Dockerizando a nossa aplicação e introduzindo o PostgreSQL
<!-- Não assisti o vídeo dessa aula 
https://www.youtube.com/watch?v=bpBbbUgmdMs&list=PLOQgLBuj2-3IuFbt-wJw2p2NiV9WTRzIP
-->
Objetivos da aula:

- Compreender os conceitos básicos do Docker
- Entender como criar uma imagem Docker para a nossa aplicação FastAPI
- Aprender a rodar a aplicação utilizando Docker
- Introduzir o conceito de Docker Compose para gerenciamento de múltiplos contêineres
- Aprender o que é um Dockerfile e sua estrutura
- Entender os benefícios e motivos da mudança de SQLite para PostgreSQL

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

#### Comando para Unix/Linux
~~~shell
docker run \
    --name app_database_v2 \ #nome da imagem docker
    -e POSTGRES_USER=app_user \
    -e POSTGRES_DB=app_db \ #nome do banco de dados
    -e POSTGRES_PASSWORD=app_password \
    -p 5432:5432 \
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

Testando, abrir a aplicação e tentar criar um usuário no http://127.0.0.1:8000/docs
Caso tenha sido criando tentar logar com o usuário criado.

{
  "username": "user@example.com",
  "password": "string"
}

Agora tentar criar um todo e se tudo ok, ir novamente no banco de dados para ver se também salvou em base de dados.

Oh Glória, tudo ok por aqui até o momento.


## Resolvendo os testes que estavam rodando no sqlite
<!-- Vídeo Aula 10 - 00:27:09 -->

### Ajustando o arquivo `conftest.py`
Agora todos os meus testes passaram, mas dependem do banco de dados em pé.


### Testando com Docker
Existe uma biblioteca python que gerencia as dependências de containers externos
para que a aplicação seja executada. O TestContainers
~~~shell
poetry add --group dev testcontainers
~~~

Ajustando programa ... e testando novamente ...
~~~shell
task test -s
~~~


## Parte 2 - Criando a imagem do nosso projeto
<!-- Vídeo Aula 10 - 00:51:28 -->

Criando na raiz o arquivo `Dockerfile`
~~~shell
echo > Dockerfile
~~~


Aqui está um exemplo de Dockerfile para criar o ambiente e executar nossa aplicação:
~~~shell
FROM python:3.12-slim
ENV POETRY_VIRTUALENVS_CREATE=false

WORKDIR app/
COPY . .

RUN pip install poetry

RUN poetry config installer.max-workers 10
RUN poetry install --no-interaction --no-ansi

EXPOSE 8000
CMD poetry run uvicorn --host 0.0.0.0 fast_zero_v2.app:app
~~~

## Criando a imagem
Para criar uma imagem Docker a partir do Dockerfile, usamos o comando docker build. O comando a seguir cria uma imagem chamada "fast_zero":
~~~shell
docker build -t "fast_zero_v2" .
~~~

No terminal funcionou mas no VSCODe não, deu acesso negado em algum arquivo, e o terminal está como adm.


Então verificaremos se a imagem foi criada com sucesso usando o comando:
~~~shell
docker images
~~~

## Executando o container
~~~shell
docker run -it --name fastzeroappv2 -p 8000:8000 fast_zero_v2:latest
~~~

~~~shell
curl http://localhost:8000
~~~

## Parte 3 - Simplificando nosso fluxo com docker-compose
Criação do compose.yaml
~~~shell
echo > compose.yaml
~~~

~~~shell
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
    image: fastzero_app_v2
    entrypoint: ./entrypoint.sh
    build: .
    ports:
      - "8000:8000"
    depends_on:
      - fastzero_database
    environment:
      DATABASE_URL: postgresql+psycopg://app_user:app_password@fastzero_database:5432/app_db

volumes:
  pgdata:
~~~

~~~shell
docker-compose up
~~~

Caso dê algum erro de porta, derrube as imagens e crie o compose novamente.

<!-- Vídeo Aula 10 - 01:24:41 o meu está dando erro com portas já usadas-->

![alt text](image-5.png)

Extra - estudar isso depois
~~~shell
poetry add ... tolong #biblioteca que auxilia olhar e pesquisar os logs
~~~


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
poetry run uvicorn --host 0.0.0.0 --port 8000 fast_zero.app:app
~~~


## Adicionando o Entrypoint ao Docker Compose:

Incluímos o entrypoint no nosso serviço no arquivo compose.yaml, garantindo que esteja apontando para o script correto:

~~~shell
docker-compose up --build
~~~

Caso dê algum erro de execução no arquivo entrypoint, precisa dar poder de execução no mesmo.

~~~shell
docker-compose up -d fastzero_database
~~~

~~~shell
poetry add --group dev testcontainers
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
git commit -m "Dokerizando o projeto." 
git push --set-upstream origin main 
~~~

Conferindo se subiu tudo ok
~~~shell
git log
~~~



# Aula 11 Automatizando os testes com Integração Contínua (CI)
<!-- https://fastapidozero.dunossauro.com/11/ 
https://github.com/features/actions
-->
<!-- Minha aplicação não está rodando por erro de porta, verificar 
qd for iniciar a aula, reiniciar a máquina.
-->

## Preparando o ambiente
<!-- No projeto do duno tem o diretório `.git` que não sei de onde é.
-->
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
~~~shell
name: Pipeline
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - name: Instalar o python
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'
~~~

Atualizando o repositório.
~~~shell
git add . 
git commit -m "Instalação do Python no CI" 
git push 
~~~

Atualizando as dependencias de arquivos do projeto `.github/workflows/pipeline.yaml`

Atualizando o repositório e ver se executou os testes
~~~shell
git add .\.github\workflows\pipeline.yaml
git commit -m "Executando os testes" 
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

Agora ir no repositório https://github.com/LuizPerciliano/fast_zero_sync_v2/actions/runs/10501322321/job/29091123627 e atualizar "Re-run jobs" apertando o botão na aplicação.

Deu erro pois faltou atualizar os segredos no `.github/workflows/pipeline.yaml`

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
git commit -m "Adicionando as variáveis de ambiente para o CI"
git push --set-upstream origin main 
~~~

Verificar o job correto se está ok.

## Dando um up nos testes antes do commit remoto
Ferramenta: https://github.com/nektos/act

Com o uso da ferramenta acima, até melhorando a visualização dos logs do git para casos de muitos ajustes de erros.

Pesquisar sobre o act e implantar.



# Aula 12 Fazendo deploy no Fly.io
<!-- https://fastapidozero.dunossauro.com/12/ 
https://youtu.be/Xt7A5QnsSeo?list=PLOQgLBuj2-3IuFbt-wJw2p2NiV9WTRzIP
https://fly.io/

No projeto do duno tem o diretório `.git` que não sei de onde é.

Descobrir o que é sentry
-->

## O Fly.io
O Fly.io é uma plataforma de deploy que nos permite lançar nossas aplicações na nuvem e que oferece serviços para diversas linguagens de programação e frameworks como Python e Django, PHP e Laravel, Ruby e Rails, Elixir e Phoenix, etc.

### Flyclt
Uma das formas de interagir com a plataforma é via uma aplicação de linha de comando disponibilizada pelo Fly, o flyctl.

Instalando no windows: https://fly.io/docs/flyctl/install/
~~~shell
pwsh -Command "iwr https://fly.io/install.ps1 -useb | iex"
~~~

Provavelmente será necessário reiniciar o terminal, logo após teste o comando abaixo:
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

A pergunta feita ao final dessa seção Do you want to tweak these settings before proceeding? pode ser traduzida como: Você deseja ajustar essas configuração antes de prosseguir?. Diremos que sim, digitando Y e em seguida Enter.

Após configurar similar a imagem a abaixo, selecione confirma:
![alt text](image-6.png)


Acessos:
- Admin URL: https://fly.io/apps/fast-zero-777


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


Uma coisa que podemos notar na resposta do secrets é que ele leu nosso arquivo .env e adicionou a variável de ambiente DATABASE_URL com base no postgres que foi criado durante o comando launch. Um ponto de atenção que devemos tomar nesse momento, é que a variável criada é iniciada com o prefixo postgres://. Para que o sqlalchemy reconheça esse endereço como válido, o prefixo deve ser alterado para postgresql+psycopg://. Para isso, usaremos a url fornecida pelo comando launch e alterar o prefixo.

Desta forma, podemos registar a variável de ambiente DATABASE_URL novamente. Agora com o valor correto:


<!-- flictl no notion -->
~~~shell
flyctl secrets set DATABASE_URL="postgresql+psycopg://postgres:nome-user-do-app:senhageradanofly@nome-da-maquina-db.flycast:5432/nome-bd-da-app”
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
fly logs -a fast-zero-v2
ou 
fly logs -a fast-zero-v2 | tl # tem que ter a biblioteca tl instalada
ou site app
~~~

<!--
URL ADM:
https://fly.io/apps/fast-zero-v2/monitoring

APP:
https://fast-zero-v2.fly.dev/

até o minuto 00:57 ok, mas o meu não

-->

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
flyctl ssh console -a fast-zero-v2 -C "poetry run alembic upgrade head"
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
~~~


# Aula 13 Despedida e próximos passos
<!-- https://youtu.be/33vn7dxg37U?list=PLOQgLBuj2-3IuFbt-wJw2p2NiV9WTRzIP 
https://fastapidozero.dunossauro.com/13/
-->
Revisão geral e um tapa no readme.

# Projeto final
<!-- https://fastapidozero.dunossauro.com/14/
-->

Em andamento ...
---

# Final da Aplicação
## Passos para subir a aplicação e ou ajustar o projeto após tudo finalizado 

~~~shell
# se tiver docker, iniciar o serviço
  # Get-Service -Name com.docker.service # verifica o seviço
  # Start-Service -Name com.docker.service
  # iniciar as máquinas necessárias

Start-Service -Name com.docker.service
docker start app_database_v2
# Verficar se tem algo a comitar ou puxar do repositório remoto
clear
cd C:\projetos\projetos-GIT\fast_zero_v2\ 
poetry shell
# codifica
# testa
# comita
# deploy
---