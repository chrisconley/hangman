lengths:= 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 27 28

splits:= $(addprefix ./build/splits/,$(lengths))
$(splits): ./words.txt ./splitter.py
	python2.7 ./splitter.py ./words.txt ./build/splits
splits: $(splits)

naive_counts: $(addprefix ./build/naive/,$(lengths))
./build/naive/%: ./build/splits/% ./naive/counter.py
	python2.7 ./naive/counter.py $< > $@

clean:
	rm -rf ./build
	mkdir -p ./build/splits
	mkdir -p ./build/naive

.PHONY : split

#time make naive_counts -j4