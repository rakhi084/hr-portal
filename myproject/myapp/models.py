# from django.db import models
# from django.contrib.auth.models import User
# # Create your models here.
# class HR(models.Model):
#     user = models.OneToOneField(
#         User,
#         on_delete=models.CASCADE,
#         related_name="hr_profile"
#     )

#     phone = models.CharField(max_length=15)
#     department = models.CharField(max_length=100)
#     designation = models.CharField(max_length=100)

#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.user.get_full_name() or self.user.username
    
# class Employee(models.Model):
#     GENDER_CHOICES = (
#         ('Male', 'Male'),
#         ('Female', 'Female'),
#         ('Other', 'Other'),
#     )

#     user = models.OneToOneField(
#         User,
#         on_delete=models.CASCADE,
#         related_name="employee_profile"
#     )

#     hr = models.ForeignKey(
#         HR,
#         on_delete=models.SET_NULL,
#         null=True,
#         related_name="employees"
#     )

#     employee_id = models.CharField(max_length=20, unique=True)

#     phone = models.CharField(max_length=15)
#     address = models.TextField()

#     gender = models.CharField(
#         max_length=10,
#         choices=GENDER_CHOICES
#     )

#     department = models.CharField(max_length=100)
#     designation = models.CharField(max_length=100)

#     salary = models.DecimalField(
#         max_digits=10,
#         decimal_places=2
#     )

#     joining_date = models.DateField()

#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.employee_id} - {self.user.get_full_name()}"


from django.db import models
from django.contrib.auth.models import User


# ============================
# HR MODEL
# ============================

class HR(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="hr_profile"
    )

    phone = models.CharField(max_length=15)

    department = models.CharField(max_length=100)

    designation = models.CharField(max_length=100)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.get_full_name() or self.user.username


# ============================
# EMPLOYEE MODEL
# ============================

class Employee(models.Model):

    GENDER_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    )

    STATUS_CHOICES = (
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
    )

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="employee_profile"
    )

    hr = models.ForeignKey(
        HR,
        on_delete=models.SET_NULL,
        null=True,
        related_name="employees"
    )

    employee_id = models.CharField(
        max_length=20,
        unique=True
    )

    phone = models.CharField(max_length=15)

    address = models.TextField()

    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES
    )

    department = models.CharField(max_length=100)

    designation = models.CharField(max_length=100)

    salary = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    joining_date = models.DateField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Active'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.employee_id} - {self.user.get_full_name()}"


# ============================
# LEAVE MODEL
# ============================

class Leave(models.Model):

    LEAVE_TYPES = (
        ('Casual', 'Casual'),
        ('Sick', 'Sick'),
        ('Vacation', 'Vacation'),
    )

    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    )

    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name="leaves"
    )

    leave_type = models.CharField(
        max_length=20,
        choices=LEAVE_TYPES
    )

    start_date = models.DateField()

    end_date = models.DateField()

    reason = models.TextField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Pending'
    )

    applied_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.employee.employee_id} - {self.leave_type}"