from django import forms


class PornhubForm(forms.Form):
    url = forms.URLField()
    title = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'placeholder': 'Enter your video link'}),
    )

    class Meta:
        fields = ['url']