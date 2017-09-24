import tornado.ioloop
import tornado.web
import logging
import json
import os.path
import sys
from tornado.options import define, options
from tornado import gen
import motor.motor_tornado
from logging.config import dictConfig
from tornadoes import ESConnection

from validators.input_validator import InputValidator
from generators.slug_generator import SlugGenerator

def make_app():
    es_index = "feed"

    client = motor.motor_tornado.MotorClient("mongodb://mongodb:27017")
    db = client.test

    es = ESConnection("elasticsearch", 9200)

    handlers = [
        (r"/", MainHandler),
        (r"/news/new", NewsCreateHandler),
        (r"/news/create", NewsCreateHandler),
        (r"/news/search", NewsSearchHandler),
        (r"/news/([^/]+)", NewsShowHandler),
    ]
    settings = dict(
        template_path = os.path.join(os.path.dirname(__file__), "templates"),
        static_path = os.path.join(os.path.dirname(__file__), "static"),
        xsrf_cookies = True,
        cookie_secret = "__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
        debug = True,
        db = db,
        es = es,
        es_index = es_index
    )

    return tornado.web.Application(handlers, **settings)


class MainHandler(tornado.web.RequestHandler):
    @gen.coroutine
    def get(self):
        db = self.settings["db"]

        cursor = db.news.find().sort("_id", -1)
        news = yield cursor.to_list(length=20)
        total_count = yield cursor.count()

        self.render("news.html", news = news, total_count = total_count)

class NewsSearchHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("news_search.html", news = [])

    @tornado.web.asynchronous
    def post(self):
        es = self.settings["es"]
        es_index = self.settings["es_index"]

        text_query = self.get_argument("text_query")
        query = { "query": { "match" : { "_all" : text_query } } }

        es.search(
            callback=self.callback,
            index=es_index,
            type="news",
            source=query
        )

    @gen.coroutine
    def callback(self, response):
        result = json.loads(response.body)["hits"]["hits"]

        result_ids = []

        for item in result:
            result_ids.append(item["_id"])

        db = self.settings["db"]
        cursor = db.news.find({ "_id": { "$in": result_ids }})
        news = yield cursor.to_list(length=20)

        self.render("news_search.html", news = news)


class NewsShowHandler(tornado.web.RequestHandler):
    @gen.coroutine
    def get(self, slug):
        db = self.settings["db"]

        news = yield db.news.find_one({ "slug": slug })

        self.render("news_show.html", news = news)


class NewsCreateHandler(tornado.web.RequestHandler):
    @gen.coroutine
    def get(self):
        self.render("news_new.html")

    def post(self):
        db = self.settings["db"]

        input_data = InputValidator(
            title = self.get_argument("title"),
            image = self.get_argument("image"),
            body = self.get_argument("body")
        )

        if input_data.valid():
            self.document = {
                "title": self.get_argument("title"),
                "slug": SlugGenerator(self.get_argument("title")).generate(),
                "image": self.get_argument("image"),
                "body": self.get_argument("body")
            }

            db.news.insert_one(self.document, callback = self.on_create)
            self.redirect("/")
        else:
            self.set_status(400)
            self.render("news_new.html", errors=input_data.errors)

    def on_create(self, result, error):
        if error is None:
            es = self.settings["es"]
            es_index = self.settings["es_index"]

            document = {
                "title": self.document["title"],
                "body": self.document["body"]
            }

            # TODO: Consider this will be OK for now
            es.put(es_index, "news", result.inserted_id, document)


if __name__ == "__main__":
    app = make_app()
    tornado.options.parse_command_line()
    app.listen(8888)

    tornado.ioloop.IOLoop.current().start()
