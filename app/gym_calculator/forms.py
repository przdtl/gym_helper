from django import forms


class BenchCalculatorForm(forms.Form):
    barbell_weight = forms.CharField(
        widget=forms.NumberInput(
            attrs={'class': "form-control mb-1", 'autofocus': 'true'}),
        max_length=4,
    )

    reps = forms.ChoiceField(
        widget=forms.Select(attrs={'class': 'form-control mb-1'}),
        choices=(
            ((i, str(i + 2)) for i in range(14))
        ),
    )
