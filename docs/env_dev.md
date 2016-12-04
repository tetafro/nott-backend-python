# Prepare environment for development server

## 1. Install servers
```
sudo apt-get install nginx
sudo apt-get install postgresql libpq-dev
```

## 2. Install dependencies
```
sudo apt-get install python3-pip python3-dev gcc
sudo apt-get install libjpeg-dev zlib1g-dev  # for Pillow
sudo pip3 install virtualenv
sudo pip3 install dropbox  # for DB backup
sudo apt-get install git
sudo apt-get install bc  # install script dependency
```

## 3. Clone the repository
```
git clone https://github.com/tetafro/notes.git
```

## 4. Environment variables
```
export SERVER_MODE=dev
sudo sh -c 'echo SERVER_MODE=dev >> /etc/environment'
```

## 5. Make virtualenv
```
cd notes
virtualenv -p python3 venv
source venv/bin/activate
pip3 install -r requirements.txt
```

## 6. Copy configs
```
sudo cp configs/dev/nginx/sites-avaliable/notes /etc/nginx/sites-available/

cd /etc/nginx/sites-enabled/
sudo ln -s ../sites-available/notes .
sudo service nginx reload
```

## 7. DB setup
```
sudo su - postgres
createdb db_notes
createuser --no-createdb pguser
psql
\password pguser
GRANT ALL PRIVILEGES ON DATABASE db_notes TO pguser;

./manage.py migrate
```

## 8. Run server
```
./manage.py runserver
```
