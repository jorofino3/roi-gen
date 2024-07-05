# Variables
JAVAC = javac
JAVAC_FLAGS = -d bin

# Source files
SRC_DIR = src
SRC_FILES = $(wildcard $(SRC_DIR)/**/*.java) $(wildcard $(SRC_DIR)/*.java)

# Build target
all: $(SRC_FILES)
	$(JAVAC) $(JAVAC_FLAGS) $(SRC_FILES) 

clean:
	rm -rf bin

.PHONY: clean