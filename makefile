exe:	main.cpp
	python main.py

run:
	python main.py

r:
	python main.py

pull:
	git pull

push:
	git push https://github.com/dgforck1/OOADBoardGame

commit:
	git commit -a

add:
	git add -A

push_all:
	git add -A
	git commit -a
	git push https://github.com/dgforck1/OOADBoardGame

force_pull:
	git reset --hard HEAD
	git pull
