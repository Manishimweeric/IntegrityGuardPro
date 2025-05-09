from django.shortcuts import get_object_or_404, redirect,render
from django.contrib import messages
from django.http import HttpResponse
from .models import User,Case,Collabration,ContactMessage
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from .models import Case, Feedback,Evidence
from django.conf import settings
from datetime import datetime, timedelta


def approaching_deadline_cases(request):
    # Check if the user is logged in
    user_id = request.session.get('user_id')
    
    if not user_id:
        messages.error(request, "You need to log in as an investigator to access this page.")
        return redirect('login')
    
    user = User.objects.get(id=request.session['user_id'])
    name = request.session["name"]
    role = request.session["user_type"]
    
    # Calculate the date 25 days ago (to find cases assigned 25+ days ago)
    deadline_threshold = timezone.now() - timedelta(days=25)
    
    # Get cases that are approaching the 1-month mark (5 or fewer days remaining)
    approaching_deadline_cases = Case.objects.filter(
        assigned_to=user,
        created_at__lte=deadline_threshold
    ).order_by('created_at')
    
    # Calculate days remaining for each case
    for case in approaching_deadline_cases:
        # One month from assigned date
        one_month_date = case.created_at + timedelta(days=30)
        # Days remaining until one month
        days_remaining = (one_month_date - timezone.now()).days
        # Ensure we don't show negative days
        case.days_remaining = max(0, days_remaining)
    
    context = {
        'approaching_deadline_cases': approaching_deadline_cases,
        'name': name,
        'role': role,
    }
    
    return render(request, 'investigator/approaching_deadline_cases.html', context)


def index(request):
    return render(request, 'index.html')
def admin_dashboard(request):
    # Fetch user-specific data
    total_cases = Case.objects.count()
    cases_under_investigation = Case.objects.filter(status="under_investigation").count()
    resolved_cases = Case.objects.filter(status="resolved").count()
    pending_cases = Case.objects.filter(status="reported").count()
    name = request.session["name"]
    role = request.session["user_type"]


    # Filter users based on their role
    admin_users = User.objects.filter(user_type='admin').count()
    investigator_users = User.objects.filter(user_type='investigator').count()
    reporter_users = User.objects.filter(user_type='reporter').count()

    # Prepare data for the frontend
    context = {
        'total_cases': total_cases,
        'cases_under_investigation': cases_under_investigation,
        'resolved_cases': resolved_cases,
        'name': name,
        'pending_cases': pending_cases,
        'role': role,
        'admin_users': admin_users,
        'investigator_users': investigator_users,
        'reporter_users': reporter_users,
    }
    return render(request, 'Admin/admin_dashboard.html', context)


from django.utils import timezone
from datetime import timedelta

def investigator_dashboard(request):
    # Check if the user is logged in
    user_id = request.session.get('user_id')
    user_type = request.session.get('user_type')
    
    if not user_id:
        messages.error(request, "You need to log in as a reporter to access this page.")
        return redirect('login')
    
    user = User.objects.get(id=request.session['user_id'])
    name = request.session["name"]
    role = request.session["user_type"]
    
    # Fetch user-specific data
    total_cases = Case.objects.filter(assigned_to=user).count()
    cases_under_investigation = Case.objects.filter(assigned_to=user, status="under_investigation").count()
    resolved_cases = Case.objects.filter(assigned_to=user, status="resolved").count()
    
    # Calculate the date 25 days ago (to find cases assigned 25+ days ago)
    # These cases will reach 1 month in 5 or fewer days
    deadline_threshold = timezone.now() - timedelta(days=28)
    
    # Get cases that are approaching the 1-month mark (5 or fewer days remaining)
    approaching_deadline_cases = Case.objects.filter(
        assigned_to=user,
        status="under_investigation",
        created_at__lte=deadline_threshold
    ).order_by('created_at')
    
    # Calculate days remaining for each case
    for case in approaching_deadline_cases:
        # One month from assigned date
        one_month_date = case.created_at + timedelta(days=30)
        # Days remaining until one month
        days_remaining = (one_month_date - timezone.now()).days
        # Ensure we don't show negative days
        case.days_remaining = max(0, days_remaining)
    
    users = User.objects.filter(user_type="legalAdvisor")
    
    context = {
        'total_cases': total_cases,
        'cases_under_investigation': cases_under_investigation,
        'resolved_cases': resolved_cases,
        'approaching_deadline_cases': approaching_deadline_cases,
        'name': name,
        'users': users,
        'role': role,
    }
    
    return render(request, 'investigator/investigator_dashboard.html', context)

def Legal_Advisor_dashboard(request):
     # Check if the user is logged   in
    user_id = request.session.get('user_id')
    user_type = request.session.get('user_type')
    user = User.objects.get(id=request.session['user_id'])

    name = request.session["name"]
    role= request.session["user_type"]

    # Fetch user-specific data
    total_cases = Case.objects.filter(Legal_assigned_to=user).count()
    cases_under_investigation = Case.objects.filter(Legal_assigned_to=user, status="under_Legal_Advisor").count()
    resolved_cases = Case.objects.filter(Legal_assigned_to=user, status="resolved").count()

    context = {
        'total_cases': total_cases,
        'cases_under_investigation': cases_under_investigation,
        'resolved_cases': resolved_cases,
        'name': name,
        'role': role,
    }
    return render(request, 'Legal/Legal_Dashboard.html',context)


def Internal_Investigator_Dashboard(request):
    user_id = request.session.get('user_id')
    user_type = request.session.get('user_type')
    user = User.objects.get(id=request.session['user_id'])

    name = request.session["name"]
    role= request.session["user_type"]

    # Fetch user-specific data
    total_cases = Case.objects.filter(Legal_assigned_to=user).count()
    cases_under_investigation = Case.objects.filter(internal_Investigator=user, status="under_investigation").count()
    resolved_cases = Case.objects.filter(internal_Investigator=user, status="resolved").count()

    context = {
        'total_cases': total_cases,
        'cases_under_investigation': cases_under_investigation,
        'resolved_cases': resolved_cases,
        'name': name,
        'role': role,
    }

    return render(request, 'Internal/Internal_Dashboard.html',context)




def reporter_dashboard(request):
    # Check if the user is logged   in
    user_id = request.session.get('user_id')
    user_type = request.session.get('user_type')
    user = User.objects.get(id=request.session['user_id'])
    name = request.session["name"]
    role= request.session["user_type"]
    if not user_id or user_type != 'reporter':
        messages.error(request, "You need to log in as a reporter to access this page.")
        return redirect('login')

    # Fetch user-specific data
    total_cases = Case.objects.filter(reported_by=user).count()
    cases_under_investigation = Case.objects.filter(reported_by=user, status="under_investigation").count()
    resolved_cases = Case.objects.filter(reported_by=user, status="resolved").count()
    pending_cases = Case.objects.filter(status="reported").count()

    context = {
        'total_cases': total_cases,
        'cases_under_investigation': cases_under_investigation,
        'resolved_cases': resolved_cases,
        'pending_cases': pending_cases,
        'name': name,
        'role': role,
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
                request.session['email'] = user.email           

                # Redirect based on the user's role
                if user.user_type == 'admin':
                    return redirect('admin_dashboard')  
                elif user.user_type == 'investigator':
                    return redirect('investigator_dashboard')  
                elif user.user_type == 'reporter':
                    return redirect('reporter_dashboard') 
                elif user.user_type == 'legalAdvisor':
                    return redirect('Legal_Dashboard') 
                elif user.user_type == 'internal_Investigator':
                    return redirect('Internal_Investigator_Dashboard')  
                else:
                    return redirect('login')  
            else:
                messages.error(request, "Incorrect Email or password.")
                return redirect('login')  
        except User.DoesNotExist:
            messages.error(request, "No account found with this email.")
            return redirect('login') 

    return render(request, 'login.html')

def Case_View(request):
    name = request.session["name"]
    role= request.session["user_type"]
    return render(request, 'Reporter/Case.html', {'name': name, 'role': role})

def reporter_dashboards(request):
    user = User.objects.get(id=request.session['user_id'])
    name = request.session["name"]
    role= request.session["user_type"]
    status = request.GET.get('status')
    cases = Case.objects.filter(reported_by=user) 
    if status:
        cases = Case.objects.filter(status=status)
    else:
        cases = Case.objects.filter(status="reported")
    return render(request, 'Reporter/DisplayCase.html', {'cases': cases, 'name': name, 'role': role})

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

def edit_cases(request, case_id):
    case = get_object_or_404(Case, id=case_id)

    # Check if the case status is 'REPORTED'
    if case.status != "Reported":
        messages.error(request, "This case cannot be edited because it has moved to the follow-up status.")       
        return redirect("reporter_view")

    if request.method == "POST":
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
    return redirect('login')  

def investigators_view (request):

    name = request.session["name"]
    role= request.session["user_type"]

    context = {
        'name': name,
        'role': role,
    }
    return render(request, 'Admin/CreateInvestigator.html', context)


def investigators_create (request):

    name = request.session["name"]
    role= request.session["user_type"]

    if request.method == "POST":
        fullname = request.POST.get('fullname')
        address = request.POST.get('address')
        phone_number = request.POST.get('phone_number')
        email = request.POST.get('email')
        user_types="investigator"
        password=123456789

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
            user_type=user_types
        )
        user.save()
        messages.success(request, "Account created ")
        return redirect('investigator_view')  

    context = {
        'name': name,
        'role': role,
    }
    return render(request, 'Admin/CreateInvestigator.html', context)

def investigator_List(request):
    name = request.session["name"]
    role= request.session["user_type"]
    cases = Case.objects.all()
    investigators = User.objects.filter(user_type='investigator')
    context = {
        'name': name,
        'role': role,
        'cases': cases,
        'investigators': investigators
    }   
    return render(request, 'Admin/DisplayInvestigator.html', context)


def edit_case(request, case_id):
    case = get_object_or_404(Case, id=case_id)
    investigators = User.objects.all()

    if request.method == 'POST':
        investigator_id = request.POST.get('investigator')
        if investigator_id:
            investigator = User.objects.get(id=investigator_id)
            case.assigned_to = investigator
            case.status="under_investigation"

            # Set the corresponding user's is_active to False
            if case.assigned_to:
                user = investigator
                user.save()

                

            case.save()
            messages.success(request, 'Investigator assigned successfully and user marked as inactive.')
            return redirect('view_all_Cases')
        else:
            messages.error(request, 'Please select an investigator.')

    name = request.session["name"]
    role= request.session["user_type"]
    cases = Case.objects.all()
    investigators = User.objects.filter(user_type='investigator',is_active=True)
    context = {
        'name': name,
        'role': role,
        'cases': cases,
        'investigators': investigators,
    }
    return render(request, 'Admin/DisplayCases.html', context)

def cases_list(request):
    status = request.GET.get('status')
    name = request.session["name"]
    role= request.session["user_type"]
    if status:
        cases = Case.objects.filter(status=status)
    else:
        cases = Case.objects.filter(status="reported")
    
    # Pass the list of investigators if needed
    investigators = User.objects.filter(user_type='investigator')

    context = {
        'name': name,   
        'role': role,
        'cases': cases,
        'investigators': investigators,
    }    
    return render(request, 'Admin/DisplayCases.html',context)

def view_all_Cases (request):
    name = request.session["name"]
    role= request.session["user_type"]
    cases = Case.objects.filter(status="reported")
    investigators = User.objects.filter(user_type='investigator')
    context = {
        'name': name,
        'role': role,
        'cases': cases,
        'investigators': investigators,
    }
    return render(request, 'Admin/DisplayCases.html', context)

def collabration(request):
    name = request.session["name"]
    role= request.session["user_type"]
    email= request.session["email"]
    user = User.objects.filter(user_type="investigator").exclude(email=email)

    context = {
        'name': name,
        'role': role,
        'users': user
    }
    return render(request, 'investigator/Collabration.html', context)

def send_email_view(request):
    user = User.objects.get(id=request.session['user_id'])
    if request.method == "POST":
        email = request.POST.get("email")
        message = request.POST.get("message")
        try:
            user = User.objects.get(email=email)  
        except User.DoesNotExist:
            messages.error(request, "This Investigator email does not exist in our records.")
            return redirect("send_email_view") 
        try:
            send_mail(
                subject="Collaboration Request",
                message=message, 
                from_email="manishimweeric54@gmail.com",
                recipient_list=[email],
                fail_silently=False, 
            )
            Collabor = Collabration.objects.create(
            Reciever_email=email,
            message=message,
            user=user,
            sender_email="manishimweeric54@gmail.com"
            )
            Collabor.save()
            messages.success(request, "Email sent successfully!")
            return redirect("collabration") 
        except Exception as e:
            messages.error(request, f"An error occurred: {e}")
            return redirect("collabration") 

    return redirect("collabration")  

def Messages_view(request):
    name = request.session["name"]
    role= request.session["user_type"]
    user = User.objects.get(id=request.session['user_id'])
    sendingmessages = Collabration.objects.filter(user=user)
    recievedmessages = Collabration.objects.all().exclude(user=user)


    context = {
        'name': name,
        'role': role,
        'sendingmessages': sendingmessages,
        'recievedmessages': recievedmessages,
    }
    return render(request, 'investigator/Message.html', context)

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def Investigetor_Case_views(request):
    name = request.session["name"]
    role = request.session["user_type"]
    user = User.objects.get(id=request.session['user_id'])
    investigators = User.objects.filter(user_type='legalAdvisor')
    internal_Investigator = User.objects.filter(user_type='internal_Investigator')
    status = request.GET.get('status')
    if status:
        cases_list = Case.objects.filter(assigned_to=user, status=status)
    else:
        cases_list = Case.objects.filter(assigned_to=user, status="under_investigation")
    
    page = request.GET.get('page', 1)
    paginator = Paginator(cases_list, 3) 
    
    try:
        cases = paginator.page(page)
    except PageNotAnInteger:
        cases = paginator.page(1)
    except EmptyPage:
        cases = paginator.page(paginator.num_pages)
    
    cases_with_feedback = cases_list.filter(feedbacks__isnull=False)
    context = {
        'name': name,
        'role': role,
        'cases': cases,
        'investigators': investigators,
        'internal_Investigators': internal_Investigator,
        'cases_with_feedback': cases_with_feedback,
    }
    return render(request, 'investigator/CaseAssigned.html', context)


def assigned_case(request, case_id):
    if request.method == "POST":
        user = User.objects.get(id=request.session['user_id'])
        case = get_object_or_404(Case, id=case_id)
        description = request.POST.get("description")
        case.reported = description
        case.status = 'resolved'
        case.save()
        messages.success(request, "Feedback sent successfully!")
        return redirect("investigetor_case")  

    return redirect("investigetor_case") 


def Ligal_assigned_case(request, case_id):
    role = request.session["user_type"]
    if request.method == "POST":
        user = User.objects.get(id=request.session['user_id'])
        case = get_object_or_404(Case, id=case_id)
        user_reported_by=User.objects.get(id=case.reported_by.id)
        description = request.POST.get("description")
        evidence_file = request.FILES.get("evidence_file")
        feedback = Feedback.objects.create(
            case=case,
            feedback_message=description,
            provided_by=user,
            reported_by=user_reported_by,
            reported_role=role
        )

        if evidence_file:
            fs = FileSystemStorage(location=settings.MEDIA_ROOT)
            filename = fs.save(evidence_file.name, evidence_file)
            feedback.feedback_file = filename

        case.status = 'resolved'
        case.save()
        user.is_active = True
        user.save()

        feedback.save()
        messages.success(request, "Feedback sent successfully!")
        return redirect("Legal_case")  

    return redirect("Legal_case")  

def Internal_Investigetor_feedback_case(request, case_id):
    role = request.session["user_type"]
    if request.method == "POST":
        user = User.objects.get(id=request.session['user_id'])
        case = get_object_or_404(Case, id=case_id)
        user_reported_by=User.objects.get(id=case.reported_by.id)
        description = request.POST.get("description")
        evidence_file = request.FILES.get("evidence_file")
        feedback = Feedback.objects.create(
            case=case,
            feedback_message=description,
            provided_by=user,
            reported_by=user_reported_by,
            reported_role=role
        )

        if evidence_file:
            fs = FileSystemStorage(location=settings.MEDIA_ROOT)
            filename = fs.save(evidence_file.name, evidence_file)
            feedback.feedback_file = filename

        case.status = 'under_investigation'
        case.save()
        user.is_active = True
        user.save()

        feedback.save()
        messages.success(request, "Feedback sent successfully!")
        return redirect("Internal_Investigator_Case")  

    return redirect("Internal_Investigator_Case")  


from django.core.paginator import Paginator
from datetime import datetime, timedelta
from django.shortcuts import render
from .models import Case, User  # Make sure to import your models

def Investigetor_Case_views_Solved(request):
    name = request.session["name"]
    role = request.session["user_type"]
    user = User.objects.get(id=request.session['user_id'])
    investigators = User.objects.filter(user_type='investigator', is_active=True)

    # Get the date filter parameters
    from_date = request.GET.get('from_date')
    to_date = request.GET.get('to_date')

    # Base query
    cases = Case.objects.filter(assigned_to=user, status="resolved")

    # Apply date filters if provided and valid
    if from_date and from_date != 'None':
        cases = cases.filter(created_at__gte=from_date)
    if to_date and to_date != 'None':
        # Add one day to include the end date fully
        to_date_obj = datetime.strptime(to_date, '%Y-%m-%d')
        next_day = to_date_obj + timedelta(days=1)
        cases = cases.filter(created_at__lt=next_day)

    cases_with_feedback = cases.filter(feedbacks__isnull=False)

    # Pagination
    paginator = Paginator(cases,2)  # Show 10 cases per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'name': name,
        'role': role,
        'cases_with_feedback': cases_with_feedback,
        'cases': page_obj,  # Pass the paginated cases
        'investigators': investigators,
        'from_date': from_date,
        'to_date': to_date,
    }
    return render(request, 'investigator/SolvedCase.html', context)



def admin_Case_views_Solved(request):
    name = request.session["name"]
    role = request.session["user_type"]
    
    # Default to all resolved cases
    cases = Case.objects.filter(status="resolved")
    
    # Handle date filtering
    from_date = request.GET.get('from_date')
    to_date = request.GET.get('to_date')
    
    if from_date and to_date:
        # Convert to proper date format and filter
        cases = cases.filter(
            created_at__date__gte=from_date,
            created_at__date__lte=to_date
        )
    
    context = {
        'name': name,
        'role': role,
        'cases': cases,
        'from_date': from_date,
        'to_date': to_date,
    }
    return render(request, 'admin/SolvedCase.html', context)



def case_detail_view(request, case_id):
    name = request.session["name"]
    role = request.session["user_type"]
    
    # Get the case or return 404 if not found
    case = get_object_or_404(Case, id=case_id)
    
    context = {
        'name': name,
        'role': role,
        'case': case,
    }
    return render(request, 'admin/case_detail.html', context)

def Reporter_Case_views_Solved (request):
    name = request.session["name"]
    role= request.session["user_type"]
    user = User.objects.get(id=request.session['user_id']) 
    cases = Case.objects.filter(reported_by=user, status="resolved")
    
    # Fetch cases that have at least one associated feedback
    cases_with_feedback = cases.filter(feedbacks__isnull=False)

    context = {
        'name': name,
        'role': role,
        'cases_with_feedback': cases_with_feedback,
    }
    return render(request, 'Reporter/SolvedCase.html', context)

def UpdateReporter (request):
    user = User.objects.get(id=request.session['user_id'])
    name = request.session["name"]
    role= request.session["user_type"]
    context = {
            'name': name,
            'role': role,
            'user': user,
        }

    if request.method == "POST":

        fullname = request.POST.get('fullname')
        address = request.POST.get('address')
        phone_number = request.POST.get('phone_number')
        email = request.POST.get('email')
        password = request.POST.get('password')

        user.fullname = fullname
        user.address = address
        user.phone_number = phone_number
        user.email = email
        user.password=password      


        user.save()       
        messages.success(request, "Profile updated successfully!")
       
        return render(request, 'Reporter/UpdateProfile.html',context)
    return render(request, 'Reporter/UpdateProfile.html',context)

def UpdateslegalProfile (request):
    user = User.objects.get(id=request.session['user_id'])
    name = request.session["name"]
    role= request.session["user_type"]
    context = {
            'name': name,
            'role': role,
            'user': user,
        }

    if request.method == "POST":

        fullname = request.POST.get('fullname')
        address = request.POST.get('address')
        phone_number = request.POST.get('phone_number')
        email = request.POST.get('email')
        password = request.POST.get('password')

        user.fullname = fullname
        user.address = address
        user.phone_number = phone_number
        user.email = email
        user.password=password      


        user.save()       
        messages.success(request, "Profile updated successfully!")
       
        return render(request, 'Reporter/UpdateProfile.html',context)
    return render(request, 'Reporter/UpdateProfile.html',context)


def UpdateInvestigetor (request):
    user = User.objects.get(id=request.session['user_id'])
    name = request.session["name"]
    role= request.session["user_type"]
    context = {
            'name': name,
            'role': role,
            'user': user,
        }

    if request.method == "POST":

        fullname = request.POST.get('fullname')
        address = request.POST.get('address')
        phone_number = request.POST.get('phone_number')
        email = request.POST.get('email')
        password = request.POST.get('password')

        user.fullname = fullname
        user.address = address
        user.phone_number = phone_number
        user.email = email
        user.password=password      


        user.save()       
        messages.success(request, "Profile updated successfully!")
       
        return render(request, 'investigator/UpdateProfile.html',context)
    return render(request, 'investigator/UpdateProfile.html',context)
        
    
def Updateadimn (request):
    user = User.objects.get(id=request.session['user_id'])
    name = request.session["name"]
    role= request.session["user_type"]
    context = {
            'name': name,
            'role': role,
            'user': user,
        }

    if request.method == "POST":

        fullname = request.POST.get('fullname')
        address = request.POST.get('address')
        phone_number = request.POST.get('phone_number')
        email = request.POST.get('email')
        password = request.POST.get('password')

        user.fullname = fullname
        user.address = address
        user.phone_number = phone_number
        user.email = email
        user.password=password

        user.save()       
        messages.success(request, "Profile updated successfully!")
       
        return render(request, 'admin/UpdateProfile.html',context)
    return render(request, 'admin/UpdateProfile.html',context)

def contact_view(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")
        
        ContactMessage.objects.create(name=name, email=email, message=message)
        messages.success(request, "Your message has been sent successfully!")
        return redirect("index")

    return redirect("index")

def contactus_display (request):
    name = request.session["name"]
    role= request.session["user_type"]
    contactus = ContactMessage.objects.all()
    context = {
        'name': name,
        'role': role,
        'contacts': contactus,
    }
    return render(request, 'admin/contacts.html', context)


def LegalAdvisor (request):
    name = request.session["name"]
    role= request.session["user_type"]

    if request.method == "POST":
        fullname = request.POST.get('fullname')
        address = request.POST.get('address')
        phone_number = request.POST.get('phone_number')
        email = request.POST.get('email')
        user_types=request.POST.get('role')
        password=123456789

        if User.objects.filter(email=email).exists():
            messages.error(request, "This email is already registered Try Other Email.")
            return redirect('Legal_advisor')
        try:
            EmailValidator()(email)
        except ValidationError:
            messages.error(request, "Invalid email format.")
            return redirect('Legal_advisor')
        user = User.objects.create(
            fullname=fullname,
            address=address,
            phone_number=phone_number,
            email=email,
            password=password,  
            user_type=user_types
        )
        user.save()
        messages.success(request, "Thank you for creating a Legal Advisor Account was Successful")
        return redirect('Legal_advisor_List')  

    context = {
        'name': name,
        'role': role,
    }
    return render(request, 'investigator/LegalAdvisor.html', context)

from django.db.models import Q
def LegalAdvisorList (request):
    name = request.session["name"]
    role= request.session["user_type"]   

    legal_advisors = User.objects.filter(
        Q(user_type="legalAdvisor") | Q(user_type="internal_Investigator")
    )
    context = {
        'name': name,
        'role': role,
        'legal_advisors': legal_advisors,
    }
    return render(request, 'investigator/LegalAdvisorList.html', context)


def Legal_Case_views (request):
    name = request.session["name"]
    role= request.session["user_type"]
    user = User.objects.get(id=request.session['user_id'])
    investigators = User.objects.filter(user_type='legalAdvisor',is_active=True)
    status = request.GET.get('status')  
    if status:
        cases = Case.objects.filter(Legal_assigned_to=user,status=status)
    else:
        cases = Case.objects.filter(Legal_assigned_to=user,status="under_Legal_Advisor")
    cases_with_evidence = cases.filter(evidence__isnull=False)
    cases_with_feedback = cases.filter(feedbacks__isnull=False)
      
    context = {
        'name': name,
        'role': role,
        'cases': cases,
        'investigators': investigators,
        'cases_with_evidence': cases_with_evidence,
        'cases_with_feedback': cases_with_feedback,
    }
    return render(request, 'Legal/CaseAssigned.html', context)




def Internal_Investigator_Case_views (request):
    name = request.session["name"]
    role= request.session["user_type"]
    user = User.objects.get(id=request.session['user_id'])
    investigators = User.objects.filter(user_type='internal_Investigator',is_active=True)
    status = request.GET.get('status')  
    if status:
        cases = Case.objects.filter(Legal_assigned_to=user,status=status)
    else:
        cases = Case.objects.filter(Legal_assigned_to=user,status="under_investigation")
    cases_with_evidence = cases.filter(evidence__isnull=False)
    cases_with_feedback = cases.filter(feedbacks__isnull=False)
    context = {
        'name': name,
        'role': role,
        'cases': cases,
        'investigators': investigators,
        'cases_with_feedback': cases_with_feedback,
        'cases_with_evidence': cases_with_evidence
    }
    return render(request, 'Internal/Case_Assigned.html', context)



def Legal_Case_views_Solved (request):
    name = request.session["name"]
    role= request.session["user_type"]
    user = User.objects.get(id=request.session['user_id'])
    investigators = User.objects.filter(user_type='investigator',is_active=True) 
    cases = Case.objects.filter(Legal_assigned_to=user, status="resolved")
    
    # Fetch cases that have at least one associated feedback
    cases_with_feedback = cases.filter(feedbacks__isnull=False)

    context = {
        'name': name,
        'role': role,
        'cases_with_feedback': cases_with_feedback,
        'cases': cases,
        'investigators': investigators,
    }
    return render(request, 'Legal/SolvedCase.html', context)



def Legal_Assign_edit_case(request, case_id):
    case = get_object_or_404(Case, id=case_id)
    investigators = User.objects.all()

    if request.method == 'POST':
        legal_id = request.POST.get('legal_id')
        if legal_id:
            LegalAdvisor = User.objects.get(id=legal_id)
            case.Legal_assigned_to = LegalAdvisor
            case.status="under_Legal_Advisor"
            if case.assigned_to:
                user = LegalAdvisor
                user.is_active = False
                user.save()

            case.save()
            messages.success(request, 'Legal Advisor assigned successfully .')
            return redirect('investigetor_case')
        else:
            messages.error(request, 'Please select an Legal Advisor.')

    name = request.session["name"]
    role= request.session["user_type"]
    cases = Case.objects.all()
    investigators = User.objects.filter(user_type='investigator',is_active=True)
    context = {
        'name': name,
        'role': role,
        'cases': cases,
        'investigators': investigators,
    }
    return render(request, 'investigator/CaseAssigned.html', context)

from django.utils import timezone

def internal_Investigator_Assign_edit_case(request, case_id):
    case = get_object_or_404(Case, id=case_id)
    investigators = User.objects.all()

    if request.method == 'POST':
        internal_Investigator_id = request.POST.get('internal_Investigator_id')
        if internal_Investigator_id:
            internal_Investigators = User.objects.get(id=internal_Investigator_id)

            # Get the current month and year
            now = timezone.now()
            current_month = now.month
            current_year = now.year

            # Count how many cases this Legal Advisor already has this month
            assigned_cases_count = Case.objects.filter(
                internal_Investigator=internal_Investigators,
                created_at__year=current_year,
                created_at__month=current_month
            ).count()

            if assigned_cases_count > 4:
                messages.error(request, f'{internal_Investigators.fullname} already has 4 cases assigned this month.')
                return redirect('investigetor_case')

            case.internal_Investigator = internal_Investigators
            case.status = "under_investigation"

            if case.assigned_to:
                user = internal_Investigators
                user.is_active = False
                case.Assigned_at = now 
                user.save()

            case.save()
            messages.success(request, 'Internal_Investigator assigned successfully.')
            return redirect('investigetor_case')
        else:
            messages.error(request, 'Please select a internal_Investigator.')

    name = request.session["name"]
    role = request.session["user_type"]
    cases = Case.objects.all()
    investigators = User.objects.filter(user_type='internal_Investigator', is_active=True)

    context = {
        'name': name,
        'role': role,
        'cases': cases,
        'investigators': investigators,
    }
    return render(request, 'investigator/CaseAssigned.html', context)



def Adding_Evidence_case(request, case_id):
    if request.method == "POST":
        user = User.objects.get(id=request.session['user_id'])
        case = get_object_or_404(Case, id=case_id)
        user_reported_by=User.objects.get(id=case.reported_by.id)
        evidence_file = request.FILES.get("evidence_file")
        evidence = Evidence.objects.create(
            case=case,
            provided_by=user,
            reported_by=user_reported_by
        )

        if evidence_file:
            fs = FileSystemStorage(location=settings.MEDIA_ROOT)
            filename = fs.save(evidence_file.name, evidence_file)
            evidence.feedback_file = filename

        evidence.save()
        messages.success(request, "Thank you for adding Evidence on this  Case!")
        return redirect("investigetor_case")  

    return redirect("investigetor_case")