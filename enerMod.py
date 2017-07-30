from flask import Flask, send_from_directory
import settings

#Flask App
app = Flask(__name__, static_url_path='/enermod/assets')
app.config.from_object(settings)

@app.after_request
def adding_header_content(head):
    head.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    head.headers["Pragma"] = "no-cache"
    head.headers["Expires"] = "0"
    head.headers['Cache-Control'] = 'public, max-age=0'
    return head

@app.route('/enermod/')
@app.route('/enermod/<path:path>')
def login(path=''):
    return app.send_static_file('views/login.html')

@app.route('/enermod/home')
def home(path=''):
    return app.send_static_file('views/home.html')

@app.route('/enermod/favicon.ico')
def favicon():
    return app.send_static_file('favicon.ico')

if __name__ == "__main__":
    try:
        app.run(host=settings.SERVER_HOST, port=settings.SERVER_PORT)
    except KeyboardInterrupt:
        pass