from django import forms


class UpdateOrderEntry(forms.Form):
    product = forms.IntegerField(label="Add to cart", initial=1, help_text="Add to you shopping cart")
    count = forms.IntegerField(label="Count", initial=1)
