from flask import Flask
from routes.Note import home_blueprint,notes_blueprint


app = Flask(__name__)

@app.route("/ping")
def ping():
    return {"message": "pong"}

app.register_blueprint(home_blueprint) 
app.register_blueprint(notes_blueprint, url_prefix="/api/notes")


if __name__ == "__main__":
    app.run(debug=True)
