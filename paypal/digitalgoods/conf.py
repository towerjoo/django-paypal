from django.conf import settings
from django.core.urlresolvers import reverse

class PayPalSettingsError(Exception):
    """Raised when settings be bad."""
    

TEST = getattr(settings, "PAYPAL_TEST", True)


RECEIVER_EMAIL = settings.PAYPAL_RECEIVER_EMAIL


# API Endpoints.
#POSTBACK_ENDPOINT = "https://www.paypal.com/cgi-bin/webscr"
#SANDBOX_POSTBACK_ENDPOINT = "https://www.sandbox.paypal.com/cgi-bin/webscr"
POSTBACK_ENDPOINT = settings.SITE_DOMAIN + "/__paypal/dg/"
SANDBOX_POSTBACK_ENDPOINT = POSTBACK_ENDPOINT

# Images
DG_IMAGE = getattr(settings, "PAYPAL_DG_IMAGE", "https://www.paypal.com/en_US/i/btn/btn_dg_pay_w_paypal.gif")

