# Llamkay

Aplicar las migraciones en el siguiente orden:
´´´
python manage.py makemigrations chats
python manage.py makemigrations llamkay
python manage.py makemigrations users
python manage.py makemigrations jobs
python manage.py makemigrations
´´´
Para finalmente: python manage.py migrate
