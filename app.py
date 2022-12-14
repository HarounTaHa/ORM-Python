import json
from model import Model
from field import *
from database import Database
from http.server import SimpleHTTPRequestHandler, HTTPServer

Model.db = Database('database.sqlite')
Model.connection = Model.db.connect()

PORT = 8000


class Post(Model):
    title = CharField()
    body = TextField()
    created_at = DateTimeField()
    published = BooleanField()


class User(Model):
    first_name = CharField()
    last_name = CharField(max_length=255)
    age = IntegerField()


if __name__ == '__main__':
    class MyHandler(SimpleHTTPRequestHandler):
        def do_GET(self) -> None:
            if self.path == '/posts':
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(Post.all()).encode('utf-8'))
            else:
                post_id = int(self.path.split('/')[-1])
                result = Post.get(post_id)
                if result is False:
                    self.send_response(404)
                    self.wfile.write(b'Not Found')
                    return
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(Post.get(post_id)).encode('utf-8'))


    with HTTPServer(("", PORT), MyHandler) as httpd:
        print("Serving at port", PORT)
        httpd.serve_forever()
