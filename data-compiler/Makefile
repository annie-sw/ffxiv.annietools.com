FBS_ROOT := ../external/flatbuffers
FLATC := $(FBS_ROOT)/flatc
PYTHON3 := python3

FBS_FILES := $(shell find fbs -type f)
JS_OUT := ../frontend/src/assets/generated
PYTHON_OUT := generated

DATA_OUT := ../frontend/static/data

.PHONY: all
all: $(FLATC) data-clean
	mkdir -p $(JS_OUT)
	mkdir -p $(PYTHON_OUT)
	mkdir -p $(DATA_OUT)
	# $(FLATC) -o $(JS_OUT) -I fbs --js --no-js-exports $(FBS_FILES)
	$(FLATC) -o $(JS_OUT) -I fbs --js $(FBS_FILES)
	$(FLATC) -o $(PYTHON_OUT) -I fbs --python $(FBS_FILES)
	$(PYTHON3) main.py $(DATA_OUT)

.PHONY: data-clean
data-clean:
	rm -rf $(JS_OUT)
	rm -rf $(PYTHON_OUT)
	rm -rf $(DATA_OUT)

$(FLATC):
	cd ../external/flatbuffers && cmake -G "Unix Makefiles" && make
