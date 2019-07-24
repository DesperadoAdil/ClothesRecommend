# -*- coding: UTF-8 -*-
from app import app
from werkzeug.contrib.fixers import ProxyFix

app.wsgi_app = ProxyFix(app.wsgi_app)

app.run(debug = True, host = "0.0.0.0", port = 80)
