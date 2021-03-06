# Retries a command on failure.
# $1 - the max number of attempts
# $2... - the command to run
retry() {
    local -r -i max_attempts="$1"; shift
    local -i attempt_num=1
    until "$@"
    do
        if ((attempt_num==max_attempts))
        then
            echo "Attempt $attempt_num failed and there are no more attempts left!"
            return 1
        else
            echo "Attempt $attempt_num failed! Trying again in $attempt_num seconds..."
            sleep $((attempt_num++))
        fi
    done
}

#################
echo "Reading Config from environment variables"
echo "Now initialising dvc configurations"
# Retry several times for first command
retry 10 dvc db init
echo "Checking DVC version"
dvc version
echo "Pinging the DB"
dvc db ping
echo "Database Version before any action"
dvc db current
echo "Now upgrading db to the head"
dvc db upgrade --no-confirm --head
echo "Database Version after all upgrades are done"
dvc db current
