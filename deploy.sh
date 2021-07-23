source ./venv.sh

npm run build

pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
