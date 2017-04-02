# -*- coding: UTF-8 -*-
# @file   server
# @author zh1995
# @date   17-4-1
# @brief

import os
import sys
import handler
import logging.config
import tornado.ioloop
from tornado.options import define, options

sys.path.append(os.getcwd())

logging.config.fileConfig(r'config/logging.conf')

define("port", default=10101, help="run on the given port", type=int)

settings = {
    'debug': True
}

handlers = [
    (r"/user/login", handler.login_handler.LoginHandler),
    (r"/user/register", handler.register_handler.RegisterHandler),
]

if __name__ == "__main__":
    application = tornado.web.Application(handlers=handlers, **settings)
    application.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()