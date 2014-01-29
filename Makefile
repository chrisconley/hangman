# ubuntu box needs PYTHONPATH set
# PYTHONPATH=./ make play_naive_split

lengths:= 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 27 28

words: ./build ./build/words.txt
./build/words.txt: ./build ./words.txt
	cat ./words.txt | awk 'BEGIN {srand()} !/^$$/ { if (rand() <= .10) print $$0}' > $@

random_words: ./build ./build/random_words.txt
./build/random_words.txt: ./build/words.txt
	cat ./build/words.txt | awk 'BEGIN {srand()} !/^$$/ { if (rand() <= .10) print $$0}' > $@

splits:= $(addprefix ./build/splits/,$(lengths))
$(splits): ./build/words.txt ./splitter.py
	python2.7 ./splitter.py ./build/words.txt ./build/splits
splits: $(splits)

naive_counts: ./build ./build/naive_counts.csv
./build/naive_counts.csv: ./build/words.txt ./naive/counter.py
	python2.7 ./naive/counter.py $< > $@

naive_split_counts: $(addprefix ./build/naive_split/,$(lengths))
./build/naive_split/%: ./build/splits/% ./naive/counter.py
	python2.7 ./naive/counter.py $< > $@

naive_duplicates_counts: $(addprefix ./build/naive_duplicates/,$(lengths))
./build/naive_duplicates/%: ./build/splits/% ./naive/counter.py
	python2.7 ./naive/counter.py $< --counter duplicates > $@

feedback_distinct_counts: $(addprefix ./build/feedback_distinct/,$(lengths))
./build/feedback_distinct/%: ./build/splits/% ./feedback/counter.py
	python2.7 ./feedback/counter.py $< --counter distinct > $@

feedback_duplicates_counts: $(addprefix ./build/feedback_duplicates/,$(lengths))
./build/feedback_duplicates/%: ./build/splits/% ./feedback/counter.py
	python2.7 ./feedback/counter.py $< --counter duplicates > $@

feedback_positional_counts: $(addprefix ./build/feedback_positional/,$(lengths))
./build/feedback_positional/%: ./build/splits/% ./feedback/counter.py
	python2.7 ./feedback/counter.py $< --counter positional > $@

play_naive: random_words ./build/naive_counts.csv
	cat ./build/random_words.txt | python2.7 ./naive/play.py - ./build/naive_counts.csv

play_naive_split: random_words naive_split_counts
	cat ./build/random_words.txt | python2.7 ./naive/play_split.py - ./build/naive_split/

./build:
	mkdir -p ./build/splits
	mkdir -p ./build/naive_split
	mkdir -p ./build/feedback_distinct
	mkdir -p ./build/feedback_duplicates
	mkdir -p ./build/feedback_positional

clean:
	rm -rf ./build

.PHONY : split

#time make naive_counts -j4
