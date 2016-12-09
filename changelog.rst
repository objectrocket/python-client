changelog
=========

0.4.x
-----
- New stats endpoint that provides instance stats (for consumption by newrelic)
- Instance details now include instance settings.
- Use ``six`` to allow extensions under py3.
- Require lib elasticsearch >= 2.
- Modify ``Instance.__repr__`` to show only name and id. Less noisy.
- Implement the instance ACLs interface.
- Implement the instance bound ACLs interface.
- Implement the auth._verify method for token verification.
- Allowing instances to be extensible.
- sharded mongodb instance stats are fetched using a pool of threads (one thread per shard)
- Added acl delete functionality

0.3.x
-----
- Implemented the ACL sync interface.

0.2.x
-----
- Allow default API endpoint to be taken from the environment.
- Updates to authentication pattern.
- Built out extension patterns using stevedore.

0.1.x
------
- Initial release with basic API interfacing and object support.
