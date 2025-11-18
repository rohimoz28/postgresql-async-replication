#!/bin/bash
set -e

PGDATA="/var/lib/postgresql/data"

echo "========================================="
echo "Setting up REPLICA Server"
echo "========================================="

# Cek apakah sudah ada data (untuk avoid re-setup)
if [ -f "$PGDATA/PG_VERSION" ]; then
    echo "Data directory already initialized, starting PostgreSQL..."
    exec docker-entrypoint.sh postgres
fi

echo "Waiting for PRIMARY to be ready..."
until pg_isready -h db-master -p 5432 -U flaskuser; do
    echo "  Primary not ready yet, retrying in 3 seconds..."
    sleep 3
done

echo "PRIMARY is ready!"
echo ""
echo "Starting pg_basebackup from PRIMARY..."

# Hapus isi data directory jika ada
rm -rf ${PGDATA}/*

# Jalankan pg_basebackup
PGPASSWORD=replicator123 pg_basebackup \
    -h db-primary \
    -D /var/lib/postgresql/data \
    -U replicator \
    -v -P -R \
    --slot=standby_slot1 \
    --checkpoint=fast

echo "pg_basebackup completed successfully!"
echo ""

# Buat standby.signal (PostgreSQL 12+)
touch ${PGDATA}/standby.signal
echo "Created standby.signal"

# Konfigurasi koneksi ke primary
cat >> ${PGDATA}/postgresql.auto.conf <<EOF
# Replica Configuration
primary_conninfo = 'host=db-primary port=5432 user=replicator password=replicator123 application_name=standby_slot1'
primary_slot_name = 'standby_slot1'
hot_standby = on
EOF

echo "Configured primary connection info"
echo ""
echo "========================================="
echo "REPLICA Setup Complete!"
echo "Starting PostgreSQL in standby mode..."
echo "========================================="

# Start PostgreSQL
exec docker-entrypoint.sh postgres