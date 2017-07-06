from flask import Flask
import settings

#Flask App
app = Flask(__name__)
app.config.from_object(settings)

@app.route('/enermod/')
def index():
    return "EnerMod"

if __name__ == "__main__":
    try:
        app.run(host=settings.SERVER_HOST, port=settings.SERVER_PORT)
    except KeyboardInterrupt:
        pass