./build/naive.distinct.csv: ./naive/counter.py
	time head -n 100 words.txt | python2.7 $< - --counter distinct > $@

./build/naive.duplicates.csv: ./naive/counter.py
	time head -n 100 words.txt | python2.7 $< - --counter duplicates > $@

splits:= 2.csv 3.csv 4.csv 5.csv 6.csv 7.csv 8.csv 9.csv 10.csv 11.csv 12.csv 13.csv 14.csv 15.csv 16.csv 17.csv
naive_splits_build:= $(addprefix ./build/split/,$(splits))
$(naive_splits_build): ./split/counter.sh
	time head -n 100 words.txt | ./split/counter.sh $(splits)
# hi
nsb: $(naive_splits_build)

./build/feedback.distinct.csv: ./feedback/counter.py
	time head -n 100 words.txt | python2.7 $< - --counter distinct > $@

./build/feedback.duplicates.csv: ./feedback/counter.py
	time head -n 100 words.txt | python2.7 $< - --counter duplicates > $@

./build/feedback.positional.csv: ./feedback/counter.py
	time head -n 100 words.txt | python2.7 $< - --counter positional > $@
