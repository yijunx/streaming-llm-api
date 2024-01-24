# streaming-llm-api

Bring it up and running:
* starting up the flask websocket server with gunicorn `gunicorn -b 0.0.0.0:5000 --workers 4 --threads 100 app.flask_socket:app`
* mock that user send in questions like `how to play bass`, via `python app/llm.py question1 "how to play bass"` and `python app/llm.py question2 "how to play piano"`

How it works
* In this app folder, there are 2 backends (at least we need to image we have 2 backends)
* first backend is the `app/flask_socket.py`, this is the backend which allows browser to establish websocket with, and this backend listens to rabbitmq.
* the second backend is the `app/llm.py`, this is the backend which answer user's question like `how to play piano`, and then, stream the steamed response from openai to rabbitmq, then it will be consumed by the flask socket backend (which listens to the rabbitmq)

Why doing this
* well user does not want to wait for the whole response to be generated, then send to user. 
* openai start to response after 1 seconds, and finish at 3 seconds for question like `how to play piano`. 
* so if we dont stream, user has to wait for 3 seconds!. (well you can observe the log when you trigger the `app/llm.py`)
