# streaming-llm-api

How it works
* In this app folder, there are 2 backends (at least we need to image we have 2 backends)
* first backend is the `app/flask_socket.py`, this is the backend which allows browser to establish websocket with, and this backend listens to rabbitmq.
* the second backend is the `app/llm.py`, this is the backend which answer user's question, and then, stream the steamed response from openai to rabbitmq, then it will be consumed by the flask socket backend (which listens to the rabbitmq)
