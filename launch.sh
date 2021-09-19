#!/bin/bash

DB=_boggle_paroliere_bot_db
WORKDIR=/bot

docker run --restart unless-stopped \
           -v "$PWD"/$DB:$WORKDIR/$DB \
           -v "$PWD"/dbs_old:$WORKDIR/dbs_old \
           -e TOKEN="" \
           -e CST_CID="" \
           -itd bogglebot:latest