#!/bin/bash

BACKUP_SRC="/mnt/e/cloeila_backup.bak"
BACKUP_DST="/var/lib/postgresql/Databases/Cloeila/cloeila_backup.bak"
LOG_FILE="/var/lib/postgresql/Databases/Cloeila/restore_log.txt"
DB_NAME="cloeila_dev"

echo "[INFO] Copying backup from $BACKUP_SRC to $BACKUP_DST"
cp "$BACKUP_SRC" "$BACKUP_DST"

echo "[INFO] Creating database $DB_NAME (if not exists)"
sudo -u postgres psql -tc "SELECT 1 FROM pg_database WHERE datname = '$DB_NAME'" | grep -q 1 || \
sudo -u postgres psql -c "CREATE DATABASE $DB_NAME"

echo "[INFO] Restoring backup to $DB_NAME"
sudo -u postgres pg_restore -d "$DB_NAME" "$BACKUP_DST" > "$LOG_FILE" 2>&1

if grep -q ERROR "$LOG_FILE"; then
    echo "[FAILURE] Restore failed. See log at $LOG_FILE for details."
else
    echo "[SUCCESS] Restore completed. See log at $LOG_FILE"
fi

