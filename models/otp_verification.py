from odoo import models, fields, api
import random
import string
from datetime import datetime, timedelta
from odoo.exceptions import ValidationError

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
    
    @api.model
    def delete_expired_otps(self):
        """Delete OTP records that have expired."""
        expired_otps = self.search([('expiration', '<', datetime.now())])
        if expired_otps:
            expired_otps.unlink()

class MobileOTPVerification(models.Model):
    _name = 'mobile.otp.verification'
    _description = 'Mobile OTP Verification'

    phone_number = fields.Char('Phone Number', required=True)
    otp = fields.Char('OTP')
    is_verified = fields.Boolean('Is Verified', default=False)

    @api.model
    def generate_otp(self, phone_number):
        otp = str(random.randint(100000, 999999))
        self.env['otp.verification'].create({
            'phone_number': phone_number,
            'otp': otp,
        })
        # Replace with your SMS gateway API call
        self.send_sms(phone_number, otp)
        return otp

    def verify_otp(self, phone_number, otp):
        record = self.search([('phone_number', '=', phone_number), ('otp', '=', otp)], limit=1)
        if record:
            record.is_verified = True
            return True
        else:
            raise ValidationError('Invalid OTP')

    def send_sms(self, phone_number, otp):
        # Integrate with your SMS Gateway API here
        print(f"Sending OTP {otp} to {phone_number}")