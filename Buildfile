docker stop flaskapp
docker stop some-mysql
docker rm flaskapp
docker rm some-mysql

docker build -t flaskapp .
docker run -p 3306:3306 --name some-mysql -e MYSQL_ROOT_PASSWORD=password -d mysql:8.0
sleep 30
docker run -p 80:5000 --name flaskapp --link some-mysql:some-mysql -d flaskapp
