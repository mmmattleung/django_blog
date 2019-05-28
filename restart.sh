#!/bin/bash


/usr/local/nginx/sbin/nginx -s quit
echo "$?"
sleep 1

uwsgi --stop uwsgi.pid
echo "$?"
sleep 1


/usr/local/nginx/sbin/nginx
echo "$?"
sleep 1

uwsgi --ini uwsgi.ini
echo "$?"
sleep 1
