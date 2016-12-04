# Prepare environment for production server

## 1. Install servers
```
sudo apt-get install nginx
sudo apt-get install uwsgi uwsgi-plugin-python3
sudo apt-get install postgresql libpq-dev
```

## 2. Install dependencies
```
sudo apt-get install python3-pip python3-dev gcc
sudo apt-get install libjpeg-dev zlib1g-dev # for Pillow
sudo pip3 install virtualenv
sudo pip3 install dropbox # for DB backup
```

## 3. Copy project to server

## 4. Make virtualenv
```
cd notes
virtualenv -p python3 venv
source venv/bin/activate
pip3 install -r requirements.txt
```

## 5. Copy configs
```
sudo cp configs/nginx/sites-avaliable/* /etc/nginx/sites-available/
sudo cp configs/uwsgi/apps-available/* /etc/uwsgi/apps-available/

cd /etc/nginx/sites-enabled/
sudo ln -s ../sites-available/notes .

cd /etc/uwsgi/apps-enabled/
sudo ln -s ../apps-available/notes.ini .
sudo service nginx reload
```

## 6. DB setup
```
sudo su - postgres
createdb db_notes
createuser --no-createdb pguser
psql
\password pguser
GRANT ALL PRIVILEGES ON DATABASE db_notes TO pguser;
psql db_notes < db_notes_dump.sql
```
