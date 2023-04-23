docker pull mysql/mysql-server
docker run --name mysql-container -p 3306:3306 -e MYSQL_ROOT_PASSWORD=password -d mysql/mysql-server:latest --init-file /schema.sql
docker cp ./data_service/ddl/schema.sql mysql-container:/schema.sql