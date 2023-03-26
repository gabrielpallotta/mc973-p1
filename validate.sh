#!/bin/bash

for d in test/* ; do
    if ! diff --strip-trailing-cr -q "$d/saida0.csv" "$d/esperado0.csv" &>/dev/null; then
        echo "$d failed for delay=0"
    fi
    if ! diff --strip-trailing-cr -q "$d/saida1.csv" "$d/esperado1.csv" &>/dev/null; then
        echo "$d failed for delay=1"
    fi
done