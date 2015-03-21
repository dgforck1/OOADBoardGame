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

#removes all the ~ files, which are just backups
cleanup:
	find ./ -name '*.pyc' | xargs rm
	find ./ -name '*~' | xargs rm

#clear all of the records in the database
reset_db:
	mysql --user=root --password=root < Dreadnaught/TTT/sql/reset_db.sql
