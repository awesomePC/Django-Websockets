Django-websockets
=================


What this project is about?
---------------------------

This is a simple implementation of REST using Websockets.

Websockets are a way of creating a persistent connections between the client and server. These sockets allow bi-directional data transfer without the need of long-polling or refreshing. Since these are also based on HTTP so only one HTTP request is sent to the server for establishing the connection.

Django-channels are used in this project as a dependency.

There are 3 main actions which a user can do via minimal UI.

1. Start a new request on the server. Takes 3 arguments which are **connid, time and route**

connid -> Specifies the connection ID for a particular request.
time -> Timeout for the request.
route -> Specifies which Consumer should be invoked for handling this request. In this case it is **request**

2. Kill a running request on the server. Takes 2 arguments which are **connid and route**

connid -> Specifies the connection ID for a particular request.
route -> Specifies which Consumer should be invoked for handling this request. In this case it is **kill**

3. Get the status of all the running requests on the server. Takes only 1 argument which is **route**

route -> Specifies which Consumer should be invoked for handling this request. In this case it is **status**

All the communication between the client and server happens over JSON which is also a standard way of communication over the Channels.

Setting up the environment
--------------------------

```bash
$ sudo pip install -r requirements.txt
```


Running the application
-----------------------

```bash
$ redis-server
$ python manage.py runserver
```


API Endpoints
---------------------

### Searching libraries

@api {get} /query/module

@apiParam {String, String} library name and entered text

@apiOutput {String, String, Array} status, message and data array

Example:

```bash
$ curl -X GET -H "Content-Type: application/json" -d '{"lib":["basic_string", "vector"], "text": "push"}' http://127.0.0.1:8000/query/module
```