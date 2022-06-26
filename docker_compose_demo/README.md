## Demo with Docker Compose

- Run the below to see it in action
```commandline
# Clone the repo and checkout release branch
git clone git@github.com:kenho811/Python_Database_Version_Control.git 

# cd to the repository
cd Python_Database_Version_Control/docker_compose_demo

# Fnd the docker-compose.yml and run 
docker compose up

# Using psql as client, access the postgres DB and see the result
(URL: postgres://test:test@localhost:5433/test)
PGPASSWORD=test psql -U test -d test -h localhost -p 5433

# Check out docker-compose.yml file for usage as a microservice
```

