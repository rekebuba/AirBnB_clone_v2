#!/usr/bin/env bash
# a Bash script that sets up web servers for the deployment of web_static

if [ ! -x /usr/sbin/nginx ]; then
	sudo apt-get update -y -qq && \
	     sudo apt-get install -y nginx
fi

sudo mkdir -p /data/web_static/releases/test /data/web_static/shared/

echo "<h1>Welcome<\h1>" | sudo dd status=none of=/data/web_static/releases/test/index.html

sudo ln -sf /data/web_static/releases/test /data/web_static/current

sudo chown -R ubuntu:ubuntu /data/

sudo cp /etc/nginx/sites-enabled/default nginx-sites-enabled_default.backup

sudo sed -i '37i\\tlocation /hbnb_static/ {\n\t\talias /data/web_static/current/;\n\t}\n' /etc/nginx/sites-available/default

sudo service nginx restart
