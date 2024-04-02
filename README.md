# Desafio Freelaw

Este documento mostra como configurar e executar o projeto abaixo.

## Instalação

Certifique-se de ter o Python e o Poetry instalados em seu sistema.

1. Clone este repositório:

   ```bash
   git clone https://github.com/fagnerpsantos/freelaw.git
   ```

2. Navegue até o diretório do projeto:

   ```bash
   cd event-api
   ```

3. Instale as dependências usando Poetry:

   ```bash
   poetry install
   ```
   

## Configuração do arquivo .env

Para gerenciar as variáveis de ambiente do seu projeto, você pode criar um arquivo `.env`. Este arquivo será usado para armazenar informações sensíveis e configurações específicas do ambiente, como chaves de API, segredos de autenticação e configurações de banco de dados.

1. Crie um arquivo `.env` na raiz do seu projeto.

2. Adicione as variáveis de ambiente necessárias ao arquivo `.env`, seguindo o formato `NOME_DA_VARIAVEL=valor`.

   Por exemplo:

   ```plaintext
   DEBUG=True
   SECRET_KEY=teste
   DATABASE_URL=sqlite:///db.sqlite3
   CELERY_BROKER_URL=redis://localhost:6379/0
   EMAIL_HOST_USER=seuemail@mail.com
   EMAIL_HOST_PASSWORD=host_password
   EMAIL_USE_TLS=True
   ```

   Certifique-se de substituir os valores de exemplo pelos valores específicos do seu projeto.

## Configuração do Banco de Dados
1. Execute as migrações do Django para criar o esquema do banco de dados:

   ```bash
   poetry run python manage.py migrate
   ```

## Configuração do Celery

1. Certifique-se de ter um broker (por exemplo, RabbitMQ ou Redis) instalado e em execução.

3. Inicie o Celery worker:

   ```bash
   poetry run celery -A event_api worker -l info
   ```

## Executando o Servidor Django

Agora que o banco de dados e o Celery estão configurados, você pode iniciar o servidor Django:

```bash
poetry run python manage.py runserver
```

O servidor estará acessível em `http://127.0.0.1:8000/`.

## Documentação dos endpoints

Todos os endpoints estão documentados em `/swagger/`. Basicamente a API funciona da seguinte maneira:

1. Primeiro é necessário criar um evento com uma requisição do tipo `POST` para a rota `/api/events`
2. Depois, com o evento criado, basta criar um usuário para se registrar utilizando uma requisição do tipo `POST` para a rota `/api/users/`
3. Agora, basta logar com o usuário enviando uma requisição do tipo `POST` para a rota `/token`
4. Por fim, para realizar a inscrição, basta enviar esse token no `header Authorization` da requisição passando o ID do evento que o usuário será inscrito.

Ao final desse processo, o usuário receberá um email confirmando sua inscrição no evento.

### Documentação detalhada dos endpoints

# Documentação do Endpoint CRUD de Events

## Funcionamento Geral

O endpoint CRUD de events permite realizar operações básicas de criação, leitura, atualização e exclusão de events.

## Métodos Disponíveis

1. **POST /api/events/**: Cria um novo event.
2. **GET /api/events/{id}**: Obtém os detalhes de um event específico.
3. **PUT /api/events/{id}**: Atualiza os detalhes de um event existente.
4. **DELETE /api/events/{id}**: Exclui um event.

## Como Executar Cada Método

1. **POST - Criar um Novo Event**: Envie uma requisição POST para `/api/events/` com os dados do event no corpo da requisição.
2. **GET - Obter Detalhes de um Event**: Envie uma requisição GET para `/api/events/{id}` para obter os detalhes de um event específico.
3. **PUT - Atualizar um Event Existente**: Envie uma requisição PUT para `/api/events/{id}` com os novos dados do event no corpo da requisição.
4. **DELETE - Excluir um Event**: Envie uma requisição DELETE para `/api/events/{id}` para excluir um event.


# Documentação do Endpoint CRUD de Usuários

## Funcionamento Geral

O endpoint CRUD de usuários permite realizar operações básicas de criação, leitura, atualização e exclusão de usuários.

## Métodos Disponíveis

1. **POST /api/users/**: Cria um novo usuário.
2. **GET /api/users/{id}**: Obtém os detalhes de um usuário específico.
3. **PUT /api/users/{id}**: Atualiza os detalhes de um usuário existente.
4. **DELETE /api/users/{id}**: Exclui um usuário.

## Como Executar Cada Método

1. **POST - Criar um Novo Usuário**: Envie uma requisição POST para `/api/users/` com os dados do usuário no corpo da requisição.
2. **GET - Obter Detalhes de um Usuário**: Envie uma requisição GET para `/api/users/{id}` para obter os detalhes de um usuário específico.
3. **PUT - Atualizar um Usuário Existente**: Envie uma requisição PUT para `/api/users/{id}` com os novos dados do usuário no corpo da requisição.
4. **DELETE - Excluir um Usuário**: Envie uma requisição DELETE para `/api/users/{id}` para excluir um usuário.


# Documentação do Endpoint de registro de usuários

## Funcionamento Geral

O endpoint de registros tem como objetivo registrar um usuário ao evento.

## Métodos Disponíveis

1. **POST /api/event/register/**: Associa um usuário a um evento.
2. **GET /api/event/register/**: Obtém todos os eventos que um usuário está associado.

## Como Executar Cada Método

1. **POST - Associa um usuário a um evento**: Envie uma requisição POST para `/api/event/register/` com o id do evento no corpo da requisição e o token do usuário no `header Authorization`.
2. **GET - Obter Eventos do usuário**: Envie uma requisição GET para `/api/event/register/` para obter os eventos que um usuário está cadastrado.


# Documentação do Endpoint Token da Aplicação

Este documento descreve o funcionamento básico do endpoint `/token/` de uma aplicação, usado para autenticação e obtenção de tokens de acesso.

## Funcionamento Geral

O endpoint `/token/` fornece tokens de acesso para usuários autenticados.

## Métodos Disponíveis

1. **POST /token/**: Obtém um token de acesso para o usuário autenticado.

## Como Executar o Método

1. **POST - Obter Token de Acesso**: Envie uma requisição POST para `/token/` com as credenciais de autenticação do usuário no corpo da requisição. O servidor autentica as credenciais e retorna um token de acesso válido, se a autenticação for bem-sucedida.


## Contribuindo

Sinta-se à vontade para enviar pull requests ou abrir issues se encontrar algum problema ou tiver sugestões de melhoria.
