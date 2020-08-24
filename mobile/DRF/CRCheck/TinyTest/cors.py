from rest_framework.response import Response as response

class CorsMiddleware(object):
    def process_response(self, req, resp):
        response["Access-Control-Allow-Origin"] = "*"
        return response