setup: requirements.txt
	pip install -r requirements.txt

run:
	python main.py $(FILE)

clean:
	rm -rf __pycache__