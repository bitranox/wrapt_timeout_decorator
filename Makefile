## create virtual environment
## see: https://earthly.dev/blog/python-makefile/
venv:
	echo "ToDo - MakeFile is still in Development, contact bitranox@gmail.com if You need it"
	## virtualenv venv

## install all needed for development
develop: venv
	echo "ToDo - MakeFile is still in Development, contact bitranox@gmail.com if You need it"
	## venv/bin/python3 -m pip install -e . -r requirements_test.txt
	## venv/bin/python3 -m pip install -e . -r requirements.txt

test:
	echo "ToDo - MakeFile is still in Development, contact bitranox@gmail.com if You need it"

install:
	echo "ToDo - MakeFile is still in Development, contact bitranox@gmail.com if You need it"

## clean the development environment
clean:
	echo "ToDo - MakeFile is still in Development, contact bitranox@gmail.com if You need it"
	## -rm -rf venv

uninstall:
	echo "ToDo - MakeFile is still in Development, contact bitranox@gmail.com if You need it"
	## -rm -rf venv

## ideas - create make targets for "normal" installation and virtual environments,
## and to be able to pass the virtual environment directory alternatively
## not a priority now, since there are many other ways to install this package
## see: https://earthly.dev/blog/python-makefile/
