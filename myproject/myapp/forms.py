from django import forms
from .models import Employee


class EmployeeForm(forms.ModelForm):
    # User model fields
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)
    first_name = forms.CharField(max_length=150)
    last_name = forms.CharField(max_length=150)

    class Meta:
        model = Employee
        fields = [
            "username",
            "password",
            "first_name",
            "last_name",
            "employee_id",
            "phone",
            "address",
            "gender",
            "department",
            "designation",
            "salary",
            "joining_date",
            "status",
        ]