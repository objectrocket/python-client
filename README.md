[![Circle CI](https://circleci.com/gh/objectrocket/python-client.svg?style=svg)](https://circleci.com/gh/objectrocket/python-client)
[![codecov.io](http://codecov.io/github/objectrocket/python-client/coverage.svg?branch=master)](http://codecov.io/github/objectrocket/python-client?branch=master)
[![Coverage Status](https://coveralls.io/repos/objectrocket/python-client/badge.svg?branch=master&service=github)](https://coveralls.io/github/objectrocket/python-client?branch=master)

ObjectRocket Python Client
==========================
ObjectRocket API interface library for Python.

**NOTICE:** this client is still undergoing intial stages of development, and some public interfaces may change as development continues. We will increment the version of this package to 1.0.0 once the public interface to this library is deemed stable.

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
```bash
pip install objectrocket
```

### development
#### test
Testing against local you will want to export a couple environment variables:

```bash
export OR_DEFAULT_API_URL='http://localhost:5050/v2/'
export OR_DEFAULT_ADMIN_API_URL='http://localhost:5050/admin/'
```

Before you push your code, run `tox` from the top level directory. If errors
are reported, fix them.

#### coverage
To receive a test coverage report, run `tox -e coverage` from the top level directory.

#### pypi build
Update version in setup.py
Pushing a tag following the pattern `/^[0-9]+.[0-9]+.[0-9]+$/` will automatically trigger a new version of the client to be built and uploaded to [pypi](https://pypi.python.org). A pattern of `/^[0-9]+.[0-9]+.[0-9]+-rc[0-9]+$/` will cause it to be pushed to [testpypi](https://testpypi.python.org).

#### documentation
To build the documentation, invoke `tox -e docs` from the top level directory.
The HTML index can then be found at `docs/build/html/index.html`.
