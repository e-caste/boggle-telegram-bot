FROM python:3.9-slim-buster
RUN mkdir /bot
WORKDIR /bot
COPY requirements.txt .
# install requirements as soon as possible so rebuilds are faster
RUN apt-get update && apt-get install -y gcc libffi-dev
RUN pip3 install -r requirements.txt
COPY *.py ./
ENV WD=""
CMD ["python", "-u", "boggle_telegram_bot.py"]

# build with
#   docker build -t bogglebot .
# run with
# -e TOKEN=... -e CST_CID=...