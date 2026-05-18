from django import forms

from storage.models import Changes, Order

class ChangesForm(forms.Form):
    def __init__(self, *args, **kwargs):
        item = kwargs.pop('item')

        super(ChangesForm, self).__init__(*args, **kwargs)

        if item:
            item_changes = Changes.objects.filter(item=item)
            value_list = item_changes.values_list(
                'component', flat=True
            ).distinct()

            #choices = Changes.options.component.choices

            for value in value_list:
                available = item_changes.filter(component=value)
                display_name = available.first().get_component_display()
                self.fields['custom_%s' % value] = forms.ModelChoiceField(queryset=available, label=display_name, required = True)

class CartForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["delivery_type", "delivery_address", "payment_type"]