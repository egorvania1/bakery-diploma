from django import forms

from storage.models import Changes

class ChangesForm(forms.Form):
    def __init__(self, item=None, **kwargs):
        super(ChangesForm, self).__init__(**kwargs)

        if item:
            item_changes = Changes.objects.filter(item=item)
            value_list = item_changes.values_list(
                'component', flat=True
            ).distinct()

            for value in value_list:
                #get_component_display()
                self.fields['custom_%s' % value] = forms.ModelChoiceField(queryset=item_changes.filter(component=value), label=value)
