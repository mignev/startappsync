help:
	@echo "   install      to install StartAppSync"
	@echo "   uninstall    to uninstall StartAppSync"
	@echo "   clean        to clean build files"
	@echo "   test         to run tests"
	@echo "   deploy       to deploy new version on github and pypi"

test:
	@echo "Run all tests"
	@echo "---------"
	@nosetests --rednose

install:
	@echo "Installing"
	@sudo python setup.py install --record installed_files.txt

uninstall: clean
	@cat installed_files.txt | xargs sudo rm -rf
	@sudo rm installed_files.txt

clean:
	@sudo rm -rf StartAppSync.egg*
	@sudo rm -rf dist
	@sudo rm -rf build
	@find . -name *.pyc -type f -exec rm {} \;

deploy:
	@git push
	@python setup.py sdist upload
