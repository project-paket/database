#!/bin/bash
PGPASSWORD=password
export PGPASSWORD
pg_restore -h 188.225.76.56 -U user_1 -c -F c -d elevatorr $1
