from pyexpat import model
from random import choices
from attr import fields
from django import forms
from matplotlib import widgets
from .models import Homework, Notes, Todo

class NotesForm(forms.ModelForm):
    class Meta:
        model = Notes
        fields = ["Title",
            "Description"
        ]

class DateInput(forms.DateInput):
    input_type = "date"

class HomeworkForm(forms.ModelForm):
    class Meta:
        model = Homework
        widgets = {"Due":DateInput()}
        fields = ["Subject", 
            "Title", 
            "Description", 
            "Due", 
            "Is_Finished"
        ]
class YoutubeForm(forms.Form):
    search = forms.CharField(max_length=50, required=False, label = "Enter your search title here:")

class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ["Title",
                "Is_finished"
        ]

class ConversionForm(forms.Form):
    CHOICES = [('length', 'Length'), ('mass', 'Mass')]
    measurement = forms.ChoiceField(choices=CHOICES, widget= forms.RadioSelect)

class ConversionLengthForm(forms.Form):
    CHOICES = [('yard', 'Yard'), ('foot', 'Foot')]
    input = forms.CharField(required = False, label= False, widget = forms.TextInput(
        attrs={"placeholder": "Enter your number",'type': 'number'}
    ))
    measurement1 = forms.CharField(
        widget= forms.Select(choices=CHOICES), label=""
    )
    measurement2 = forms.CharField(
        widget= forms.Select(choices=CHOICES), label=""
    )
class ConversionMassForm(forms.Form):
    CHOICES = [('pound', 'Pound'), ('kilogram', 'Kilogram')]
    input = forms.CharField(required=False, label = False, widget=forms.TextInput(
        attrs= {'placholder':'Enter your desired int value', 'type':'number'}
    ))
    measurement1 = forms.CharField(
        widget= forms.Select(choices=CHOICES), label= ""
    )
    measurement2 = forms.CharField(
        widget= forms.Select(choices=CHOICES), label= ""
    )
