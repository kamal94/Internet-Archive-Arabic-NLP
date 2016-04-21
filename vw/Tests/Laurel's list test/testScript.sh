#! usr/bin/zsh

vw --binary -t -i ../../data/sentiment.model -p testdata.te.pr testdata.te > audit.log
vw -i data/sentiment.model -t --invert_hash sentiment.model.readable testdata.te --quiet > readable.txt