# streaming-llm-api

Step 0:
reopen in devcontainer

Bring it up and running:
* starting up the flask websocket server with gunicorn `gunicorn -b 0.0.0.0:5000 --workers 4 --threads 100 app.flask_socket:app`, this is a service which establish websocket with backend. and the backend listens to rabbitmq.
* Starting up the another backend which actually receives the question, `python another_backend.py`.
* Using your browser to open localhost:5000 to observe the streaming words comming back from flask_socket (which streamed from rabbitmq, which put there by another_backend streamingly)

How it works
* In this app folder, there are 2 backends
* first backend is the `app/flask_socket.py`, this is the backend which allows browser to establish websocket with, and this backend listens to rabbitmq.
* the second backend is the `another_backend.py`, this is the backend which answer user's question like `how to play piano`, and then, stream the steamed response from openai to rabbitmq (`app/llm.py`), then it will be consumed by the flask socket backend (which listens to the rabbitmq)

Why doing this
* well user does not want to wait for the whole response to be generated, then send to user. 
* openai start to response after 1 seconds, and finish at 3 seconds for question like `how to play piano`. 
* so if we dont stream, user has to wait for 3 seconds!. (well you can observe the log when you trigger the `app/llm.py`)

How it can be implemeted to production environments
