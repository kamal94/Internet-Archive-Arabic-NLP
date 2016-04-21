#! /bin/bash
echo CREATING THE MODEL
vw --binary data.tr --passes 20 -c -k -f data.model --ngram 2 -b 29 --loss_function logistic -q sd -q dt
echo MAKING PREDICTIONS
vw --binary -t -i data.model -p data.te.pred data.te
echo GETTING READABLE FORMAT
vw -i data.model -t --invert_hash data.model.readable data.tr --quiet
cat data.model.readable  | tail -n+13 | sort -t: -k3nr | head -n30