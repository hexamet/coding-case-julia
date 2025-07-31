#!/bin/bash
set -e
mysql -u root "$MYSQL_DATABASE" < /schema.sql