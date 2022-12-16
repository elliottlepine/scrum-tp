#!/bin/bash

for pdf in $(ls CORPUS_TRAIN)
do
    python3 app/index.py -t -i CORPUS_TRAIN/${pdf} -o CORPUS_TEXT/${pdf}.txt
done
