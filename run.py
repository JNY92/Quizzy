from flask import Flask
from app import vfquiz_bp
from models import db

app = Flask(__name__)
app.config.from_object("config")
app.register_blueprint(artemis_bp, url_prefix='/artemis')
db.init_app(app)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False

if __name__ == "__main__":
    app.run(debug=False)
