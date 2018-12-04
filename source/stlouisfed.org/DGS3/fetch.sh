#!/bin/bash

declare -r ua='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36'
declare -r referer='https://fred.stlouisfed.org/series/DGS3'

declare -r ts=$(date +%Y-%m-%d-%H-%M-%S)
declare -r yyyy=${ts:0:4}
declare -r mm=${ts:5:2}
declare -r dd=${ts:8:2}

declare -r url="https://fred.stlouisfed.org/graph/fredgraph.csv?bgcolor=%23e1e9f0&chart_type=line&drp=0&fo=open%20sans&graph_bgcolor=%23ffffff&height=450&mode=fred&recession_bars=on&txtcolor=%23444444&ts=12&tts=12&width=1168&nt=0&thu=0&trc=0&show_legend=yes&show_axis_titles=yes&show_tooltip=yes&id=DGS3&scale=left&cosd=1962-01-02&coed=2018-11-30&line_color=%234572a7&link_values=false&line_style=solid&mark_type=none&mw=3&lw=2&ost=-99999&oet=99999&mma=0&fml=a&fq=Daily&fam=avg&fgst=lin&fgsnd=2009-06-01&line_index=1&transformation=lin&vintage_date=$yyyy-$mm-$dd&revision_date=$yyyy-$mm-$dd&nd=1962-01-02"

declare -r destdir=./data/raw/$yyyy
mkdir -p $destdir

declare -r destfile=$destdir/$ts-DGS3.csv
echo "url=$url destfile=$destfile"

mkdir -p ./data/tmp/
declare -r tmpfile=$(mktemp "./data/tmp/${ts}-XXXX")
if curl --retry 3 -L --max-time 20 --max-filesize 10000000 --user-agent "$ua"  -H 'Accept-Language: en-us' -H 'Accept-Encoding: gzip' --referer "$referer" -o $tmpfile "$url"
then
    stat -f%z $tmpfile
    if od -x -N 2 $tmpfile | grep 8b1f; then
        # already gzip'd
        mv $tmpfile $destfile.gz
    else
        gzip $tmpfile
        mv $tmpfile.gz $destfile.gz
        stat -f%z $destfile.gz
    fi
else
    exit 1
fi
