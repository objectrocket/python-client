[![Build Status](https://travis-ci.org/objectrocket/python-client.svg)](https://travis-ci.org/objectrocket/python-client)
[![codecov.io](http://codecov.io/github/objectrocket/python-client/coverage.svg?branch=master)](http://codecov.io/github/objectrocket/python-client?branch=master)
[![Coverage Status](https://coveralls.io/repos/objectrocket/python-client/badge.svg?branch=master&service=github)](https://coveralls.io/github/objectrocket/python-client?branch=master)

ObjectRocket Python Client
==========================
ObjectRocket API interface library for Python.


### examples
To use the library, simply do the following:


```python
>>> import objectrocket

>>> client = objectrocket.Client()
>>> client.authenticate('<username>', '<password>')

# Create a new instance.
>>> client.instances.create(name='instance0', size=5, zone='US-West'
<MongodbInstance {...} at 0x10aedb990>

# Get an instances object.
>>> client.instances.get('instance0')
<MongodbInstance {...} at 0x10aedb980>

# Get all instances.
>>> client.instances.all()
[<MongodbInstance {...} at 0x10aedb980>]
```


### installation

    pip install objectrocket


### development
#### test
Before you push your code, run `tox` from the top level directory. If errors
are reported, fix them.

#### coverage
To receive a test coverage report, run `tox -e coverage` from the top level directory.

#### build
To build the client, invoke `tox -e build` from the top level directory.
Your artifact will appear in the `dist` directory, and will look
something like `objectrocket-<version>-py2.py3-<abi>-<platform>.whl`.

#### documentation
To build the documentation, invoke `tox -e docs` from the top level directory.
The HTML index can then be found at `docs/build/html/index.html`.
