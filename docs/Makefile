BUILD_DIR = ./_build
SRC_DIR = ../src

all: docs src-browser

docs:
	jupyter-book build -W -n --keep-going .

src-browser:
	ford -d $(SRC_DIR) -o $(BUILD_DIR)/html/src FORD_options.md

.PHONY: clean

clean:
	jupyter-book clean .