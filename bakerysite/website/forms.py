from django import forms

from storage.models import Changes
from storage.models import ChangedItem

class ChangesForm(forms.ModelForm):


    class Meta:
        model = ChangedItem
        fields = ('changes', )

    def __init__(self, item=None, **kwargs):
        super(ChangesForm, self).__init__(**kwargs)
        if item:
            self.fields['changes'].queryset = Changes.objects.filter(item=item)
