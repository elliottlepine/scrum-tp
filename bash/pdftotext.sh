#!/bin/bash

args=("-raw" "-bbox-layout -q -l 1")

for pdf in $(ls CORPUS_TRAIN)
do
    for i in ${!args[@]};
    do 
        echo pdftotext ${args[$i]} 'CORPUS_TRAIN/'$pdf 'CORPUS_TEXT/'$pdf'.'$i'.txt'
        pdftotext ${args[$i]} 'CORPUS_TRAIN/'$pdf 'CORPUS_TEXT/'$pdf'.'$i'.txt'
    done 
done
