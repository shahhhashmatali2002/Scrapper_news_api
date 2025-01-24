from flask_restful import Resource
from flask import request
from datetime import datetime, date
from api.utils.theNewsArticle import TheNewsArticle
# from dateutil.parser import parse

class NewsArticleProcess(Resource):
    def post(self):
        try:
            data = request.get_json()

            city = data['city']
            # Assume you have a date in dd-mm-yyyy format
            date_str = data['date']

            # # Convert the string to a datetime object using the original format
            # date_obj = parse(date_str)

            # # Convert the datetime object to the desired format (yyyy-mm-dd)
            # formatted_date = date_obj.strftime("%d-%m-%Y")
            formatted_date = date_str
            
            try:
                news_articles = TheNewsArticle.scrape_news(formatted_date,city)
            except Exception as e:
                print(f'Error: {e}')

            if len(news_articles) > 0:
                return {
                    'Data': {'date': formatted_date,'articles': news_articles,'city': city},
                    'message': "News Articles Fetched successfully!",
                    'StatusCode': 200
                }
            
            else:
                return {
                    'Data': None,
                    'message': "Something went wrong!",
                    'StatusCode': 500
                }

        except Exception as e:
            print(f"Error: {e}")
            print(f'len of articles news {len(news_articles)} in error exception')
            return {
                'Data': None,
                'message': str(e),
                'StatusCode': 500
            }