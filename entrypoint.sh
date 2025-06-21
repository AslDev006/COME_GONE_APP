#!/bin/sh


set -o errexit
set -o nounset

echo "Fixing permissions..."
whoami
chown -R app:app /app/database

echo "Permissions fixed."

exec "$@"