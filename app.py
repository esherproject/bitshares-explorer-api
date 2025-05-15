import connexion
from flask_cors import CORS
import logging
import services.limiter
from services.cache import cache
import services.profiler

logging.basicConfig()

# Optional: Swagger UI available at http://<host>:5000/apidocs/
options = {
    'swagger_url': '/apidocs'
}

# Create the Connexion app
app = connexion.App(__name__, specification_dir='swagger', options=options)

# Enable CORS
CORS(app.app)

# Initialize Flask extensions
cache.init_app(app.app)
limiter = services.limiter.init(app.app)
services.profiler.init_app(app.app)

# Use the official BitShares OpenAPI spec
app.add_api("openapi.yaml", strict_validation=True, validate_responses=True)

# Entry point for WSGI server (e.g. gunicorn)
application = app.app

# Local dev runner
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
