#!/bin/bash

date >> logs/docker.elasnocongresso.log
cd src/
python3 -m scrapy crawl camara 1>> ../logs/crawl_camara.log 2>> ../logs/crawl_camara.err.log;
python3 -m scrapy crawl senado 1>> ../logs/crawl_senado.log 2>> ../logs/crawl_senado.err.log;
python run_models.py
python sync_spreadsheets.py

