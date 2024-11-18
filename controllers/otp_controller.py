from odoo import http
from odoo.http import request
from datetime import datetime


class OTPController(http.Controller):

    @http.route('/generate_otp', methods=["POST"], type="json", auth='public')
    def generate_otp(self):
        # Generate OTP and store it
        # import wdb;wdb.set_trace()

        otp = request.env['otp.verification'].sudo().generate_otp(request.httprequest.json['email'])

        
        # Send email
        mail = request.env['mail.mail'].sudo().create({
            'subject': 'Your OTP Code',
            'body_html': f'<p>Your OTP is: <strong>{otp}</strong>. It expires in 10 minutes.</p>',
            'email_to': request.httprequest.json['email'],
            'email_from': 'usman.shaikhnag@esehat.org',
        })
        mail.send()

        return {'status': 'success', 'message': 'OTP sent to email'}

    @http.route('/verify_otp', methods=["POST"], type="json", auth='public')
    def verify_otp(self):
        email = request.httprequest.json['email']
        otp = request.httprequest.json['otp']
        # import wdb;wdb.set_trace()

        otp_record = request.env['otp.verification'].sudo().search([
            ('email', '=', email),
            ('otp', '=', otp),
            ('expiration', '>', datetime.now())
        ], limit=1)
        
        if otp_record:
            return {'status': 'success', 'message': 'OTP verified successfully'}
        else:
            return {'status': 'error', 'message': 'Invalid or expired OTP'}
        
    
    @http.route('/checkEmail', methods=["POST"], type="json", auth='public')
    def checkEmail(self):
        email = request.httprequest.json.get('email')
        
        # Check if email is provided
        # import wdb;wdb.set_trace()

        if not email:
            return {'status': 'error', 'message': 'Email not provided'}, 400  # HTTP 400 for missing data

        # Search for an existing user with the specified email
        existing_user = request.env['res.users'].sudo().search([('login', '=', email)], limit=1)
        
        # Check if the user exists and respond accordingly
        if existing_user:
            return {'status': 'error', 'message': 'Email already exists'}, 409  # HTTP 409 Conflict for duplicate
        return {'status': 'success', 'message': 'Email available'}, 200