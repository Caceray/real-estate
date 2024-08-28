from django import forms

from cash_flows.models import Rent, Charge, Loan, Acquisition

class BaseForm(forms.ModelForm):
  def __init__(self, *args, **kwargs):
    super(BaseForm, self).__init__(*args, **kwargs)
    for field_name, field in self.fields.items():
      if isinstance(field.widget, (forms.TextInput, forms.DateInput)):
        current_classes = field.widget.attrs.get('class', '')
        field.widget.attrs["class"] = f"{current_classes} user-input".strip()
        field.widget.attrs["wrapper_class"] = "form-group"
      else:
        raise TypeError(f"Unexpected widget [{type(field.widget)}] for field [{field_name}]")

class AcquisitionForm(BaseForm):
  class Meta:
    model = Acquisition
    fields = '__all__'
    widgets = {"nominal": forms.TextInput(attrs={"class": "currency-input"}),
               "fees": forms.TextInput(attrs={"class": "currency-input"}),
               "start":forms.DateInput(attrs={"type": "date"})}

    labels = {"nominal":"Prix d'achat",
              "fees":"Frais d'acqusition",
              "start":"Date d'achat"}

class RentForm(BaseForm):
  class Meta:
    model = Rent

    fields = '__all__'
    exclude = ["dataframe"]

    widgets = {"rent": forms.TextInput(attrs={'class': 'currency-input'}),
               "start":forms.DateInput(attrs={"type": "date"}),
               'broker_fees': forms.TextInput(attrs={"class": 'currency-input',}),
               "warranty": forms.TextInput(attrs={"class": "rate-input"}),
               "inflation": forms.TextInput(attrs={"class": "rate-input"})}
    
    labels = {"rent":"Loyer mensuel",
              "warranty":"Assurance GLI",
              "start":"Date mise en location",
              "broker_fees":"Frais de mise en location"}

class ChargeForm(BaseForm):
  class Meta:
    model = Charge

    fields = '__all__'
    exclude = ["start","end"]

    widgets = {"property_tax": forms.TextInput(attrs={'class': 'currency-input'}),
               "waste_collection_tax": forms.TextInput(attrs={'class': 'currency-input'})}

    labels = {"property_tax":"Taxe foncière",
              "waste_collection_tax":"Taxe ordures ménagères"}
    
class LoanForm(BaseForm):
  class Meta:
    model = Loan
    fields = '__all__'
    widgets = {"nominal": forms.TextInput(attrs={'class': 'currency-input'}),
               "start":forms.DateInput(attrs={"type": "date"}),
               "rate":forms.TextInput(attrs={"class": "rate-input"}),
               "duration":forms.TextInput(attrs={"type": "period"})}

    labels = {"rate":"Taux",
              "duration":"Durée (années)",
              "start":"Date de déblocage des fonds"}
