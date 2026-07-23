
from django import forms

from django.contrib.auth.models import User

from django.contrib.auth.forms import UserCreationForm

from .models import (
    Ticket,
    Message
)



# ==========================
# User Registration Form
# ==========================

class RegisterForm(UserCreationForm):


    email = forms.EmailField(

        required=True,

        widget=forms.EmailInput(

            attrs={

                "class": "form-control",

                "placeholder": "Enter email address"

            }

        )

    )



    class Meta:


        model = User


        fields = [

            "username",

            "email",

            "password1",

            "password2",

        ]



    def __init__(self, *args, **kwargs):


        super().__init__(*args, **kwargs)



        self.fields["username"].widget = forms.TextInput(

            attrs={

                "class": "form-control",

                "placeholder": "Enter username"

            }

        )



        self.fields["password1"].widget = forms.PasswordInput(

            attrs={

                "class": "form-control",

                "placeholder": "Enter password"

            }

        )



        self.fields["password2"].widget = forms.PasswordInput(

            attrs={

                "class": "form-control",

                "placeholder": "Confirm password"

            }

        )



        # Remove default help text

        self.fields["password1"].help_text = ""

        self.fields["password2"].help_text = ""





# ==========================
# Ticket Form
# ==========================

class TicketForm(forms.ModelForm):


    class Meta:


        model = Ticket


        fields = [

            "subject",

            "description",

        ]



        widgets = {


            "subject": forms.TextInput(

                attrs={

                    "class": "form-control",

                    "placeholder":
                    "Enter ticket subject"

                }

            ),



            "description": forms.Textarea(

                attrs={

                    "class": "form-control",

                    "rows": 6,

                    "placeholder":
                    "Describe your issue in detail..."

                }

            ),

        }



        labels = {


            "subject": "Subject",


            "description": "Description"

        }



    def clean_subject(self):


        subject = self.cleaned_data.get(
            "subject"
        )


        if not subject or len(subject.strip()) < 5:


            raise forms.ValidationError(

                "Subject must contain at least 5 characters."

            )


        return subject





    def clean_description(self):


        description = self.cleaned_data.get(
            "description"
        )


        if not description or len(description.strip()) < 10:


            raise forms.ValidationError(

                "Description must contain at least 10 characters."

            )


        return description





# ==========================
# Chat Message Form
# ==========================

class MessageForm(forms.ModelForm):


    class Meta:


        model = Message


        fields = [

            "content"

        ]



        widgets = {


            "content": forms.Textarea(

                attrs={

                    "class": "form-control",

                    "rows": 3,

                    "placeholder":
                    "Type your message..."

                }

            )

        }



        labels = {

            "content": ""

        }



    def clean_content(self):


        content = self.cleaned_data.get(
            "content"
        )


        if not content or len(content.strip()) == 0:


            raise forms.ValidationError(

                "Message cannot be empty."

            )


        return content