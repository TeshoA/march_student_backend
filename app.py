from flask import Flask

from routes import initialize_routes
from flask_cors import CORS

# create the Flask application
app = Flask(__name__)
CORS(app)

# used to sign cookies to protect against data tampering
app.config['SECRET_KEY'] = 'Hello from the secret world of Flask! ;)'

initialize_routes(app)

if __name__ == "__main__":
    app.run(debug=True)
