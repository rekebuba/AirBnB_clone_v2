#!/usr/bin/env bash

if ! command -v nginx -v &> /dev/null; then
    sudo apt -y update
    sudo apt -y install nginx
fi

if ! command -v cd data/ &> /dev/null; then
    mkdir data
fi

if ! command -v cd data/web_static/ &> /dev/null; then
    mkdir data/web_static
fi

if ! command -v cd data/web_static/releases/ &> /dev/null; then
    mkdir data/web_static/releases
fi

if ! command -v cd data/web_static/shared/ &> /dev/null; then
    mkdir data/web_static/shared
fi

if ! command -v cd data/web_static/shared/ &> /dev/null; then
    mkdir data/web_static/shared
fi

if ! command -v cd data/web_static/releases/test/ &> /dev/null; then
    mkdir data/web_static/releases/test
    code="<html>
    <head>
    </head>
    <body>
        Holberton School
    </body>
    </html>
        "
    touch data/web_static/releases/test/index.html
    echo "$code" | tee data/web_static/releases/test/index.html
fi

if ! command -v cd data/web_static/current/ &> /dev/null; then
    mkdir data/web_static/current
fi
chmod 777 -R data/
ln -s -f data/web_static/releases/test/ data/web_static/current

server_config=\
'
        locarion /current/ {
            alias /data/web_static/current/;
            autoindex off;
        }
'
if ! grep -qF "$server_config" /etc/nginx/sites-available/default; then
    sudo sed -i '55 r /dev/stdin' /etc/nginx/sites-available/default <<< "$server_config"
fi
