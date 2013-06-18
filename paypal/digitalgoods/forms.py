from django import forms
from django.utils.safestring import mark_safe
from paypal.digitalgoods.conf import *
from django.conf import settings
from paypal.digitalgoods.widgets import ValueHiddenInput, ReservedValueHiddenInput

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
    item_number = forms.CharField(widget=ValueHiddenInput())
    quantity = forms.CharField(widget=ValueHiddenInput())
    
    
    # IPN control.
    notify_url = forms.CharField(widget=ValueHiddenInput())
    cancel_return = forms.CharField(widget=ValueHiddenInput())
    return_url = forms.CharField(widget=ReservedValueHiddenInput(attrs={"name":"return"}))
    custom = forms.CharField(widget=ValueHiddenInput())
    invoice = forms.CharField(widget=ValueHiddenInput())
    
    # Default fields.
    cmd = forms.ChoiceField(widget=forms.HiddenInput(), initial='')
    charset = forms.CharField(widget=forms.HiddenInput(), initial="utf-8")
    currency_code = forms.CharField(widget=forms.HiddenInput(), initial="USD")
    no_shipping = forms.ChoiceField(widget=forms.HiddenInput(), choices=SHIPPING_CHOICES, 
        initial=SHIPPING_CHOICES[0][0])

    def __init__(self, button_type="buy", *args, **kwargs):
        super(PaypalDGForm, self).__init__(*args, **kwargs)
        self.button_type = button_type

    def render(self):
        return mark_safe(u"""<script src="https://www.paypalobjects.com/js/external/dg.js"></script>
        <script>
        var dg = new PAYPAL.apps.DGFlow({
        trigger:"submitBtn",
        expType: "instant"
        });
        </script>
        <form action="%s" method="post">
    %s
    <input type="image" src="%s" border="0" name="submit" alt="Buy it Now" />
</form>""" % (POSTBACK_ENDPOINT, self.as_p(), self.get_image()))
        
        
    def sandbox(self):
        return mark_safe(u"""<script src="https://www.paypalobjects.com/js/external/dg.js"></script>
        <script>
        var dg = new PAYPAL.apps.DGFlow({
        trigger:"submitBtn",
        expType: "instant"
        });
        </script>
        <form action="%s" method="post">
    %s
    <input type="image" id="submitBtn" src="%s" border="0" name="submit" alt="Buy it Now" />
</form>""" % (SANDBOX_POSTBACK_ENDPOINT, self.as_p(), self.get_image()))
        
    def get_image(self):
        return DG_IMAGE
