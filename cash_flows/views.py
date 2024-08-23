from django.shortcuts import render
from cash_flows.forms import RentForm, ChargeForm, LoanForm, AcquisitionForm

from engine.taxes import LocationNue

categories = [AcquisitionForm, RentForm, ChargeForm, LoanForm]

def main_view(request):
    html_input = {}

    if request.method == "POST":
        for category in categories:
            key = category.__name__.replace("Form","").lower()
            form = category(request.POST)
            if form.is_valid():
                instance = form.save(commit=False)
                html_input[key] = form
                if key == "loan":
                    html_input["loan_tab"] = instance.to_html()
                elif key == "rent":
                    html_input["rent_tab"] = instance.to_html(annual=False)
            else:
                print(f"Form {key} is not valid!")
                print(form.errors)

        rent = RentForm(request.POST).save(commit=False).get_object().get_dataframe()
        loan = LoanForm(request.POST).save(commit=False).get_object().get_dataframe()

        import pandas as pd
        df = pd.concat([rent, -loan["Interest"]], axis=1).sort_index()
        print(df)

    else:
        for category in categories:
            key = category.__name__.replace("Form","").lower()
            html_input[key] = category()

    return render(request, 'cash_flows/main_view.html', html_input)
