#!/bin/bash

PATH=""
CNT_ID=$(docker ps --filter ancestor=bogglebot | tail -1 | cut -d ' ' -f 1)

cd "$PATH"/boggle-telegram-bot

git checkout production
git pull
docker build -t bogglebot:latest .
docker stop $CNT_ID
docker rm $CNT_ID
./launch.sh

cd -