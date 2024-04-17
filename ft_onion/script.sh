#!/bin/sh

apt install -y nginx
apt install -y tor

cp ./index.html /var/www/html
cp ./torrc /etc/tor/
cp ./nginx.conf /etc/nginx

systemctl restart nginx
systemctl restart tor

#Del nginx:
#sudo apt remove nginx
#sudo apt purge nfinx nginx-common

#Del tor:
#sudo apt remove tor
#sudo apt purge tor torsocks

#Nginx nothing, 2 line for torrc