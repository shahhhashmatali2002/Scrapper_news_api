"""
    @author Agha Hammad Raza
    @abstract API endpoints
    @since 06-07-2024
"""

from api import app, api

# ----------{ Controller Imports }----------
import api.Controller.TestingRoutes as TestingRoutes

import api.Controller.NewsArticleProcess as NewsArticleProcess

# Register API resources
api.add_resource(TestingRoutes.TestingRoutes, "/api/testing-api", endpoint="testing-api")

api.add_resource(NewsArticleProcess.NewsArticleProcess, '/api/news-article',endpoint="news-article")



if __name__ == "__main__":
    with app.app_context():
        app.run(debug=True, host="0.0.0.0", port=5000)
