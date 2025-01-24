from flask import request
from flask_restful import Resource
from api import db
from api.model.user import User as UserModel  # Assuming your model is in a file named models.py
from api.model.result import Result as ResultModel
from sqlalchemy.exc import IntegrityError  # To handle any database integrity errors
from werkzeug.security import generate_password_hash  # Optional, if you use it for hashing passwords
import datetime
from flask_jwt_extended import create_access_token
from api.utils.GlobalFunc import GLobalFun

class Signup(Resource):
    def post(self):
        try:
            # Get the data from the request body
            data = request.get_json()

            # Ensure all required fields are present
            name = data.get('name')
            email = data.get('email')
            password = data.get('password')

            if not name or not email or not password:
                return {
                    'Data': None,
                    'message': "Name, email, and password are required fields.",
                    'StatusCode': 400
                }

            # Check if the user already exists with the given email
            if UserModel.find_by_email(email):
                return {
                    'Data': None,
                    'message': "A user with this email already exists.",
                    'StatusCode': 409
                }

            # Register the new user
            user = UserModel.register(name=name, email=email, password=password)

            # Return success response
            return {
                'Data': None,
                'message': "User registered successfully!",
                'StatusCode': 200
            }

        except IntegrityError as e:
            db.session.rollback()  # Rollback the session in case of error
            return {
                'Data': None,
                'message': f"Database error: {str(e)}",
                'StatusCode': 500
            }
        except Exception as e:
            return {
                'Data': None,
                'message': str(e),
                'StatusCode': 500
            }


class Login(Resource):
    def post(self):
        try:
            # Get the data from the request body
            data = request.get_json()

            # Ensure email and password are provided
            email = data.get('email')
            password = data.get('password')

            if not email or not password:
                return {
                    'Data': None,
                    'message': "Email and password are required fields.",
                    'StatusCode': 400
                }

            # Find user by email
            user = UserModel.find_by_email(email)

            if not user:
                return {
                    'Data': None,
                    'message': "Invalid email or password.",
                    'StatusCode': 401
                }
            
            # Check if the provided password matches the stored hash
            if not UserModel.verify_hash(password, user.password):
                return {
                    'Data': None,
                    'message': "Invalid email or password.",
                    'StatusCode': 401
                }

            # Secret key for encoding JWT (should be kept secure in real production applications)
            secret_key = 'your_secret_key_here'

            access_token = create_access_token(
                identity=[user.email, user.UserId],  # You can use user-specific data here
                expires_delta=datetime.timedelta(minutes=30)  # after an hour token will be expire 
                # expires_delta=False  # Optional: False means no expiration time, you can define a timedelta instead
            )

            return {
                'Data': {
                    'id': user.UserId,
                    'name': user.name,
                    'token': access_token
                },
                'message': "Login successful!",
                'StatusCode': 200
            }

        except Exception as e:
            print('Login Error: ',e)
            return {
                'Data': None,
                'message': 'Something went wrong!',
                'StatusCode': 500
            }
        
class UserData(Resource):
    def get(self,user_id):
        try:
            get_response = GLobalFun.token_verification()

            if get_response is not None and 'StatusCode' in get_response and get_response['StatusCode'] in [401]:
                return get_response, 401
            
            user = UserModel.find_by_userId(int(user_id))
            if not user:
                return {
                    'Data': None,
                    'message': "Invalid user id.",
                    'StatusCode': 401
                }
            
            get_user_data = ResultModel.get_by_userid(user_id)
            user_data = []


            if not get_user_data:
                return {
                    'Data': None,
                    'message': "No records found!",
                    'StatusCode': 401
                }
            
            for data in get_user_data:
                user_data.append({'id': data.id,'name': user.name,'age': data.age,'score':data.score,'createdAt': data.created_at.strftime('%Y-%m-%d %H:%M:%S')})

            return {
                'Data': user_data,
                'message': "Data fetch successful!",
                'StatusCode': 200
            }

        except Exception as e:
            print('Login Error: ',e)
            return {
                'Data': None,
                'message': 'Something went wrong!',
                'StatusCode': 500
            }
    