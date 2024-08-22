all: data/albumy.json

data/albumy.json: data/albumy.org
	@echo "Generating json from org-mode file..."
	python3 parser/album_list_parser/main.py --out data/albumy.json data/albumy.org

clean:
	@echo "Cleaning up..."
	rm -f data/albumy.json
