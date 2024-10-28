from odoo import http
from odoo.http import request
from datetime import datetime


class OTPController(http.Controller):

    @http.route('/generate_otp', methods=["POST"], type="json", auth='public')
    def generate_otp(self, email):
        # Generate OTP and store it
        # import wdb;wdb.set_trace()

        otp = request.env['otp.verification'].generate_otp(email)
        
        # Send email
        mail = request.env['mail.mail'].create({
            'subject': 'Your OTP Code',
            'body_html': f'<p>Your OTP is: <strong>{otp}</strong>. It expires in 5 minutes.</p>',
            'email_to': email,
            'email_from': request.env.user.email or 'noreply@example.com',
        })
        mail.send()

        return {'status': 'success', 'message': 'OTP sent to email'}

    @http.route('/verify_otp', type='json', auth='public')
    def verify_otp(self, email, otp):
        otp_record = request.env['otp.verification'].sudo().search([
            ('email', '=', email),
            ('otp', '=', otp),
            ('expiration', '>', datetime.now())
        ], limit=1)
        
        if otp_record:
            return {'status': 'success', 'message': 'OTP verified successfully'}
        else:
            return {'status': 'error', 'message': 'Invalid or expired OTP'}