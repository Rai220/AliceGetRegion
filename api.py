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

# Импортируем подмодули Flask для запуска веб-сервиса.
from flask import Flask, request
app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG)

# Хранилище данных о сессиях.
sessionStorage = {}
regions = {}

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
    print("Main called")
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