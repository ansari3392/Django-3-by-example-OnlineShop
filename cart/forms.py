from django import forms

PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]

class CartProductForm(forms.Form):
    quantity = forms.TypeChoiceField(
        choices=PRODUCT_QUANTITY_CHOICES,
        coerce=int
    )
    override = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)
    