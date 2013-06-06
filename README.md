# Python bindings to the Scyld Cloud-Auth API

This is a client for the Scyld Cloud-Auth API.  Scyld Cloud-Auth is created and maintained by [Penguin Computing, Inc.](http://www.penguincomputing.com).

## Quickstart

```python
>>> from cloudauthclient.v1.client import Client
>>> authclient = Client(endpoint=URL, api_key=KEY, api_secret=SECRET)
>>> authclient.token
'du2kJvRI1Ah7Me63aDNQnObl84CPcS0j'
```
