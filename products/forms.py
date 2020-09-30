from django import forms
from .models import Product, Category


class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        exclude = ('sold', 'reserved')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        categories = Category.objects.all()
        friendly_names = [(c.id, c.get_friendly_name()) for c in categories]
        self.fields['category'].choices = friendly_names
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'border-black rounded-0'
        self.fields['image'].label = "Image" \
            " (please use pictures 500px*500px for better results)"
        self.fields['weight'].label = "Weight in grams"
        self.fields['l'].label = "Long in cms"
        self.fields['h'].label = "High in cms"
        self.fields['w'].label = "Wide in cms"
        self.fields['available_quantity'].widget.attrs['min'] = 1
        self.fields['l'].widget.attrs['min'] = 1
        self.fields['h'].widget.attrs['min'] = 1
        self.fields['w'].widget.attrs['min'] = 1
        self.fields['weight'].widget.attrs['min'] = 1
