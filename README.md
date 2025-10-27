# Llamkay

Aplicar las migraciones en el siguiente orden:
´´´
python manage.py makemigrations chats
python manage.py makemigrations soporte
python manage.py makemigrations users
python manage.py makemigrations jobs
python manage.py makemigrations
´´´
Para finalmente: python manage.py migrate

Para pasar datos: python manage.py seed_test_data
