all: page/src/data/albumy.json

page/src/data/albumy.json: dist/albumy.json
	@echo "Moving data to webpage..."
	cp dist/albumy.json page/src/data/
	cp dist/*.jpg page/public/

dist/albumy.json: data/albumy.json
	@echo "Fetching album covers..."
	python3 cover/cover/main.py

data/albumy.json: data/albumy.org
	@echo "Generating json from org-mode file..."
	python3 parser/album_list_parser/main.py --out data/albumy.json data/albumy.org

clean:
	@echo "Cleaning up..."
	rm -f data/albumy.json
	rm -f dist/albumy.json
