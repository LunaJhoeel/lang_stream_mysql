# Containerize and deploy the Streamlit app
docker-compose up

# Error database 'tech_stack_db' does not exist
docker-compose up -d
# Get inside the MySQL container to create database
docker exec -it <mysql_container_id> /bin/bash
mysql -u root -p
create database tech_stack_db;

# Error "Table 'tech_stack_db.tech_stack_table' doesn't exist"
create table tech_stack_db.tech_stack_table (component varchar(255));

INSERT INTO tech_stack_db.tech_stack_table (component) VALUES ('Test');
DE
