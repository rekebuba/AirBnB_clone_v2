#!/usr/bin/env bash
# a Bash script that sets up web servers for the deployment of web_static

if ! command -v nginx -v &> /dev/null; then
    sudo apt -y update
    sudo apt -y install nginx
fi

if [ ! -d "data" ]; then
    mkdir data
fi

if [ ! -d "data/web_static" ]; then
    mkdir data/web_static
fi

if [ ! -d "data/web_static/releases" ]; then
    mkdir data/web_static/releases
fi

if [ ! -d "data/web_static/shared" ]; then
    mkdir data/web_static/shared
fi

if [ ! -d "data/web_static/releases/test" ]; then
    mkdir data/web_static/releases/test
    code="<html>
        <head>
        </head>
        <body>
            Holberton School
        </body>
    </html>"

    touch data/web_static/releases/test/index.html
    echo "$code" | tee data/web_static/releases/test/index.html &> /dev/null
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
if ! grep -qF "locarion /current/" /etc/nginx/sites-available/default; then
    sudo sed -i '55 r /dev/stdin' /etc/nginx/sites-available/default <<< "$server_config"
fi
