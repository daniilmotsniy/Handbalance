Login & Set Up: 

`ssh -i <filename>.pem.txt ec2-user@<ip>`

`sudo yum install -y docker`

`sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)"     -o /usr
/local/bin/docker-compose`

`sudo chmod +x /usr/local/bin/docker-compose`

`sudo usermod -a -G docker ec2-user`

`ssh-keygen -t rsa`

`cat ~/.ssh/id_rsa.pub`

`sudo yum install git -y`

`sudo /etc/init.d/docker start`

`sudo systemctl enable docker.service`

`sudo systemctl start docker.service`

`sudo iptables -t nat -A PREROUTING -p tcp --dport 80 -j REDIRECT --to-ports 8000`

`sudo iptables -t nat -L`

Deploy docker:

`docker-compose -f docker-compose.yaml up -d`

AWS:

` aws s3 cp s3://handbalance/most_city.mp4 most_city.mp4`