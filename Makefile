install:
	#install commmands
	pip install -r requirements.txt
format:
	#Format here
	black *.py
lint:
	#Flake8 or pylint
	#pylint --disable=R,C *.py
build:
	#Build container
	#docker build -t wgs .
deploy:
	#deploy
	#docker run -it -d -p 8050:8050 wgs:latest
all: install format lint build deploy
