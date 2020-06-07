.PHONY: clean build publish

clean:
	find . -type f -name '*.pyc' -delete

build:
	python setup.py sdist bdist_wheel

publish:
	twine upload dist/*