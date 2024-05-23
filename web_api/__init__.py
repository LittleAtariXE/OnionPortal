import sys
import os
from flask import Flask
sys.path.append(os.path.abspath(os.path.join(os.path.abspath(__file__), "..", "..")))

from onion_portal.onion_portal import OnionPortal
from constructor.constructor import Constructor
from .views import portal

def createApp() -> object:
    app = Flask(__name__)
    app.OnionPortal = OnionPortal(Constructor)
    app.OnionPortal.makeOnions()
    app.config.from_object(app.OnionPortal.serv_conf)
    app.my_conf = app.OnionPortal.serv_conf

    app.register_blueprint(portal, url_prefix="/")

    return app

