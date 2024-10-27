from odoo import models, fields, api
import random
import string
from datetime import datetime, timedelta

class OTPVerification(models.Model):
    _name = 'otp.verification'
    _description = 'OTP Verification'

    email = fields.Char(required=True)
    otp = fields.Char(required=True)
    expiration = fields.Datetime(string='Expiration')

    @api.model
    def generate_otp(self, email):
        """Generate a random 6-digit OTP and set expiration time."""
        otp = ''.join(random.choices(string.digits, k=6))
        expiration_time = datetime.now() + timedelta(minutes=5)  # OTP expires in 5 minutes
        self.create({'email': email, 'otp': otp, 'expiration': expiration_time})
        return otp