pip install -r requirements.txt
cd company-migration-ng
npm install
npm run build --prod
cd ..
rm -rf static
python manage.py collectstatic
python manage.py runserver 8000