#!/usr/bin/env bash
# a Bash script that sets up web servers for the deployment of web_static

if ! command -v nginx -v &> /dev/null; then
    sudo apt -y update
    sudo apt -y install nginx
fi

sudo mkdir -p /data/web_static/releases /data/web_static/shared

if [ ! -d "/data/web_static/releases/test" ]; then
    sudo mkdir /data/web_static/releases/test
    code="<html>
        <head>
        </head>
        <body>
            Holberton School
        </body>
    </html>"

    touch /data/web_static/releases/test/index.html
    echo "$code" | tee /data/web_static/releases/test/index.html &> /dev/null
fi

chmod 755 -R /data
ln -s -f /data/web_static/releases/test/ /data/web_static/current

server_config=\
'
        location /hbnb_static/ {
            alias /data/web_static/current/;
            autoindex off;
        }
'
if ! grep -qF "location /hbnb_static/" /etc/nginx/sites-available/default; then
    sudo sed -i '55 r /dev/stdin' /etc/nginx/sites-available/default <<< "$server_config"
fi

sudo service nginx restart
