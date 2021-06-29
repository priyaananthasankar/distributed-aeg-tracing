#! /bin/bash

# make a data folder
mkdir ../data

# generate dummy parquet files
for i in {1..100}
    do
        cp test.parquet ../data/test_$i.parquet
    done