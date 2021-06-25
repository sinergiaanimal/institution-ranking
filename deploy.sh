source ./venv.sh

npm run build
python manage.py migrate
python manage.py collectstatic --noinput
