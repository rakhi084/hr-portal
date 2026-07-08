from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Count

from .models import HR, Employee, Leave
from .forms import EmployeeForm


# ==========================
# Login
# ==========================

def login_view(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            if HR.objects.filter(user=user).exists():
                return redirect("hr_dashboard")

            elif Employee.objects.filter(user=user).exists():
                return redirect("employee_dashboard")

    return render(request, "login.html")


# ==========================
# HR Dashboard
# ==========================

@login_required
def hr_dashboard(request):

    hr = get_object_or_404(HR, user=request.user)

    employees = Employee.objects.filter(hr=hr)

    total_employee = employees.count()

    departments = employees.values(
        "department"
    ).distinct().count()

    pending_leave = Leave.objects.filter(
        employee__hr=hr,
        status="Pending"
    ).count()

    approved_leave = Leave.objects.filter(
        employee__hr=hr,
        status="Approved"
    ).count()

    recent_employees = employees.order_by("-created_at")[:5]

    pending_leaves = Leave.objects.filter(
        employee__hr=hr,
        status="Pending"
    ).select_related(
        "employee",
        "employee__user"
    )[:5]

    department_distribution = employees.values(
        "department"
    ).annotate(
        total=Count("id")
    )

    context = {

        "total_employee": total_employee,
        "departments": departments,
        "pending_leave": pending_leave,
        "approved_leave": approved_leave,
        "employees": recent_employees,
        "pending_leaves": pending_leaves,
        "department_distribution": department_distribution,

    }

    return render(request, "hr_dashboard.html", context)


# ==========================
# Employee Dashboard
# ==========================

@login_required
def employee_dashboard(request):

    employee = Employee.objects.get(user=request.user)

    total_leave = Leave.objects.filter(
        employee=employee
    ).count()

    pending_leave = Leave.objects.filter(
        employee=employee,
        status="Pending"
    ).count()

    approved_leave = Leave.objects.filter(
        employee=employee,
        status="Approved"
    ).count()

    recent_leaves = Leave.objects.filter(
        employee=employee
    ).order_by("-applied_at")[:5]

    context = {

        "employee": employee,

        "total_leave": total_leave,

        "pending_leave": pending_leave,

        "approved_leave": approved_leave,

        "recent_leaves": recent_leaves

    }

    return render(
        request,
        "employee_dashboard.html",
        context
    )


# ==========================
# Add Employee
# ==========================

@login_required
def add_employee(request):

    if request.method == "POST":

        form = EmployeeForm(request.POST)

        if form.is_valid():

            user = User.objects.create_user(

                username=form.cleaned_data["username"],
                password=form.cleaned_data["password"],
                first_name=form.cleaned_data["first_name"],
                last_name=form.cleaned_data["last_name"]

            )

            employee = form.save(commit=False)

            employee.user = user
            employee.hr = HR.objects.get(user=request.user)

            employee.save()

            return redirect("employee_list")

    else:

        form = EmployeeForm()

    return render(
        request,
        "add_employee.html",
        {
            "form": form
        }
    )


# ==========================
# View Employees
# ==========================

@login_required
def employee_list(request):

    hr = HR.objects.get(user=request.user)

    employees = Employee.objects.filter(hr=hr)

    return render(
        request,
        "employee_list.html",
        {
            "employees": employees
        }
    )


# ==========================
# Edit Employee
# ==========================

@login_required
def edit_employee(request, id):

    employee = get_object_or_404(Employee, id=id)

    if request.method == "POST":

        employee.user.first_name = request.POST.get("first_name")
        employee.user.last_name = request.POST.get("last_name")
        employee.user.username = request.POST.get("username")
        employee.user.save()

        employee.employee_id = request.POST.get("employee_id")
        employee.phone = request.POST.get("phone")
        employee.address = request.POST.get("address")
        employee.gender = request.POST.get("gender")
        employee.department = request.POST.get("department")
        employee.designation = request.POST.get("designation")
        employee.salary = request.POST.get("salary")
        employee.joining_date = request.POST.get("joining_date")
        employee.status = request.POST.get("status")

        employee.save()

        return redirect("employee_list")

    return render(
        request,
        "edit_employee.html",
        {
            "employee": employee
        }
    )


# ==========================
# Delete Employee
# ==========================

@login_required
def delete_employee(request, id):

    employee = get_object_or_404(Employee, id=id)

    employee.user.delete()

    return redirect("employee_list")

# ==========================
# employee profile
# ==========================
@login_required
def employee_profile(request):

    employee = Employee.objects.get(
        user=request.user
    )

    return render(
        request,
        "employee_profile.html",
        {
            "employee": employee
        }
    )

# ==========================
# Apply Leave
# ==========================
@login_required
def apply_leave(request):

    employee = Employee.objects.get(
        user=request.user
    )

    if request.method == "POST":

        Leave.objects.create(

            employee=employee,

            leave_type=request.POST.get("leave_type"),

            start_date=request.POST.get("start_date"),

            end_date=request.POST.get("end_date"),

            reason=request.POST.get("reason")

        )

        return redirect("leave_history")

    return render(
        request,
        "apply_leave.html"
    )

# ==========================
# Leave History
# ==========================
@login_required
def leave_history(request):

    employee = Employee.objects.get(
        user=request.user
    )

    leaves = Leave.objects.filter(
        employee=employee
    ).order_by("-applied_at")

    return render(
        request,
        "leave_history.html",
        {
            "leaves": leaves
        }
    )



@login_required
def leave_requests(request):

    hr = HR.objects.get(user=request.user)

    leaves = Leave.objects.filter(
        employee__hr=hr,
        status="Pending"
    )

    return render(
        request,
        "leave_requests.html",
        {"leaves": leaves}
    )


@login_required
def approved_leaves(request):

    hr = HR.objects.get(user=request.user)

    leaves = Leave.objects.filter(
        employee__hr=hr,
        status="Approved"
    )

    return render(
        request,
        "approved_leaves.html",
        {"leaves": leaves}
    )


@login_required
def rejected_leaves(request):

    hr = HR.objects.get(user=request.user)

    leaves = Leave.objects.filter(
        employee__hr=hr,
        status="Rejected"
    )

    return render(
        request,
        "rejected_leaves.html",
        {"leaves": leaves}
    )

@login_required
def approve_leave(request, id):

    leave = Leave.objects.get(id=id)

    leave.status = "Approved"

    leave.save()

    return redirect("leave_requests")


@login_required
def reject_leave(request, id):

    leave = Leave.objects.get(id=id)

    leave.status = "Rejected"

    leave.save()

    return redirect("leave_requests")