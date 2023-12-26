# Be_backend

## Para iniciar o projeto, clone o proejto be_frontend e be_backend no mesmo diretório

### Crie os seguintes arquivos na raiz do diretório
* .env
* Caddyfile
* docker-compose.yml


---

## Para o .env utilize o .env.example dentro de be_backend como guia para configurar suas variáveis de ambiente

```
PORT=8000
ENVIRONMENT=development
PYTHONPATH=.
POSTGRES_HOSTNAME=host.docker.internal //127.0.0.1
POSTGRES_PORT=5432
POSTGRES_USER=db_user
POSTGRES_PASSWORD=db_password
POSTGRES_DB=db_name
POSTGRES_SSL=false

EMAIL_RESET_TOKEN_EXPIRE_HOURS=1

FIRST_SUPER_ADMIN_EMAIL=superadmin@email.com
FIRST_SUPER_ADMIN_PASSWORD=superdupersecretpassword
FIRST_SUPER_ADMIN_ACCOUNT_NAME=superduperaccount

SECRET_KEY=secret
ACCESS_TOKEN_EXPIRE_MINUTES=60
USERS_OPEN_REGISTRATION=True

VITE_SERVER_NAME=http://127.0.0.1/api/v1/

MAIL_USERNAME=user@example.com
MAIL_PASSWORD=foobar

APP_URL=127.0.0.1
```

--- 

## Para o Caddyfile segue um exemplo de configuração

```
{
	local_certs
	auto_https disable_redirects
}

http://127.0.0.1:80 {
    reverse_proxy /api/* http://web:8000
    reverse_proxy http://app:8080
    tls internal
}
```

---

## Para o docker-compose.yml segue um exemplo de configuração

```
version: "3"
services:
  app:
    image: frontend
    build: ./be_frontend
    container_name: frontend
    env_file:
      - .env
    ports:
      - "8080:8080"

  web:
    build:
      context: ./be_backend
      args:
        - ENVIRONMENT=${ENVIRONMENT}
    volumes:
      - ./be_backend:/app
      - ./be_backend/app/logs:/app/logs
    image: pythonweb     
    container_name: backend
    ports:
      - "${PORT}:8000"
    depends_on:
      - db
    env_file:
      - .env

  db:
    image: postgres:12-alpine
    ports:
      - "5432:5432"
    volumes:
      - ./postgres-data:/var/lib/postgresql/data
    env_file:
      - .env

  caddy:
    image: caddy:latest
    container_name: caddy
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./Caddyfile:/etc/caddy/Caddyfile # Mount your Caddy configuration file
    depends_on:
      - web
      - app

volumes:
  postgres_data:

```

---

# Para iniciar o projeto

## Abra o terminal na raiz do diretório e execute os seguintes comandos

```
docker-compose up -d --build
```

```
docker-compose exec web alembic upgrade head
```
