# Note on how to make a release
```bash
$ vim viznet/version.py
$ python setup.py bdist_wheel
$ twine upload dist/*
```
