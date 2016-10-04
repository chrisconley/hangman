# ### Overview
#
# This will take the dictionary in ./words.txt and split it into
# files containing words of specific lengths.
#
# ### Usage
#
# make splits

BUILD_DIR = ./build

lengths:= 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 27 28

splits:= $(addprefix ./build/splits/,$(lengths))
$(splits): $(BUILD_DIR) ./words.txt ./splitter.py
	python ./splitter.py ./words.txt ./build/splits
splits: $(splits)

$(BUILD_DIR):
	mkdir -p ./build/splits
	mkdir -p ./build/guesses

clean:
	rm -rf $(BUILD_DIR)

.PHONY : split clean

#time make naive_counts -j4
