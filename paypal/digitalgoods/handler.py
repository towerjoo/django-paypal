from django.conf import settings
import logging
class Paypal:
    def __init__(self, is_sandbox=settings.PAYPAL_SANDBOX):
        self.is_sandbox = is_sandbox
        if self.is_sandbox:
            self.paypal_host = "https://www.sandbox.paypal.com/cgi-bin/webscr"
            self.nvp_host = "https://api-3t.sandbox.paypal.com/nvp"
        else:
            self.paypal_host = "https://www.paypal.com/cgi-bin/webscr"
            self.nvp_host = "https://api-3t.paypal.com/nvp"

    def verify_ipn(self, post_data):
        """post data is gotten from the request.POST passed from django's request
        """
        is_valid_receiver = True if post_data.get("receiver_email") == settings.PAYPAL_RECEIVER else False
        if not is_valid_receiver:
            logging.error("paypal got a wrong receiver_email %s", post_data.get("receiver_email"))
            return False, {}
        cmd = "cmd=_notify-validate&"
        import urllib2, re
        # post back to validate
        if not post_data:
            logging.error("Post data from paypal is none, check the button form")
            return False, {}
        req = urllib2.urlopen(self.paypal_host, cmd + post_data.urlencode())
        ret = req.read()
        if_match = re.search("VERIFIED", ret, re.I)
        if if_match is None:
            # error handling
            logging.error("We got a fail message from paypal, %s", ret)
            return False, {}
        else:
            # data should return the related payment data to the caller, like uid, amount, etc.
            data = {}
            custom = post_data.get("custom")
            uid, appid = custom.split("|")
            data.update({
                "amount" : post_data.get("payment_gross"),
                "uid" : uid,
                "appid" : appid,
                "currency" : post_data.get("mc_currency"),
            })
            return True, data

    def urldecode(self, url):
        import urllib
        data = url.split("&")
        ret = {}
        for d in data:
            key, value = d.split("=")
            ret.update({urllib.unquote(key) : urllib.unquote(value)})
        return ret

    def call_paypal(self, data):
        data.update({
            "user" : settings.PAYPAL_WPP_USER,
            "pwd" : settings.PAYPAL_WPP_PASSWORD,
            "signature" : settings.PAYPAL_WPP_SIGNATURE,
            "version" : settings.PAYPAL_WPP_VERSION,
        })
        logging.info(data)
        import urllib, urllib2, os
        rh = urllib2.urlopen(self.nvp_host, urllib.urlencode(data))
        cont = rh.read()
        ret = self.urldecode(cont)
        if ret.get("ACK").lower() == "success":
            return True, ret
        else:
            return False, ret

    def error_handle(self, error):
        """error is the response from paypal
        """
        if settings.DEBUG:
            import os
            myfile = open(os.path.join(settings.ROOT_PATH, "myfile.log"), "a+")
            error += "\n"
            myfile.write(error)
            myfile.close()
        else:
            pass


paypal_handler = Paypal()
