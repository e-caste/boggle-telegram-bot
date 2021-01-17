#!/bin/bash

PATH=""
CNT_ID=$(docker ps --filter ancestor=bogglebot | tail -1 | cut -d ' ' -f 1)

cd "$PATH"/boggle-telegram-bot

git checkout production
git pull
docker build -t bogglebot:latest .
if [[ "$CNT_ID" != "CONTAINER" ]]; then
  docker stop $CNT_ID
  docker rm $CNT_ID
fi
./launch.sh

cd -