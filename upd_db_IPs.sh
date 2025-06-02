#! /bin/bash

cd /root/tfg/dhcp

mysql -v -v --user=personalTIC --password=tfg_2025 db_TIC < ./upd_db_TIC.sql > /tmp/upd_db_TIC.log 2>&1
