from django.urls import path
from . import views

urlpatterns = [

    # Authentication
    path("", views.login_view, name="login"),

    # ================= HR =================

    path("hr/", views.hr_dashboard, name="hr_dashboard"),

    # Employee CRUD
    path("employees/", views.employee_list, name="employee_list"),
    path("employees/add/", views.add_employee, name="add_employee"),
    path("employees/edit/<int:id>/", views.edit_employee, name="edit_employee"),
    path("employees/delete/<int:id>/", views.delete_employee, name="delete_employee"),

    # HR Leave Management
    path("leave-requests/", views.leave_requests, name="leave_requests"),
    path("approved-leaves/", views.approved_leaves, name="approved_leaves"),
    path("rejected-leaves/", views.rejected_leaves, name="rejected_leaves"),

    path("leave/<int:id>/approve/", views.approve_leave, name="approve_leave"),
    path("leave/<int:id>/reject/", views.reject_leave, name="reject_leave"),

    # ================= EMPLOYEE =================

    path("employee/", views.employee_dashboard, name="employee_dashboard"),

    path(
        "employee/profile/",
        views.employee_profile,
        name="employee_profile"
    ),

    path(
        "employee/apply-leave/",
        views.apply_leave,
        name="apply_leave"
    ),

    path(
        "employee/leave-history/",
        views.leave_history,
        name="leave_history"
    ),

]