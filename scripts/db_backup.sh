#!/bin/bash
#
# Backup project's DB to Dropbox
#

DATE=$(date '+%Y%m%d')
DIR="/var/backups/postgresql/db_nott/"
FILE="$DATE.sql"
LOG="/var/logs/nott/db_backup.log"

TIME=$(date '+%H:%M:%S %d.%m.%Y')
echo -e "\nStart job: $TIME" >> $LOG
echo "---" >> $LOG

if [ ! -d "$DIR" ]; then
    echo "$(date '+%H:%M:%S %d.%m.%Y') Error: backup directory not found: $DIR" >> $LOG
    exit 1
fi

# PostgreSQL backup of db_nott base
pg_dump db_nott -f "$DIR$FILE"
if [ $? -eq 0 ]; then
    echo "$(date '+%H:%M:%S %d.%m.%Y') Dump completed" >> $LOG
else
    echo "$(date '+%H:%M:%S %d.%m.%Y') Error: dump failed" >> $LOG
    exit 1
fi

# Compress
gzip -f "$DIR$FILE"
if [ $? -eq 0 ]; then
    echo "$(date '+%H:%M:%S %d.%m.%Y') Compress completed" >> $LOG
else
    echo "$(date '+%H:%M:%S %d.%m.%Y') Error: compress failed" >> $LOG
    exit 1
fi

# Send backup to Dropbox
echo -n "$(date '+%H:%M:%S %d.%m.%Y') " >> $LOG
/var/lib/postgresql/dropbox_upload.py $DIR$FILE.gz >> $LOG

# Remove files older than 5 days
find /var/backups/postgresql/db_nott/ -mtime +5 -exec rm -f {} \;

# Exit with success code
exit 0
