from flask import Flask
from flask_restful import Api, Resource, reqparse
from flask_cors import CORS

app = Flask(__name__)
api = Api(app)
CORS(app)

test_post_args = reqparse.RequestParser()
test_post_args.add_argument("name", type=str, help="what's your name")
test_post_args.add_argument("age", type=int, help="how many times have you revolved")
test_post_args.add_argument("likes", type=str, help="what are some of the things you like")

class TestResource(Resource):
    def get(self, token_samp):
        return {"samp": "Hello World"}
    def post(self, token_samp):
        args = test_post_args.parse_args()
        return {"example": args}

api.add_resource(TestResource, "/testMeh/<int:token_samp>")

if __name__ == '__main__':
    app.run(debug=True)