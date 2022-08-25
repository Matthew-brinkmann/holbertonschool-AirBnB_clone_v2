#!/usr/bin/env bash
# sets up your web servers for the deployment of web_static
NEW_LOCATION="\tlocation /hbnb_static {\n\t\talias /data/web_static/current/;\n\t}\n"
if [[ $(dpkg -l nginx 2> /dev/null | wc -l) = 0 ]]; then
    apt-get -y update
    apt-get -y upgrade
    apt-get -y install nginx
    service nginx start
fi
mkdir -p /data/web_static/releases/test /data/web_static/shared
echo "server $HOSTNAME is responding correctly" > /data/web_static/releases/test/index.html
ln -sfn /data/web_static/releases/test/ /data/web_static/current
chown -hR ubuntu:ubuntu /data/
sudo sed -i "29i\\$NEW_LOCATION" /etc/nginx/sites-available/default
service nginx start
service nginx restart
