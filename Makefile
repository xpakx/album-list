YEARS := albumy
OUTPUTS := $(patsubst %,dist/%.json,$(YEARS))

all: $(OUTPUTS)
#	@echo "Cleaning..."
#	python3 cleaner/cleaner/main.py

dist/%.json: data/%.json
	@echo "Fetching album covers for $*..."
	python3 cover/cover/main.py --out dist/$*.json data/$*.json

data/%.json: data/%.org
	@echo "Generating json from org-mode file for $*..."
	python3 parser/album_list_parser/main.py --out data/$*.json data/$*.org

clean:
	@echo "Cleaning up..."
	rm -f data/albumy.json
	rm -f dist/albumy.json
