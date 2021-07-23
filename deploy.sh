source ./venv.sh

npm install
npm run build

pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput

supervisorctl restart banks-comparer-gunicorn
