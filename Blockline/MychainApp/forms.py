from django import forms
# from Mychain.models import Person


class LoginForm(forms.Form):
    """description of class"""
    username = forms.CharField(max_length = 25)
    password = forms.CharField(widget = forms.PasswordInput())
    # checkbox = forms.CharField(widget = forms.CheckboxInput())

    def clean_message(self):
        username = self.cleaned_data.get('username')
        dbuser = Person.objects.filter(name = username)

        if not dbuser:
            raise forms.ValidationError('User does not exist')
        return username



class TransactionData(forms.Form):
    receiver = forms.CharField(max_length=10)
    sender = forms.CharField(max_length=10)
    amount = forms.CharField()
    id = forms.CharField(max_length=12)
    data = forms.CharField(max_length=100)
    ''' 
    def send_json(self):
        jdata = self.cleaned_data['receiver', 'sender', 'amount']
        try:
            json_data = json.loads(jdata)
        except:
            raise forms.FieldError('Invalid data')
        return jdata
    '''

class RegisterNode(forms.Form):
    node = forms.CharField(max_length=50)



  