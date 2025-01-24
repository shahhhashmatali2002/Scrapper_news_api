from flask_restful import Resource


class TestingRoutes(Resource):
    def get(self):
        return {'data': 'Hello world'}
    