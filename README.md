# projects_fastapi# shortener_fastapi
Project control service. Python 3.12 + FastAPI

## Requirements
- Docker

## Installation
- Clone repository
- Create `.env` file
```
git clone https://github.com/firepanda70/projects_fastapi
cd projects_fastapi
touch .env
```
- Fill `.env` file like below
```
DB_URL=postgresql+asyncpg://docker:docker@pg
REDIS_PASS=redis_pass
REDIS=redis://:redis_pass@redis
COMPOSE_PROJECT_NAME=projects_fastapi
POSTGRES_USER=docker
POSTGRES_PASSWORD=docker
POSTGRES_DB=docker
LOG_LEVEL=INFO
```
- Build docker containers
```
docker compose up -d --build
```
- Done!

## Usage
Docs will be avaliable [here](http://localhost/docs#/)

To access logs execute:
```
docker logs -f <WEB_CONTAINER_ID>
```

## Technologies
- Python 3.12
- FastAPI
- SQLAlchemy
- Pydantic
- Alembic
- PostgreSQL
- Redis
- Poetry
- Docker
