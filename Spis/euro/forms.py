from django import forms

from .models import EuroAuchanNames

class EAForm(forms.ModelForm):

    class Meta:
        model = EuroAuchanNames
        fields = ('euro_name', 'auchan_name', 'pol_num')