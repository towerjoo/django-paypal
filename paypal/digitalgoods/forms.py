from django import forms
from django.utils.safestring import mark_safe
from paypal.digitalgoods.conf import *
from django.conf import settings
from paypal.digitalgoods.widgets import ValueHiddenInput, ReservedValueHiddenInput
from paypal.digitalgoods.handler import paypal_handler

class PaypalDGForm(forms.Form):
    DG = "digitalgoods"

    CMD_CHOICES = (
        ("_xclick", "Buy now or Donations"), 
        ("_cart", "Shopping cart"), 
        ("_xclick-subscriptions", "Subscribe")
    )
    
    SHIPPING_CHOICES = ((1, "No shipping"), (0, "Shipping"))
    NO_NOTE_CHOICES = ((1, "No Note"), (0, "Include Note"))
    RECURRING_PAYMENT_CHOICES = (
        (1, "Subscription Payments Recur"), 
        (0, "Subscription payments do not recur")
    )
    REATTEMPT_ON_FAIL_CHOICES = (
        (1, "reattempt billing on Failure"), 
        (0, "Do Not reattempt on failure")
    )

    # Where the money goes.
    business = forms.CharField(widget=ValueHiddenInput(), initial=RECEIVER_EMAIL)
    
    # Item information.
    amount = forms.IntegerField(widget=ValueHiddenInput())
    item_name = forms.CharField(widget=ValueHiddenInput())
    #item_number = forms.CharField(widget=ValueHiddenInput())
    #quantity = forms.CharField(widget=ValueHiddenInput())
    
    
    # IPN control.
    notify_url = forms.CharField(widget=ValueHiddenInput())
    cancel_return = forms.CharField(widget=ValueHiddenInput())
    return_url = forms.CharField(widget=ValueHiddenInput())
    invoice = forms.CharField(widget=ValueHiddenInput())
    
    # Default fields.
    #cmd = forms.ChoiceField(widget=forms.HiddenInput(), initial='')
    charset = forms.CharField(widget=forms.HiddenInput(), initial="utf-8")
    currency_code = forms.CharField(widget=forms.HiddenInput(), initial="USD")
    no_shipping = forms.ChoiceField(widget=forms.HiddenInput(), choices=SHIPPING_CHOICES, 
        initial=SHIPPING_CHOICES[0][0])

    def render(self):
        return mark_safe(u"""
        <form action="%s" method="post">
    %s
    <input type="image" src="%s" id="submitBtn" border="0" name="submit" alt="Buy it Now" />
    </form>
    <script src="https://www.paypalobjects.com/js/external/dg.js"></script>
        <script>
        var dg = new PAYPAL.apps.DGFlow({
        trigger:"submitBtn"
        });
        </script>
""" % (POSTBACK_ENDPOINT, self.as_p(), self.get_image()))
        
        
        
    def get_image(self):
        return DG_IMAGE

    def set_express_checkout(self):
        cmd = "SetExpressCheckout"
        config = {
            "PAYMENTREQUEST_0_PAYMENTACTION" : "Sale",
            "PAYMENTREQUEST_0_CURRENCYCODE" : self.cleaned_data.get("currency_code"),
            "RETURNURL" : self.cleaned_data.get("return_url"),
            "CANCELURL" : self.cleaned_data.get("cancel_return"),
            "METHOD" : cmd,
            "PAYMENTREQUEST_0_AMT" : self.cleaned_data.get("amount"),
            "PAYMENTREQUEST_0_ITEMAMT" : self.cleaned_data.get("amount"),
            "L_PAYMENTREQUEST_0_NAME0" : self.cleaned_data.get("item_name"),
            "L_PAYMENTREQUEST_0_AMT0" : self.cleaned_data.get("amount"),
            "L_PAYMENTREQUEST_0_QTY0" : "1",
            "L_PAYMENTREQUEST_0_ITEMCATEGORY0" : "Digital",
            "REQCONFIRMSHIPPING" : "0",
            "NOSHIPPING" : "1",
        }
        flag, ret = paypal_handler.call_paypal(config)
        if flag:
            if settings.PAYPAL_SANDBOX:
                return flag, "https://www.sandbox.paypal.com/incontext?token=" + ret.get("TOKEN")
            else:
                return flag, "https://www.paypal.com/incontext?token=" + ret.get("TOKEN")
        else:
            return flag, ""



