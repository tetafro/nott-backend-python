#### 1. Install servers
```
sudo apt-get install nginx
sudo apt-get install uwsgi uwsgi-plugin-python3
sudo apt-get install postgresql libpq-dev
```

#### 2. Install dependencies
```
sudo apt-get install python3-pip python3-dev gcc
sudo apt-get install libjpeg-dev zlib1g-dev # for Pillow
sudo pip3 install virtualenv
sudo pip3 install dropbox # for DB backup
```

#### 3. Copy project to server
```
scp -P 22 project.tar user@example.com:/home/user/
sudo cp /home/user/project.tar /var/www/notes/
```

#### 4. Make virtualenv
```
cd notes
virtualenv -p python3 venv
source venv/bin/activate
pip3 install -r requirements.txt
```

#### 5. Copy configs
```
sudo cp configs/nginx/sites-avaliable/* /etc/nginx/sites-available/
sudo cp configs/uwsgi/apps-available/* /etc/uwsgi/apps-available/

cd /etc/nginx/sites-enabled/
sudo ln -s ../sites-available/notes .

cd /etc/uwsgi/apps-enabled/
sudo ln -s ../apps-available/notes.ini .
sudo service nginx reload
```

#### 6. DB setup
```
sudo su - postgres
createdb db_notes
createuser --no-createdb pguser
psql
\password pguser
GRANT ALL PRIVILEGES ON DATABASE db_notes TO pguser;
psql db_notes < db_notes_dump.sql
```

#### 7. DB backup
```
cp scripts/db_backup.sh scripts/dropbox_upload.py /var/lib/postgresql/
chown postgres:postgres /var/lib/postgresql/db_backup.sh /var/lib/postgresql/dropbox_upload.py

mkdir -p /var/backups/postgresql/db_notes/
chown -R postgres:postgres /var/backups/postgresql/

mkdir /var/logs/notes/
chmod a+rw /var/logs/notes/

su - postgres
chmod u+x dropbox_upload.py db_backup.sh
echo localhost:5432:db_notes:pguser:password > .pgpass
chmod 0600 .pgpass

crontab -e
1 4 * * * ~/db_backup.sh
```

Get OAuth2 token for dropbox_upload.py here: https://www.dropbox.com/developers/apps/
