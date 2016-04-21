#! /bin/zsh

vw --binary -t -i ../../data/sentiment.model testdata.te -p testdata.te.pr  > audit.log
vw -i ../../data/sentiment.model -t --invert_hash model.readable.txt testdata.te --quiet
cat model.readable.txt  | tail -n+13 | sort -t: -k3nr | head -n30