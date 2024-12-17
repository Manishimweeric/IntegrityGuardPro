from django.shortcuts import get_object_or_404, redirect,render
from django.contrib import messages
from django.http import HttpResponse
from .models import User,Case
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
def index(request):
    return render(request, 'index.html')

def admin_dashboard(request):
    return render(request, 'admin_dashboard.html')

def investigator_dashboard(request):
    return render(request, 'investigator_dashboard.html')

def reporter_dashboard(request):
    # Check if the user is logged in
    user_id = request.session.get('user_id')
    user_type = request.session.get('user_type')
    user = User.objects.get(id=request.session['user_id'])
    name = request.session["name"]

    if not user_id or user_type != 'reporter':
        messages.error(request, "You need to log in as a reporter to access this page.")
        return redirect('login')

    # Fetch user-specific data
    total_cases = Case.objects.filter(reported_by=user).count()
    cases_under_investigation = Case.objects.filter(reported_by=user, status="Under Investigation").count()
    resolved_cases = Case.objects.filter(reported_by=user, status="Resolved").count()

    context = {
        'total_cases': total_cases,
        'cases_under_investigation': cases_under_investigation,
        'resolved_cases': resolved_cases,
        'name': name,
    }
    return render(request, 'Reporter/reporter_dashboard.html', context)
def login(request):
    return render(request, 'login.html')


def signup(request):
    if request.method == "POST":
        fullname = request.POST.get('fullname')
        address = request.POST.get('address')
        phone_number = request.POST.get('phone_number')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if User.objects.filter(email=email).exists():
            messages.error(request, "This email is already registered.")
            return redirect('signup')
        try:
            EmailValidator()(email)
        except ValidationError:
            messages.error(request, "Invalid email format.")
            return redirect('signup')
        user = User.objects.create(
            fullname=fullname,
            address=address,
            phone_number=phone_number,
            email=email,
            password=password,  
        )
        user.save()
        messages.success(request, "Account created successfully!")
        return redirect('signup')  

    return render(request, 'signup.html')  


def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            # Fetch the user by email
            user = User.objects.get(email=email)

            # Check if the password is correct (using check_password for hashed passwords)
            if (password == user.password):

                   # Store user ID in the session
                request.session['user_id'] = user.id
                request.session['name'] = user.fullname
                request.session['user_type'] = user.user_type

                # Redirect based on the user's role
                if user.user_type == 'admin':
                    return redirect('admin_dashboard')  # Replace with actual admin dashboard URL
                elif user.user_type == 'investigator':
                    return redirect('investigator_dashboard')  # Replace with actual investigator dashboard URL
                elif user.user_type == 'reporter':
                    return redirect('reporter_dashboard')  # Replace with actual reporter dashboard URL
                else:
                    return redirect('home')  # Default redirect, in case the role is not set
            else:
                messages.error(request, "Invalid password.")
                return redirect('login')  # Redirect back to the login page if password is incorrect
        except User.DoesNotExist:
            messages.error(request, "No account found with this email.")
            return redirect('login')  # Redirect back to the login page if email doesn't exist

    return render(request, 'login.html')

def Case_View(request):
    name = request.session["name"]
    return render(request, 'Reporter/Case.html', {'name': name})

def reporter_dashboards(request):
    user = User.objects.get(id=request.session['user_id'])
    name = request.session["name"]
    cases = Case.objects.filter(reported_by=user)  # Assuming a 'user' field exists in the Case model
    return render(request, 'Reporter/DisplayCase.html', {'cases': cases, 'name': name})

def create_case(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        user = User.objects.get(id=request.session['user_id'])

        case = Case.objects.create(
            title=title,
            description=description,
            reported_by=user
        )   
        messages.success(request, 'Your Case has been Reported')
        return render(request, 'Reporter/Case.html')

    return render(request, 'Reporter/case.html', {
        'status_choices': Case.STATUS_CHOICES
    })
def edit_case(request, case_id):
    if request.method == "POST":
        case = get_object_or_404(Case, id=case_id)
        case.title = request.POST.get("title")
        case.description = request.POST.get("description")
        case.details = request.POST.get("details")
        case.save()
        messages.success(request, "Case updated successfully!")
        return redirect("reporter_view")
    
    
from django.shortcuts import redirect
from django.contrib import messages

def logout_view(request):
    # Clear the session
    request.session.flush()
    messages.success(request, "You have been logged out successfully.")
    return redirect('login')  # Replace 'login' with your login page URL name
