help:
	@echo "   install      to install StartAppSync"
	@echo "   uninstall    to uninstall StartAppSync"
	@echo "   clean        to clean build files"
	@echo "   test         to run tests"
	@echo "   deploy       to deploy new version on github and pypi"

test:
	@echo "Run all tests"
	@echo "---------"
	@echo ""
	@echo "Run API tests"
	@python tests/configo_tests.py
	@echo ""
	@echo "Run CLI tests"
	@python tests/configo_executable_tests.py

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
