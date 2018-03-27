# -*- coding: utf-8 -*-
# coding: utf-8
# Импортирует поддержку UTF-8.
from __future__ import unicode_literals

# Импортируем модули для работы с JSON и логами.
import json
import logging
import random
import re
import codecs
from multiprocessing import Pool

from pymongo import MongoClient
import time
import asyncio

# Импортируем подмодули Flask для запуска веб-сервиса.
from flask import Flask, request
app = Flask(__name__)
client = MongoClient("mongodb://user:cubicrobot@ds123029.mlab.com:23029/skills")

logging.basicConfig(level=logging.DEBUG)

# Хранилище данных о сессиях.
sessionStorage = {}
regions = {}

def saveToDb(userId, text):
    print("Saving data to db...")
    result = client.skills.requests.update({'_id': userId}, {'text': text, 'time': time.time()}, upsert=True)
    print(result)

def loadRegions():
    f = codecs.open('regions.txt', 'r', 'UTF-8')
    for line in f:
        line = line.strip()
        parts = line.split(',')
        for region in parts[0:-1]:
            regions[region] = parts[-1]

loadRegions()

# Задаем параметры приложения Flask.
@app.route("/", methods=['POST'])
def main():
    # Функция получает тело запроса и возвращает ответ.
    logging.info('Request: %r', request.json)

    response = {
        "version": request.json['version'],
        "session": request.json['session'],
        "response": {
            "end_session": False
        }
    }

    handle_dialog(request.json, response)

    logging.info('Response: %r', response)    
    print("Before saving to db...")
    saveToDb(request.json['session']['user_id'], request.json['request']['command'])

    return json.dumps(
        response,
        ensure_ascii=False,
        indent=2
    )

# Функция для непосредственной обработки диалога.
def handle_dialog(req, res):
    user_id = req['session']['user_id']
    reqText = req['request']['command']
    region = re.sub("\D", "", reqText)
    res['response']['text'] = getRegion(region)

def getRegion(region):
    if not region:
        return 'Назовите код региона'
    if region in regions:
        return region + ' это ' + regions[region]
    else:
        return 'Я не знаю такого региона как ' + region