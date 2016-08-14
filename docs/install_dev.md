#### 1. Install software
```
sudo apt-get install nginx
sudo apt-get install postgresql libpq-dev
```

#### 2. Install dependencies
```
sudo apt-get install python3-pip python3-dev gcc
sudo apt-get install libjpeg-dev zlib1g-dev # for Pillow
sudo pip3 install virtualenv
sudo pip3 install dropbox # for DB backup
sudo apt-get install git
```

#### 3. Clone the repository
```
git clone https://github.com/tetafro/notes.git
```

#### 4. Environment variables
```
export SERVER_MODE=dev
sudo sh -c 'echo SERVER_MODE=dev >> /etc/environment'
```

#### 5. Make virtualenv
```
cd notes
virtualenv -p python3 venv
source venv/bin/activate
pip3 install -r requirements.txt
```

#### 6. Copy configs
```
sudo cp configs/dev/nginx/sites-avaliable/notes /etc/nginx/sites-available/

cd /etc/nginx/sites-enabled/
sudo ln -s ../sites-available/notes .
sudo service nginx reload
```

#### 7. DB setup
```
sudo su - postgres
createdb db_notes
createuser --no-createdb pguser
psql
\password pguser
GRANT ALL PRIVILEGES ON DATABASE db_notes TO pguser;

./manage.py migrate
```

#### 8. Run server
```
./manage.py runserver
```

#### 9. Linters
```
# JavaScript
sudo apt-get install nodejs npm
sudo ln -s /usr/bin/nodejs /usr/bin/node
sudo npm install -g jscs@2.11  # loris requires jscs < 3.0
npm install --save-dev jscs-preset-loris
# Python
sudo apt-get install pep8 pylint pyflakes
```

#### 10. JS compiler
```
sudo npm install -g requirejs uglify-js
cd project/public/js/
r.js -o build.js
```
