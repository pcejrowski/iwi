#!/usr/bin/env bash
sample_dir=../jupyter-wikidata/matrix/sample
rm -rf ${sample_dir}
mkdir ${sample_dir}
for file in ../jupyter-wikidata/matrix/*
do
    cp $file ${sample_dir}/$(basename "$file")
done

for file in ../jupyter-wikidata/matrix/po_slowach-lista-simple-20120104 ../jupyter-wikidata/matrix/po_slowach-categories-simple-20120104
do
    head -n 1000 $file > ${sample_dir}/$(basename "$file")
done