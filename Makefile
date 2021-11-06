
install:
	if [ ! -d .venv ]; then virtualenv -p `which python3` .venv; fi; \
	. .venv/bin/activate; \
	pip install -r requirements.txt; \
	deactivate

run:
	. .venv/bin/activate; \
	python script.py; \
	deactivate
