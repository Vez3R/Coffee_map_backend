Для развертывания необходимо:
  
  1.Создать Dockerfile
  
  2.Создать Docker-compose.yml
  
  3.Запустить команды docker build -t coffee_map . & docker-compose up -d

Файл Dockerfile:

	FROM python:3.9.21-alpine3.21

	WORKDIR /code


	COPY Coffee_map_backend/Coffee_map_back/. .


	RUN pip install -r ./requirements.txt


	CMD flask run -h 0.0.0.0 -p 8080

Файл docker-compose.yml:

	version: '3'

	services:
  		db:
  
    			image: postgres:latest
    
    			restart: unless-stopped
    
    			ports:
    
     			 - "5432:5432"
    
    			container_name: db
    
    			volumes:
    
   			   - ./pgdb:/var/lib/postgresql/data
    
   			 environment:
    
   			   POSTGRES_DB: postgres
      
   			   POSTGRES_USER: postgres
   			   
    			  POSTGRES_PASSWORD: *любой пароль*
  
  		coffee_map:
  
    			image: coffee_map:latest
    
    			restart: unless-stopped
    
    			ports:
    
     			 - "8080:8080"
    
    			container_name: coffee_map
    
    			environment:
    
    			  DB_URL: 109.172.94.7
      
    			  DB_PORT: 5432
      
     			  DB_LOGIN: postgres
      
      			  DB_PASSWORD: *любой пароль*
После того как контейнеры развернуты, необходимо скопировать в контейнер базы данных файл с бэкапом, для этого надо:

 1. Скопировать файл с бэкапом в контейнер с помощью команды docker cp *навание бэкапа* db:.

 2. Зайти в контейнер командой docker exec -it db bash

 3. Востановить бэкап командой psql < *путь до бэкапа*
