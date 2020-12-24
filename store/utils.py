from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type


class AppTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, customer , timestamp):
        return (text_type(customer.is_active)+text_type(customer.pk)+text_type(timestamp))

token_generator=AppTokenGenerator()