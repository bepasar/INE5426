# testado no Python versões 3.8.10 e 3.6.9

setup: requirements.txt
	pip install -r requirements.txt

run:
	python main.py $(FILE)

clean:
	rm -rf __pycache__