#!/bin/bash

set -e

function get_cnt_id {
  local _cnt_id=$(docker ps --filter ancestor=bogglebot | tail -1 | cut -d ' ' -f 1)
  echo $_cnt_id
}

REPO_PATH=""
CNT_ID=$(get_cnt_id)

cd "$REPO_PATH"/boggle-telegram-bot

git checkout master
git pull
docker build -t bogglebot:latest .
if [[ "$CNT_ID" != "CONTAINER" ]]; then
  docker stop $CNT_ID
  # docker rm $CNT_ID
fi
./launch.sh
cd -
CNT_ID=$(get_cnt_id)
echo "Following container logs, exit with Ctrl+C..."
docker logs -f $CNT_ID
