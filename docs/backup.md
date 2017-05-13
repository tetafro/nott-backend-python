# DB backup

```
cp scripts/db_backup.sh scripts/dropbox_upload.py /var/lib/postgresql/
chown postgres:postgres /var/lib/postgresql/db_backup.sh /var/lib/postgresql/dropbox_upload.py

mkdir -p /var/backups/postgresql/db_nott/
chown -R postgres:postgres /var/backups/postgresql/

mkdir /var/logs/nott/
chmod a+rw /var/logs/nott/

su - postgres
chmod u+x dropbox_upload.py db_backup.sh
echo localhost:5432:db_nott:pguser:password > .pgpass
chmod 0600 .pgpass

crontab -e
1 4 * * * ~/db_backup.sh
```

Get OAuth2 token for dropbox_upload.py here: https://www.dropbox.com/developers/apps/
