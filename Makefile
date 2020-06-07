.PHONY: clean build publish patch minor major

clean:
	find . -type f -name '*.pyc' -delete

build:
	python setup.py sdist bdist_wheel

publish:
	twine upload dist/*

patch:
	bumpversion patch

minor:
	bumpversion minor

major:
	bumpversion major