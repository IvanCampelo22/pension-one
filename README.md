# Teste BrasilPrev | Backe-End


### Conteúdo

1. Tecnologias Usadas
2. Executando via arquivo Docker Compose
3. Como executar o projeto no linux
4. Se sua distribuição adotar o PEP 668 
5. Observação sobre execução do projeto sem o Docker
6. Como fazer migrações no banco de dados
7. Possíveis problemas
8. Notas sobre o teste


## Tecnologias Usadas

- Python
- Fastapi
- Postgresql
- Docker


## Executando via arquivo Docker Compose (Recomendado)

1. Com o DockerCompose basta executar apenas um comando 

> sudo docker compose up 

2. Caso necessário refazer a imagem por conta de alguma alteração 

> sudo docker compose up --build

3. Teste docker compose 

>  http://0.0.0.0:8080/docs

* Obs:

1. Para zerar o banco de dados do container basta digitar: 

> sudo docker compose down

> sudo docker compose down -v



## Como executar o projeto no linux

1. Ir até a pasta do projeto e criar a virualenv

> virtualenv venv

2. Ative a virtualenv

> source venv/bin/activate

3. Instale as dependencias

> pip install -r requirements.txt

4. Na raiz do projeto, onde estiver o arquivo main.py execute: 

> python main.py

* obs:

> para rodar o projeto localmente sem o docker, é importante que no arquivo alembic.ini e no arquivo session.py estejam com a url do sqlalchemy com o host -> localhost. 

> por padrão está -> db. 

> db é o host do container

> Os testes estão rodando de forma automática durante a iniciação do container


### Se sua distribuição adotar o PEP 668 

1. Ir até a pasta do projeto e criar a virualenv
> python3 -m venv .venv

2. Ative a virtualenv
> source .venv/bin/activate

3. Instale as dependencias

> python3 -m pip install -r requirements.txt

4. Na raiz do projeto, onde estiver o arquivo main.py execute: 

> python3 -m main

* Teste local

> http://127.0.0.1:8080/docs


## Como fazer migrações no banco de dados

1. Execute o comando para criar o arquivo de migração no versions

> alembic revision -m "<nome-da-migraçao>"

2. Depois de criada a migração execute

> alembic upgrade head --sql

> alembic upgrade head


## Possíveis problemas

1. O docker não encontrar permissões para executar o start.sh

> Na raiz do projeto onde está o start.sh execute o comando (que também está Dockerfile): chmod +x start.sh

2. Credenciais no DockerCompose

> No arquivo docker compose está as credenciais padrão de meu banco de dados local, caso ocorra problema, basta atualiza-las para as suas credenciais


# Notas sobre o teste 

## Autenticação 

> A princípio, seria necessário adicionar autenticação. Separando administrador e usuários comuns, 
setando permissões nos endpoints.


## Celery

> Também seria interessante criar tasks utilizando o celery com o intuito de fazer verificações sobre os dados do cliente,
se está tudo de acordo com as diretrizes da empresa, também podendo ocorrer alterações no status de atividade
da conta do cliente.  


## Envio de emails

> Envio de e-mails. Por exemplo, quando o cliente garantir um plano, um e-mail é enviado para o endereço cadastrado,
notificando que o plano foi adquirido com sucesso. Ou, caso a data de expiração se aproxime, 
com uma task do celery agendada fazendo verificação constante, 
seria enviado um e-mail informando que seria necessário uma renovação.  


## Validação

> Validar de uma forma mais depurada os campos que vem do cliente-side, como cpf, emails e valores


## SoftDelete

Metódo onde os registros não são apagados permanentemente do banco de dados, no entanto, tem seu status alterado. Por exemplo: is_active=False 


## Obs:

> As credenciais estão expostas para facilitar a execução do projeto e também porque 
o código não vai ser hospedado em lugar nenhum. 
Tenho ciência de parâmetros de segurança e conhecimento sobre a manipulação das variáveis de ambiente