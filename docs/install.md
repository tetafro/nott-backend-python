#### 1. Install software
```
apt-get install python3-pip python3-dev gcc
apt-get install libjpeg-dev zlib1g-dev # for Pillow
apt-get install nginx
apt-get install uwsgi uwsgi-plugin-python3
apt-get install postgresql libpq-dev
apt-get install git
pip3 install virtualenv
pip3 install dropbox # for DB backup
```

#### 2. Clone the repository
```
git clone https://github.com/tetafro/notes.git
```

#### 3. Environment variables
```
export SERVER_MODE=production
echo SERVER_MODE=production >> /etc/environment
```

#### 4. Make virtualenv
```
virtualenv -p python3 venv
source venv/bin/activate
pip3 install -r requirements.txt
```

#### 5. Copy configs
```
cp configs/nginx/sites-avaliable/* /etc/nginx/sites-available/
cp configs/uwsgi/apps-available/ /etc/uwsgi/apps-available/

cd /etc/nginx/sites-enabled/
ln -s ../sites-available/notes .

cd /etc/uwsgi/apps-enabled/
ln -s ../apps-available/notes.ini .
```

#### 6. DB setup
```
su - postgres
createdb db_notes
createuser --no-createdb pguser
psql
\password pguser
GRANT ALL PRIVILEGES ON DATABASE db_notes TO pguser;
\quit
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
