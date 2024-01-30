from flask import Flask, request
from app.llm import answer_question_with_stream
from logging import getLogger


logger = getLogger(__name__)
app = Flask(__name__)


@app.route("/questions", methods=["POST"])
def answer_question():
    question_id = request.json["question_id"]
    question = request.json["question"]

    print(question)
    print(question_id)

    full_answer = answer_question_with_stream(
        question_id=question_id, question=question
    )

    print(full_answer)
    # now save the full answer into db..
    return "answered", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)

"""this is how to test
curl --location 'localhost:5001/questions' \
--header 'Content-Type: application/json' \
--data '{"question_id": "question1", "question": "how to play bass"}'
"""
