#!/bin/bash

apt install nginx -y

export $(grep -v '^#' .env | xargs)
envsubst < infrastructure/nginx/nginx.conf.template > /etc/nginx/nginx.conf

systemctl restart nginx
apt install snapd


snap install --classic certbot
ln -s /snap/bin/certbot /usr/bin/certbot
#certbot --nginx