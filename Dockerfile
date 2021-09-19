FROM pypy:3.6-7.3.0-slim
RUN mkdir -p /bot/dbs_old
WORKDIR /bot
COPY requirements.txt .
# install requirements as soon as possible so rebuilds are faster
RUN apt-get update && apt-get install -y gcc libffi-dev libssl-dev
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY *.py ./
ENV WD=""
CMD ["pypy3", "-u", "boggle_telegram_bot.py"]

# build with
#   docker build -t bogglebot .
# run with
# -e TOKEN=... -e CST_CID=...