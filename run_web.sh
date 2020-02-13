echo creating user
exec manage.py shell -c "from django.contrib.auth.models import User; User.objects.create_superuser('root', 'admin@example.com', 'root')"
# Start Gunicorn processes
echo Starting Gunicorn.
exec gunicorn orchestryzi_api.wsgi \
    --log-file - \
    --name orechestryzi_studio_api \
    --workers 5 \
    --log-level=info \
    --bind=0.0.0.0:8100
