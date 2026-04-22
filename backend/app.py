from flask import Flask, jsonify
from flask_cors import CORS
from config import Config
from db import get_db

from routes.auth import auth_bp
from routes.services import services_bp
from routes.portfolio import portfolio_bp
from routes.blog import blog_bp
from routes.contact import contact_bp
from routes.booking import booking_bp

app = Flask(__name__)
app.config.from_object(Config)
CORS(app, resources={r"/api/*": {"origins": app.config['ALLOWED_ORIGINS']}})

# Register blueprints
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(services_bp, url_prefix='/api/services')
app.register_blueprint(portfolio_bp, url_prefix='/api/portfolio')
app.register_blueprint(blog_bp, url_prefix='/api/blog')
app.register_blueprint(contact_bp, url_prefix='/api/contact')
app.register_blueprint(booking_bp, url_prefix='/api/bookings')

@app.route('/')
def index():
    return {'message': 'DevelopersHub API is running!', 'version': '1.0.1'}

@app.errorhandler(Exception)
def handle_exception(e):
    # Log the full error but return a clean JSON response
    # In a real production app, you'd use a logging library here
    print(f"Server Error: {str(e)}")
    return jsonify({
        "error": "Internal Server Error",
        "message": "An unexpected error occurred. Please try again later."
    }), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
