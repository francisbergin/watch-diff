version := $(shell python3 -c "import watch_diff;print(watch_diff.__version__)")

.PHONY: build clean tests release

clean:
	rm -rf build dist watch_diff.egg-info

build:
	python setup.py sdist bdist_wheel

test:
	python -m unittest -v

release: clean build tests
	git commit -am v$(version)
	git tag -s v$(version) -m v$(version)
	git push && git push --tags
	twine upload dist/*
