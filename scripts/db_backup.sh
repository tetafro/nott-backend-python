#!/bin/bash
#
# Backup project's DB to Dropbox
#

DATE=$(date '+%Y%m%d')
DIR="/var/backups/nott"
FILE="$DATE.dump"
LOGDIR="/var/log/nott"
LOG="$LOGDIR/db_backup.log"

mkdir -p $DIR $LOGDIR

TIME=$(date '+%H:%M:%S %d.%m.%Y')
echo -e "\nStart job: $TIME" >> $LOG
echo "---" >> $LOG

# PostgreSQL backup of db_nott base
docker exec nott_db_1 \
    pg_dump -U postgres -Fc -C db_nott > "$DIR/$FILE"
if [ $? -eq 0 ]; then
    echo "$(date '+%H:%M:%S %d.%m.%Y') Dump completed" >> $LOG
else
    echo "$(date '+%H:%M:%S %d.%m.%Y') Error: dump failed" >> $LOG
    exit 1
fi

# Send backup to Dropbox
echo -n "$(date '+%H:%M:%S %d.%m.%Y') " >> $LOG
/root/dropbox_upload.py $DIR/$FILE >> $LOG

# Remove files older than 5 days
find $DIR -mtime +5 -exec rm -f {} \;

# Exit with success code
exit 0
