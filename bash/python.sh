#!/bin/bash

echo '' > test.txt

for pdf in $(ls CORPUS_TRAIN)
do
    python3 app/index.py CORPUS_TRAIN/${pdf} CORPUS_TEXT/${pdf}.txt >> test.txt
done
