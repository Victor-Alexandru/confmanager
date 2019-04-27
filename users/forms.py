from django import forms


class RegisterForm(forms.Form):
    email=forms.EmailField(label="Email",max_length=32,required=True)
    name=forms.CharField(label="Name",max_length=32,required=True)
    password=forms.CharField(widget=forms.PasswordInput,label="Password",min_length=8,max_length=32,required=True)
    website=forms.CharField(label="Website",max_length=32,required=True)
    affiliation=forms.CharField(label="Affiliation",max_length=32,required=True)
    register_as=forms.ChoiceField(label="Register as",choices=(
        ('Participant','Participant'),
        ('Steering','Steering')
    ),required=True)


class LoginForm(forms.Form):
    email=forms.EmailField(label="Email address",max_length=32,required=True)
    password=forms.CharField(widget=forms.PasswordInput,min_length=8,max_length=32,required=True)
    login_as=forms.ChoiceField(label="Login as",choices=(
        ('Participant','Participant'),
        ('Steering','Steering')
    ),required=True)

class ConferenceForm(forms.Form):
    pass