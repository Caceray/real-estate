from django.shortcuts import render
from cash_flows.forms import RentForm, ChargeForm, LoanForm, AcquisitionForm

from engine.taxes import LocationNue

categories = [AcquisitionForm, RentForm, ChargeForm, LoanForm]

def extract_form(object, request, *args, **kwargs):
    form = object(request.POST)
    if form.is_valid():
        instance = form.save(commit=False)
        if object == ChargeForm:
            import datetime as dt
            instance.start = dt.date(2024, 1, 1)
            instance.end = dt.date(2026, 12, 1)
        instance.create_dataframe()
        html = instance.to_html()
        df = instance.get_dataframe()
    else:
        print(f"Form {object.__name__.replace('Form','').lower()} is not valid!")
        print(form.errors)

    return form, df, html

def main_view(request):
    html_input = {}

    if request.method == "POST":
        rent_form, rent_df, rent_html = extract_form(RentForm, request)
        loan_form, loan_df, loan_html = extract_form(LoanForm, request)
        charge_form, charge_df, charge_html = extract_form(ChargeForm, request)
        acquisition_form, _, _ = extract_form(AcquisitionForm, request)

        import pandas as pd
        df = pd.concat([rent_df, -loan_df["Interest"]], axis=1).sort_index()

        html_input = {"rent":rent_form,
                      "loan":loan_form,
                      "charge":charge_form,
                      "acquisition":acquisition_form,
                      "rent_tab":rent_html,
                      "loan_tab":loan_html}

        # Compute annual benefits

        # for category in categories:
        #     key = category.__name__.replace("Form","").lower()
        #     form = category(request.POST)
        #     if form.is_valid():
        #         instance = form.save(commit=False)
        #         html_input[key] = form
        #         if key == "loan":
        #             html_input["loan_tab"] = instance.to_html()
        #         elif key == "rent":
        #             html_input["rent_tab"] = instance.to_html(annual=False)
        #     else:
        #         print(f"Form {key} is not valid!")
        #         print(form.errors)

        # rent = RentForm(request.POST).save(commit=False).get_object().get_dataframe()
        # loan = LoanForm(request.POST).save(commit=False).get_object().get_dataframe()

    else:
        for category in categories:
            key = category.__name__.replace("Form","").lower()
            html_input[key] = category()

    return render(request, 'cash_flows/main_view.html', html_input)
