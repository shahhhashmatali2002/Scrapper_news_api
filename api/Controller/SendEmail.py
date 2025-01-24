from flask_restful import Resource
from flask import request
from flask_mail import Message
from api import mail

class SendEmail(Resource):
    def post(self):
        try:
            data = request.get_json()

            name = data.get('name')
            email = data.get('email')
            message = data.get('message')

            # Send email to the admin (you) with the user's contact info
            admin_msg = Message(
                subject=f"New Message from {name}",
                recipients=['brainbridging3@gmail.com'],  # Admin email
                body=f"Name: {name}\nEmail: {email}\nMessage: {message}"  # User's message content
            )

            # Send a thank-you email to the user
            thank_you_msg = Message(
                subject="Thank you for contacting us",
                recipients=[email],  # User's email address
                body=f"Dear {name},\n\nThank you for reaching out to us. We have received your message and will get back to you soon.\n\nBest regards,\nBrain Bridging"
            )

            try:
                # Send both emails
                mail.send(admin_msg)
                mail.send(thank_you_msg)
                return {
                    'Data': None,
                    'message': 'Thank you for contacting us! A confirmation email has been sent.',
                    'StatusCode': 200
                }
            except Exception as e:
                 print("Error sending email: {e}")
                 return {
                    'Data': None,
                    'message': 'Something went wrong!',
                    'StatusCode': 200
                }
        
        except Exception as e:
            print("Error: {e}")
            return {
                'Data': None,
                'message': str(e),
                'StatusCode': 500
            }