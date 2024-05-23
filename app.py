from web_api import createApp

if __name__ == "__main__":
    app = createApp()
    app.run(host=app.my_conf.HOST, port=app.my_conf.PORT)