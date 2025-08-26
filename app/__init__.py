from flask import Flask

flask_app = Flask(__name__)

# Import routes to register them
import app.routes  # noqa: E402, F401, F811
