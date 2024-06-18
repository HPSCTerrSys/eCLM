BUILD_DIR = ./_build
SRC_DIR = ../src

all: docs linkcheck src-browser

docs:
	jupyter-book build -W .

src-browser:
	ford -d $(SRC_DIR) -o $(BUILD_DIR)/html/src FORD_options.md

linkcheck:
	jupyter-book build . --builder linkcheck

.PHONY: clean

clean:
	jupyter-book clean .