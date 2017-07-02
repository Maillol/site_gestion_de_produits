from django import forms
from functools import partial
from django.utils.translation import ugettext_lazy as _


def with_bootstrap_css(field_class):
    return partial(field_class,
                   required=False,
                   widget=field_class.widget(attrs={'class': 'form-control input-sm'}))


CharField = with_bootstrap_css(forms.CharField)
DateField = with_bootstrap_css(forms.DateField)
MultipleChoiceField = with_bootstrap_css(forms.MultipleChoiceField)


class SearchProductForm(forms.Form):

    def __init__(self, storage_area_choices, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['storage_area__in'].choices = storage_area_choices

    number = CharField(label='internal label')
    packaging_product__name__icontains = CharField(label=_('packaging'))
    packaging_product__cas__names__name__icontains = CharField(
        label=_('chemical substance name'))
    packaging_product__cas__cas = CharField(label=_('CAS number'))
    expiration_date__lte = DateField(label=_('expired before'))
    expiration_date__gte = DateField(label=_('expired after'))
    storage_area__in = MultipleChoiceField(label=_('storage area'))

    def destroy_for_superuser_fields(self):
        del self.fields['number']
