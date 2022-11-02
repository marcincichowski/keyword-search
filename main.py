import cgi
import json


class KeywordHandler:
    def __init__(self, keywords, data):
        self.keywords = []
        for keyword in keywords:
            self.keywords.append(keyword.lower())
        self.data = data.lower()

    def find_keywords(self):
        result = []
        for keyword in self.keywords:
            if keyword in self.data:
                result.append(keyword)
        return result


def app(environ, start_response):
    if environ['REQUEST_METHOD'].upper() == 'POST':
        form = cgi.FieldStorage(fp=environ['wsgi.input'], environ=environ)
        try:
            keywords = form['keywords'].value
            data = form['data'].value
        except KeyError:
            response_data = b'MISSING INPUT PARAMS\n'
            status = '400 BAD REQUEST'
        else:
            try:
                data = json.loads(data.value)
            except ValueError:
                response_data = b'INVALID JSON INPUT\n'
                status = '400 BAD REQUEST'
            else:
                handler = KeywordHandler(keywords, data)
                response_data = handler.find_keywords()
                status = "200 OK"
    else:
        response_data = b'FAIL\n'
        status = "405 METHOD NOT ALLOWED"
    response_headers = [
        ('Content-type', 'text/plain'),
        ('Content-Length', str(len(response_data)))
    ]
    start_response(status, response_headers)
    return iter([response_data])
