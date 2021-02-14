import tweepy, time, sys
import hashlib  # hash do tweet
import json     # escrever JSON
import os.path  # paths do sistema
import os       # ler variaveis de ambiente
import time     # sleep
from dotenv import load_dotenv # ler variaveis de ambiente do arquivo .env
import random
from datetime import datetime

load_dotenv()

if not os.path.exists('dados/.dummy'):
    print("Faltando pasta ./dados/ (arquivo .dummy nao existe)")
    raise

if not os.path.exists('dados/tweets.json'):
    print("Faltando arquivo ./dados/tweets.json [execute primeiro o script @elasnacamara.py")
    raise

if not os.getenv("CONSUMER_KEY"):
    print("Faltando configurar ENV CONSUMER_KEY")
    raise
if not os.getenv("CONSUMER_SECRET"):
    print("Faltando configurar ENV CONSUMER_SECRET")
    raise
if not os.getenv("ACCESS_KEY"):
    print("Faltando configurar ENV ACCESS_KEY")
    raise
if not os.getenv("ACCESS_SECRET"):
    print("Faltando configurar ENV ACCESS_SECRET")
    raise

print ("Iniciando... " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

dirName = 'dados/tweets-enviados/'
if not os.path.exists(dirName):
    os.mkdir(dirName)
    print("Diretorio " , dirName ,  " criado")

with open('dados/tweets.json') as f:
  tweets = json.load(f)

auth = tweepy.OAuthHandler(os.getenv("CONSUMER_KEY"), os.getenv("CONSUMER_SECRET"))
auth.set_access_token(os.getenv("ACCESS_KEY"), os.getenv("ACCESS_SECRET"))
api = tweepy.API(auth)

for tweet in tweets:
    text = tweet['tweet']
    result = hashlib.md5(text.encode())
    fileName = f'{dirName}/{result.hexdigest()}'

    if os.path.exists( fileName ):
        print ("tweet '", text, "' ja foi tweetado")
        continue

    print ("tweetando '", text, "'...")
    response = api.update_status(text)
    with open(fileName, 'w') as outfile:
        json.dump(response._json, outfile)

    if bool(os.getenv("RANDOM_SLEEP_BETWEEN_TWEETS")):
        time.sleep(random.randint(60, 300)) # entre 1 minuto e 5


print ("Todos tweets enviados com sucesso!")
