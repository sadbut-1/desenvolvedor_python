# desenvolvedor_python

## Instalação

- git clone git@github.com:sadbut-1/desenvolvedor_python.git
- ** Se ja possuir o docker instalado
- docker-compose build
- docker-compose up ou docker-compose up -d

## Executar comandos django no projeto

- docker-compose exec web python manage.py test relatorios
- docker-compose exec web python manage.py createsuperuser
- docker-compose exec web python manage.py makemigrations
- docker-compose exec web python manage.py migrate
