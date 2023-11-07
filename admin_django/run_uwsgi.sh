set -e

chown www-data:www-data /var/log

python3 manage.py collectstatic --no-input --clear
python3 manage.py migrate --no-input
#python manage.py compilemessages -l en -l ru
python manage.py createsuperuser --noinput || true

uwsgi --strict --ini /app/uwsgi.ini
