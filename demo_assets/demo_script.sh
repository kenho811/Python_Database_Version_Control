#!sh
#################
echo "Waiting for 10 seconds until db backend is ready"
sleep 10

#################
echo "Now initialising dvc configurations"
dvc cfg init
echo "Now initialising dvc configurations"
dvc db init
echo "Now upgrading db"
dvc db upgrade
echo "Now upgrading db"
dvc db upgrade

#############
echo "From host machine, please use the below URL to check out the state of the postgres DB after the migration is run"
echo "URL:  postgres://test:test@localhost:5433/test"
