#!/bin/bash

#single model for all the languages
#tags in input and output
#adding artificial half items

#get steps
stepsline=$(grep train_steps big.yaml)
steps=${stepsline/train_steps: /}

#master training and validation files
touch BIG_src-train.txt
touch BIG_src-val.txt
touch BIG_tgt-train.txt
touch BIG_tgt-val.txt
mkdir testfiles

for lang in ady gre ice ita khm lav mlt_latn rum slv wel_sw
do
	echo $lang
	#make train/val/test files
	python mfinal.py $lang
	sed "s/^/$lang /" src-val.txt >> BIG_src-val.txt
	rm src-val.txt
	sed "s/^/$lang /" src-train.txt >> BIG_src-train.txt
	rm src-train.txt
	sed "s/^/$lang /" tgt-val.txt >> BIG_tgt-val.txt
	rm tgt-val.txt
	sed "s/^/$lang /" tgt-train.txt >> BIG_tgt-train.txt
	rm tgt-train.txt
	#test files
	sed "s/^/$lang /" src-test.txt > testfiles/${lang}_src-test.txt
	rm src-test.txt
done

#make directory
mkdir /workspace/big
#move files
mv BIG* /workspace/big/
mv testfiles /workspace/
#make vocab
onmt_build_vocab \
	-n_sample 7000 \
	-config big.yaml
#train
onmt_train -config big.yaml

for lang in ady gre ice ita khm lav mlt_latn rum slv wel_sw
do
	#translate/test
	onmt_translate \
		-model /workspace/big/run/model_step_$steps.pt \
		-src /workspace/testfiles/${lang}_src-test.txt \
		-output /workspace/testfiles/${lang}_pred_$steps.txt \
		-gpu 0 \
		-log_file logtest.log \
		--replace_unk \
		-verbose
	#create res file
	sed "s/$lang //" /workspace/testfiles/${lang}_pred_$steps.txt > tempres.txt
	paste 2021-task1-main/data/low/${lang}_test.txt \
		tempres.txt > res-$lang.txt
	rm tempres.txt
done

#cleanup
rm -r /workspace/testfiles/
rm -r /workspace/big/

#evaluate res files
./2021-task1-main/evaluation/evaluate_all.py res*

