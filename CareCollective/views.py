from django.shortcuts import render,redirect,get_object_or_404
import folium
import pytz
from django.http import HttpResponse,HttpResponseForbidden
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import datetime
from django.contrib.auth.models import User
from django.contrib.auth import logout
from datetime import timedelta,date
from django.utils.timezone import now
from CareCollective.models import Users_Model,Login_Model,State_Model,Donor_Model,Admin_Model,Category_Model,Item_Model,Request_Model,Maps_Model,Chat_Model,Comments_Model
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.contrib.auth.hashers import check_password
from django.urls import reverse
from django.core.paginator import Paginator
from django.contrib import messages
from django.db.models import Count,Max,Q
from django.db.models.functions import TruncMonth
from django.contrib.auth.hashers import check_password, make_password
# Create your views here.


def index(request):
    # Count total users excluding admins and donors
    total_users = Users_Model.objects.filter(Admin_Flag="False").exclude(
        UID__in=Donor_Model.objects.values_list('UID', flat=True)
    ).count()
    
    # Count total donors
    total_donors = Donor_Model.objects.count()
    
    # Count total approved donations
    total_donations = Request_Model.objects.filter(Status="Approved").count()
    
    # Pass the counts to the template
    context = {
        'total_users': total_users,
        'total_donors': total_donors,
        'total_donations': total_donations,
    }
    return render(request, 'index.html', context)

def login(request):
    return render(request,'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')
#------------------------------REGISTER-----------------------------------

def user_register(request):
    # Fetch all states to populate the dropdown
    states = State_Model.objects.all()

    if request.method == "POST":
        print("Form submitted")
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        email = request.POST.get("email")
        state_id = request.POST.get("State")  # Get the selected state ID
        username = request.POST.get("username")
        password = request.POST.get("password")
        confirm = request.POST.get("confirm")
        date_of_join = date.today()
        admin_flag = "False"
        status = "Active"

        # Validate that all fields are filled
        if not all([name, phone, email, username, password, confirm, state_id]):
            print("Validation failed: All fields must be filled.")
            return render(request, 'user_register.html', {
                "error": "All fields must be filled.",
                "name": name, "phone": phone, "email": email, "username": username,
                "states": states  # Pass states back to the template
            })

          # Validate email
        try:
            validate_email(email)
        except ValidationError:
            print("Validation failed: Invalid email address.")
            return render(request, 'user_register.html', {
                "error": "Invalid email address.",
                "name": name, "phone": phone, "username": username
            })

        # Validate username uniqueness
        if Login_Model.objects.filter(Username=username).exists():
            print("Validation failed: Username already exists.")
            return render(request, 'user_register.html', {
                "error": "Username already exists. Please choose a different one.",
                "name": name, "phone": phone, "email": email
            })

        # Validate phone number (10 digits and starts with a valid digit)
        if len(phone) != 10 or not phone.isdigit() or not phone.startswith(('6', '7', '8', '9')):
            print("Validation failed: Invalid phone number.")
            return render(request, 'user_register.html', {
                "error": "Invalid phone number. It must be 10 digits and start with 6, 7, 8, or 9.",
                "name": name, "email": email, "username": username
            })

        # Validate password match
        if password != confirm:
            print("Validation failed: Passwords do not match.")
            return render(request, 'user_register.html', {
                "error": "Passwords do not match.",
                "name": name, "phone": phone, "email": email, "username": username
            })

        # Save user data with the selected state
        try:
            state = State_Model.objects.get(State_Id=state_id)  # Get state object by ID
            data = Users_Model(Name=name, Mobile_Number=phone, Email_Id=email, Date_Of_Join=date_of_join, Admin_Flag=admin_flag, Status=status, State_Id=state)
            data.save()
            print(f"User saved with UID: {data.UID}")

            # Save login data
            login_data = Login_Model(UID=data, Username=username, Password=password)
            login_data.save()
            print("Login data saved")

            return render(request, 'user_register.html', {"success": "Registration successful!", "states": states})
        except Exception as e:
            print(f"Error saving data: {e}")
            return render(request, 'user_register.html', {
                "error": "There was an error processing your request.",
                "name": name, "phone": phone, "email": email, "username": username,
                "states": states  # Pass states back to the template
            })

    # GET request: just render the form with the list of states
    return render(request, 'user_register.html', {"states": states})


def donor_register(request):
    states = State_Model.objects.all()
    if request.method == "POST":
        print("Form submitted")

        name = request.POST.get("name")
        phone = request.POST.get("phone")
        email = request.POST.get("email")
        state_id = request.POST.get("State")
        username = request.POST.get("username")
        password = request.POST.get("password")
        confirm = request.POST.get("confirm")
        date_of_join = date.today()
        admin_flag = "False"
        status = "Active"

        print(f"Received data: Name={name}, Phone={phone}, Email={email}, Username={username}")

        # Validate that all fields are filled
        if not all([name, phone, email, username, password, confirm,state_id]):
            print("Validation failed: All fields must be filled.")
            return render(request, 'donor_register.html', {
                "error": "All fields must be filled.",
                "name": name, "phone": phone, "email": email, "username": username, "states": states
            })

        # Validate email
        try:
            validate_email(email)
        except ValidationError:
            print("Validation failed: Invalid email address.")
            return render(request, 'donor_register.html', {
                "error": "Invalid email address.",
                "name": name, "phone": phone, "username": username,"states": states
            })

        # Validate username uniqueness
        if Login_Model.objects.filter(Username=username).exists():
            print("Validation failed: Username already exists.")
            return render(request, 'donor_register.html', {
                "error": "Username already exists. Please choose a different one.",
                "name": name, "phone": phone, "email": email,"states": states
            })

        # Validate phone number (10 digits and starts with a valid digit)
        if len(phone) != 10 or not phone.isdigit() or not phone.startswith(('6', '7', '8', '9')):
            print("Validation failed: Invalid phone number.")
            return render(request, 'donor_register.html', {
                "error": "Invalid phone number. It must be 10 digits and start with 6, 7, 8, or 9.",
                "name": name, "email": email, "username": username,"states": states
            })

        # Validate password match
        if password != confirm:
            print("Validation failed: Passwords do not match.")
            return render(request, 'donor_register.html', {
                "error": "Passwords do not match.",
                "name": name, "phone": phone, "email": email, "username": username,"states": states
            })

        try:
            # If all validations pass, save user data
            state = State_Model.objects.get(State_Id=state_id)
            data = Users_Model(Name=name, Mobile_Number=phone, Email_Id=email, Date_Of_Join=date_of_join, Admin_Flag=admin_flag, Status=status,State_Id=state)
            data.save()
            print(f"User saved with UID: {data.UID}")

            # Save login data
            login_data = Login_Model(UID=data, Username=username, Password=password)
            login_data.save()
            print("Login data saved")
            
            # Save DONOR data
            donor_data = Donor_Model(UID=data, Donation_History_Count=0, Verified_Date=date_of_join)
            donor_data.save()
            print("donor data saved")

            return render(request, 'donor_register.html', {"success": "Registration successful!","states": states})
        except Exception as e:
            print(f"Error saving data: {e}")
            return render(request, 'donor_register.html', {
                "error": "There was an error processing your request.",
                "name": name, "phone": phone, "email": email, "username": username,"states": states
            })

    return render(request, 'donor_register.html',{"states": states})

#--------------------------------------LOGIN-----------------------------------------
def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        
        try:
            # Check if username and password match in Login_Model
            user_login = Login_Model.objects.get(Username=username, Password=password)
            user = user_login.UID  # Get the corresponding user from Users_Model
            
            # Check if the user is active
            if user.Status == "Active":
                # Store UID in session
                request.session['user_id'] = user.UID
                request.session['last_login'] = str(timezone.now())  # Store last login time
                request.session.set_expiry(3600)  # Set session expiry to 1 hour

                # Check if the user is an admin
                if user.Admin_Flag == "True":
                    admin = Admin_Model.objects.get(UID=user.UID)
                    request.session['admin_id'] = admin.Admin_Id
                    return redirect(reverse('admin_dashboard')) 

                # Check if the user is a donor
                elif Donor_Model.objects.filter(UID=user).exists():
                    return redirect(reverse('donor_dashboard'))

                # Otherwise, redirect to the user dashboard
                else:
                    return redirect(reverse('user_dashboard'))
            
            # If the user is blocked, show a message
            elif user.Status == "Blocked":
                return render(request, 'login.html', {"error": "Sorry, you are blocked by the admin."})

        except Login_Model.DoesNotExist:
            return render(request, 'login.html', {"error": "Invalid username or password."})

    return render(request, 'login.html')

#-----------------------------------------------#USER#--------------------------------
def user_dashboard(request):
    # Check if the user is still logged in
    if 'user_id' in request.session:
        # Get the last activity time and calculate the inactivity duration
        last_login = request.session.get('last_login')
        last_login_time = timezone.datetime.fromisoformat(last_login) if last_login else None
        if last_login_time and timezone.now() - last_login_time > timedelta(hours=1):
            # If user was inactive for more than an hour, log them out
            logout(request)
            return redirect(reverse('login'))  # Redirect to login if session expired

        # Fetch categories and donors in alphabetical order
        user_id = request.session['user_id']
        user = Users_Model.objects.get(pk=user_id)
        donor=Donor_Model.objects.filter(UID=user_id)
        categories=Category_Model.objects.filter(Status='Active').order_by('Category_Name')
        donors = Donor_Model.objects.filter(UID__Status='Active')
        username = Login_Model.objects.get(UID=user_id).Username
        
        # Get total requests and approved requests
        total_requests = Request_Model.objects.filter(UID=user_id).count()
        total_approved_requests = Request_Model.objects.filter(UID=user_id, Status="Approved").count()

        # Pass categories and donors to the template
        return render(request, 'user_dashboard.html', 
                      {'categories': categories,
                       'donors': donors,
                       'user': user,
                       'donor':donor,
                       'total_requests': total_requests,
                       'total_approved_requests': total_approved_requests
                       })

    return redirect(reverse('login'))

def donor_details_page(request, donor_id):
    if 'user_id' in request.session:
        last_login = request.session.get('last_login')
        last_login_time = timezone.datetime.fromisoformat(last_login) if last_login else None
        
        if last_login_time and timezone.now() - last_login_time > timedelta(hours=1):
            # If user was inactive for more than an hour, log them out
            logout(request)
            return redirect(reverse('login'))
        
        # Get the selected donor by their donor_id
        donor = get_object_or_404(Donor_Model, Donor_Id=donor_id)
        
        # Get all items that this donor has donated and are not expired
        items = Item_Model.objects.filter(Donor_Id=donor, Expiry_Date__isnull=True, Quantity__gt=0) | Item_Model.objects.filter(Donor_Id=donor, Expiry_Date__gt=timezone.now(), Quantity__gt=0)
        
        # Check if the logged-in user is an admin
        is_admin = Admin_Model.objects.filter(UID=request.session['user_id']).exists()
        
        categories = Category_Model.objects.filter(Status='Active').order_by('Category_Name')
        donors = Donor_Model.objects.filter(UID__Status='Active')

        # Pass the donor details, items, and the admin status to the template
        return render(request, 'donor_details_page.html', {'categories': categories, 'donors': donors, 'donor': donor, 'items': items, 'is_admin': is_admin})
    
    return redirect(reverse('login'))



def user_items_based_category(request, category_id):
    if 'user_id' in request.session:
        last_login = request.session.get('last_login')
        last_login_time = timezone.datetime.fromisoformat(last_login) if last_login else None
        
        if last_login_time and timezone.now() - last_login_time > timedelta(hours=1):
            # If user was inactive for more than an hour, log them out
            logout(request)
            return redirect(reverse('login'))
        
    category = Category_Model.objects.get(pk=category_id)
    donors = Donor_Model.objects.filter(UID__Status='Active')
    states = State_Model.objects.all()
    categories = Category_Model.objects.filter(Status='Active').order_by('Category_Name')
    is_admin = Admin_Model.objects.filter(UID=request.session['user_id']).exists()
    
    items = Item_Model.objects.filter(
    Category_Id=category,
    Expiry_Date__gt=now(),
    Quantity__gt=0)
    items = items | Item_Model.objects.filter(Category_Id=category, Expiry_Date__isnull=True,Quantity__gt=0)
        
    selected_donor = request.GET.get('donor')
    selected_state = request.GET.get('state')
    selected_quantity = request.GET.get('quantity')

    if selected_donor:
        items = items.filter(Donor_Id=selected_donor)

    if selected_state:
        donors_in_state = Donor_Model.objects.filter(UID__State_Id=selected_state)
        items = items.filter(Donor_Id__in=donors_in_state)

    if selected_quantity:
        items = items.filter(Quantity__gte=selected_quantity)
        
    

    context = {
        'category': category,
        'categories': categories,  
        'donors': donors,
        'states': states,
        'items': items,
        'is_admin': is_admin
    }
    return render(request, 'user_items_based_category.html', context)

def user_items_search(request, item_id): 
    item = Category_Model.objects.get(pk=item_id)
    donors = Donor_Model.objects.filter(UID__Status='Active')
    states = State_Model.objects.all()
    categories = Category_Model.objects.filter(Status='Active').order_by('Category_Name')

    search_term = request.POST.get('searched', '').strip()

    items = Item_Model.objects.filter(
        Expiry_Date__gt=now(),
        Quantity__gt=0
    )
    
    items = items | Item_Model.objects.filter(Category_Id=item, Expiry_Date__isnull=True, Quantity__gt=0)

    if search_term:
        items = items.filter(Item_Name__icontains=search_term)

    selected_donor = request.GET.get('donor')
    selected_state = request.GET.get('state')
    selected_quantity = request.GET.get('quantity')

    if selected_donor:
        items = items.filter(Donor_Id=selected_donor)

    if selected_state:
        donors_in_state = Donor_Model.objects.filter(UID__State_Id=selected_state)
        items = items.filter(Donor_Id__in=donors_in_state)

    if selected_quantity:
        items = items.filter(Quantity__gte=selected_quantity)

    context = {
        'category': item,
        'categories': categories,  
        'donors': donors,
        'states': states,
        'items': items,
    }

    return render(request, 'user_items_search.html', context)


def add_request(request, item_id):
    donors = Donor_Model.objects.all()
    categories = Category_Model.objects.filter(Status='Active').order_by('Category_Name')
    item = get_object_or_404(Item_Model, Item_Id=item_id)
    donor = item.Donor_Id  # Get the donor from the item

    if 'user_id' in request.session:
        user_id = request.session['user_id']
        # Get the Users_Model instance for the logged-in user
        user = get_object_or_404(Users_Model, UID=user_id)

    if request.method == 'POST':
        quantity = request.POST['quantity']
        urgency = request.POST['urgency']
        reason = request.POST['reason']
        request_date = now().date()  
        
        if not all([quantity, urgency, reason]):
            print("Validation failed: All fields must be filled.")
            return render(request, 'user_request.html', {
                "error": "All fields must be filled.",
                "quantity": quantity, "urgency": urgency, "reason": reason
            })

        # Create a new request
        new_request = Request_Model.objects.create(
            UID=user,  
            Donor_Id=donor,
            Item_Id=item,
            Quantity=quantity,
            Request_Date=request_date,
            Urgency=urgency,
            Reason=reason,
            Status='Pending'
        )

        new_request.save()
        messages.success(request, 'Request sent successfully.')
        return redirect('user_view_status')
 
     

    # For GET request, render the form
    return render(request, 'user_request.html', {"donors": donors,"categories": categories,'item': item, 'request_date': now().date()})

def user_request_view(request):
    donors = Donor_Model.objects.all()
    categories=Category_Model.objects.filter(Status='Active')
    if 'user_id' in request.session:
        user_id = request.session['user_id']
        user = get_object_or_404(Users_Model, UID=user_id)
    user_requests = Request_Model.objects.filter(UID=user)

    # Pagination: Show 5 requests per page
    paginator = Paginator(user_requests, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    for req in page_obj:
        # Ensure both are date objects before comparing
        req.within_20_days = (timezone.now().date() - req.Request_Date) <= timedelta(days=20)

    return render(request, 'user_request_view.html', {'page_obj': page_obj,"donors": donors,"categories": categories})

def user_request_update(request, request_id):
    request_obj = get_object_or_404(Request_Model, Request_Id=request_id)

    if request.method == 'POST':
        request_obj.Quantity = request.POST.get('quantity')
        request_obj.Urgency = request.POST.get('urgency')
        request_obj.Reason = request.POST.get('reason')
        request_obj.save()  

        # Add a success message
        messages.success(request, "Request updated successfully!")
        
        # Redirect to 'user_request_view'
        return redirect('user_request_view')

    return render(request, 'user_request_update.html', {
        'request_obj': request_obj,
        'item': request_obj.Item_Id,  
    })
    
def delete_request(request, request_id):
    if 'user_id' in request.session:
        user_id = request.session['user_id']
        user = get_object_or_404(Users_Model, UID=user_id)
        
        # Get the specific request and delete it
        request_to_delete = get_object_or_404(Request_Model, Request_Id=request_id, UID=user)
        request_to_delete.delete()
        
        # Add a success message
        messages.success(request, "Request deleted successfully.")
    
    # Redirect to the user's request list
    return redirect('user_request_view')


def user_view_status(request):
    if 'user_id' in request.session:
        user_id = request.session['user_id']
        
        # Fetch all requests for this donor
        requests = Request_Model.objects.filter(UID=user_id)
        categories = Category_Model.objects.filter(Status='Active')
        donors = Donor_Model.objects.all()

        return render(request, 'user_view_status.html', {
            'categories': categories,
            'donors':donors,
            'requests': requests
        })
    return redirect('login')

def delete_order_request(request, request_id):
    request_obj = get_object_or_404(Request_Model, Request_Id=request_id)

    if request_obj.Status == 'Pending':
        request_obj.delete()

    return redirect('user_view_status')

def user_map_view(request):
    # Fetch all states to allow user to select the state
    states = State_Model.objects.all()

    # Initialize the map centered at a default location
    map_center_lat = 20.5937  # Default latitude for India
    map_center_long = 78.9629  # Default longitude for India

    # Get map info from Maps_Model if the user selects a location
    selected_map = None
    if request.method == 'POST':
        selected_state = request.POST.get('state')
        selected_city = request.POST.get('city')

        # Find the location in the database based on the state and city
        selected_map = Maps_Model.objects.filter(State_Id=selected_state, City=selected_city).first()

        if selected_map:
            map_center_lat = selected_map.Latitude
            map_center_long = selected_map.Longitude

    # Generate Folium map
    m = folium.Map(location=[map_center_lat, map_center_long], zoom_start=6)

    # Add marker if a location was selected
    if selected_map:
        folium.Marker([selected_map.Latitude, selected_map.Longitude], 
                      popup=f"{selected_map.City}, {selected_map.State_Id.State_Name}").add_to(m)

    # Save the map to an HTML file
    m = m._repr_html_()  # Render map as HTML

    # Pass the map and state data to the template
    context = {
        'map': m,
        'states': states,
    }

    return render(request, 'user_map_view.html', context)

'''def item_complete_details(request, item_id):
    item = get_object_or_404(Item_Model, pk=item_id)
    categories = Category_Model.objects.filter(Status='Active').order_by('Category_Name')
    donors = Donor_Model.objects.filter(UID__Status='Active')
    state = item.Donor_Id.UID.State_Id
    return render(request, 'user_item_complete_details.html', {'categories': categories,
            'donors':donors,'item': item,'state': state})'''

def item_complete_details(request, item_id):
    item = get_object_or_404(Item_Model, pk=item_id)
    categories = Category_Model.objects.filter(Status='Active').order_by('Category_Name')
    donors = Donor_Model.objects.filter(UID__Status='Active')
    state = item.Donor_Id.UID.State_Id

    # Fetch approved requests and associated comments for the item
    approved_requests = Request_Model.objects.filter(Item_Id=item, Status="Approved")
    comments = Comments_Model.objects.filter(Donor_Id=item.Donor_Id, Status="Active").order_by('-Comment_Date')

    return render(request, 'user_item_complete_details.html', {
        'categories': categories,
        'donors': donors,
        'item': item,
        'state': state,
        'approved_requests': approved_requests,
        'comments': comments
    })

    

def user_chat_list(request):
    if 'user_id' in request.session:
        user_id = request.session['user_id']
    categories=Category_Model.objects.filter(Status='Active').order_by('Category_Name')
    donors = Donor_Model.objects.filter(UID__Status='Active')
    approved_requests = Request_Model.objects.filter(UID=user_id, Status="Approved") \
                                             .select_related('Donor_Id', 'Item_Id')
    
    return render(request, 'user_chat_list.html', {'approved_requests': approved_requests,
                                                   'categories':categories,
                                                   'donors':donors
                                                   })



def user_donor_chat(request, donor_id):
    if 'user_id' in request.session:
        user_id = request.session['user_id']
        user = Users_Model.objects.get(UID=user_id)
        donor = Donor_Model.objects.get(Donor_Id=donor_id)
        donors = Donor_Model.objects.filter(UID__Status='Active')
        categories = Category_Model.objects.filter(Status='Active')

        chat_messages = Chat_Model.objects.filter(UID=user, Donor_Id=donor).order_by('Message_Date')
        if request.method == "POST":
            message_content = request.POST.get('message_content')
            if message_content:
                # Create a new message
                new_message = Chat_Model(
                    UID=user,
                    Donor_Id=donor,
                    Content=message_content,
                    Message_Date=datetime.now(),
                    Sent_By=user_id
                )
                new_message.save()

                return redirect('user_donor_chat', donor_id=donor_id)

        return render(request, 'user_donor_chat.html', {
            'chat_messages': chat_messages,
            'donor': donor,
            'user': user,
            'donors': donors,
            'categories': categories,
        })
    else:
        return redirect('login')

def user_leave_comment(request):
    if 'user_id' in request.session:
        user_id = request.session['user_id']
    approved_requests = Request_Model.objects.filter(UID=user_id, Status="Approved") \
                                             .select_related('Donor_Id', 'Item_Id')
    donors = Donor_Model.objects.filter(UID__Status='Active')
    categories = Category_Model.objects.filter(Status='Active')
    
    return render(request, 'user_leave_comment.html', {'approved_requests': approved_requests,
                                                       'donors':donors,
                                                       'categories':categories
                                                       })

def leave_comment(request, donor_id):
    if 'user_id' in request.session:
        user_id = request.session['user_id']
        user = Users_Model.objects.get(UID=user_id)
        donor = Donor_Model.objects.get(Donor_Id=donor_id)
        is_admin = Admin_Model.objects.filter(UID=request.session['user_id']).exists()
        donors = Donor_Model.objects.filter(UID__Status='Active')
        categories = Category_Model.objects.filter(Status='Active')

        if request.method == 'POST' and not is_admin:
            comment_content = request.POST['comment']
            # Create a new comment
            comment = Comments_Model(
                UID=user,
                Donor_Id=donor,
                Comment=comment_content,
                Comment_Date=datetime.now(),
                Status='Active'
            )
            comment.save()
            return redirect('leave_comment', donor_id=donor_id)

        # Fetch all comments for the donor
        comments = Comments_Model.objects.filter(Donor_Id=donor,Status='Active').order_by('-Comment_Date')
        admin_comments = Comments_Model.objects.filter(Donor_Id=donor).order_by('-Comment_Date')


        return render(request, 'user_comments.html', {
            'donor': donor,
            'comments': comments,
            'is_admin': is_admin,
            'donors':donors,
            'categories':categories,
            'admin_comments':admin_comments
        })
    else:
        return redirect('login')





#-----------------------------------------------#DONOR--------------------------------
def donor_dashboard(request):
    # Check if user is logged in and is a donor
    if 'user_id' in request.session:
        user_id = request.session['user_id']
        try:
            donor = Donor_Model.objects.get(UID=user_id)
        except Donor_Model.DoesNotExist:
            return redirect(reverse('login'))  # Not a donor, redirect to login

        # Inactivity check (1 hour)
        last_login = request.session.get('last_login')
        last_login_time = timezone.datetime.fromisoformat(last_login) if last_login else None
        if last_login_time and timezone.now() - last_login_time > timedelta(hours=1):
            logout(request)
            return redirect(reverse('login'))

        # Fetch categories
        categories = Category_Model.objects.filter(Status='Active').order_by('Category_Name')
        username = Login_Model.objects.get(UID=user_id).Username

        # Chart data: count of approved requests by user
        approved_requests = (
        Request_Model.objects
        .filter(Donor_Id=donor.Donor_Id, Status="Approved")
        .values('UID__Name')
        .annotate(total=Count('Request_Id'))
        if donor else []
        )
        chart_labels = [req['UID__Name'] for req in approved_requests]
        chart_data = [req['total'] for req in approved_requests]

        return render(request, 'donor_dashboard.html', {
            'categories': categories,
            'donor': donor,
            'chart_labels': chart_labels,
            'chart_data': chart_data,
            'username':username
        })

    return redirect(reverse('login'))



def add_item(request):
    if 'user_id' in request.session:
        user_id = request.session['user_id']
        try:
            donor = Donor_Model.objects.get(UID=user_id)
        except Donor_Model.DoesNotExist:
            return redirect(reverse('login'))  # Redirect to login if donor not found
    categories = Category_Model.objects.filter(Status='Active')

    if request.method == 'POST':
        # Get form data
        item_name = request.POST['item_name']
        description = request.POST['description']
        quantity = int(request.POST['quantity'])
        expiry_date = request.POST.get('expiry_date', None)
        category_id = request.POST['category']  # Get the selected category from the form
        status = 'Active'

        # Handle images
        image1 = request.FILES['image1']  # Image1 is mandatory
        image2 = request.FILES.get('image2', None)  # Optional Image2
        image3 = request.FILES.get('image3', None)  # Optional Image3

        # Fetch the donor and category
        try:
            category = Category_Model.objects.get(Category_Id=category_id, Status="Active")
        except Category_Model.DoesNotExist:
            return render(request, 'add_items.html', {"error": "Invalid category selected.",'categories': categories})

        # Check if the selected category is food and validate expiry date
        if category.Category_Name.lower() == 'food' and not expiry_date:
            # Pass form data back to template in case of error
            return render(request, 'add_items.html', {
                "error": "Expiry date is required for food items.",
                "name": item_name, "description": description, 
                "quantity": quantity, "category_id": category_id,
                "image1": image1, "image2": image2, "image3": image3,'categories': categories
            })
            
        if category.Category_Name.lower() == 'food' :
            today = datetime.now()
            expected_expiry_date = today + timedelta(days=30)

            # Convert to string for comparison
            expected_date_str = expected_expiry_date.strftime('%Y-%m-%d')
            
            if expiry_date < expected_date_str :
                return render(request, 'add_items.html', {
                "error": "Expiry date should be more than a month.",
                "name": item_name, "description": description, 
                "quantity": quantity, "category_id": category_id,
                "image1": image1, "image2": image2, "image3": image3,'categories': categories
            })

        # Validate mandatory fields
        if not all([item_name, description, quantity, image1]):
            return render(request, 'add_items.html', 
                {
                "error": "All fields must be filled.",
                "name": item_name, "description": description, 
                "quantity": quantity, "category_id": category_id,
                "image1": image1, "image2": image2, "image3": image3,'categories': categories
                })

        # Save the item to the database
        new_item = Item_Model(
            Item_Name=item_name,
            Item_Description=description,
            Quantity=quantity,
            Expiry_Date=expiry_date if expiry_date else None,
            Image1=image1,
            Image2=image2 if image2 else None,  
            Image3=image3 if image3 else None,  
            Donor_Id=donor,
            Category_Id=category,
            Status=status
        )
        new_item.save()

        return render(request, 'add_items.html', {"success": "Item added successfully!",'categories': categories})

    # Fetch active categories to show in the dropdown
    categories = Category_Model.objects.filter(Status='Active')
    return render(request, 'add_items.html', {'categories': categories})


def donor_items_based_category(request, category_id):
    category = Category_Model.objects.get(pk=category_id)
    donors = Donor_Model.objects.all()
    states = State_Model.objects.all()
    categories = Category_Model.objects.filter(Status='Active')
    items = Item_Model.objects.filter(Category_Id=category, Expiry_Date__isnull=True) | Item_Model.objects.filter(Category_Id=category, Expiry_Date__gt=now())
    
    selected_donor = request.GET.get('donor')
    selected_state = request.GET.get('state')
    selected_quantity = request.GET.get('quantity')

    if selected_donor:
        items = items.filter(Donor_Id=selected_donor)

    if selected_state:
        donors_in_state = Donor_Model.objects.filter(UID__State_Id=selected_state)
        items = items.filter(Donor_Id__in=donors_in_state)

    if selected_quantity:
        items = items.filter(Quantity__gte=selected_quantity)

    context = {
        'category': category,
        'categories': categories,
        'donors': donors,
        'states': states,
        'items': items,
    }
    return render(request, 'donor_items_based_category.html', context)

def list_donated_items(request):
    if 'user_id' in request.session:
        user_id = request.session['user_id']
        try:
            donor = Donor_Model.objects.get(UID=user_id)
        except Donor_Model.DoesNotExist:
            return redirect(reverse('login')) 
    
    donor = Donor_Model.objects.get(UID=user_id)
    categories_list = Category_Model.objects.all()
    
    # Get all items donated by this donor
    donated_items = Item_Model.objects.filter(Donor_Id=donor).select_related('Category_Id')

    # Group items by category
    categories = Category_Model.objects.filter(item_model__Donor_Id=donor).distinct()

    # Pass the current date to the template
    context = {
        'donated_items': donated_items,
        'categories': categories,
        'categories_list': categories_list,
        'today': now().date(),  # Current date
    }
    
    return render(request, 'list_donated_items.html', context)

def delete_item(request, item_id):
    item = get_object_or_404(Item_Model, Item_Id=item_id)
    Request_Model.objects.filter(Item_Id=item).delete()
    item.delete()
    messages.success(request, 'Item and associated requests deleted successfully.')

    return redirect('list_donated_items') 

def donor_items_update(request, item_id):
    # Fetch the item by its ID
    item = get_object_or_404(Item_Model, Item_Id=item_id)
    categories = Category_Model.objects.filter(Status='Active')
    
    if request.method == 'POST':
        # Process form data
        item.Item_Name = request.POST['item_name']
        item.Category_Id = get_object_or_404(Category_Model, Category_Id=request.POST['category'])
        item.Item_Description = request.POST['description']
        item.Quantity = request.POST['quantity']
        expiry_date = request.POST.get('expiry_date', None)
        
        if expiry_date:
            item.Expiry_Date = expiry_date
        
        # Handle image uploads
        if 'image1' in request.FILES:
            item.Image1 = request.FILES['image1']
        if 'image2' in request.FILES:
            item.Image2 = request.FILES['image2']
        if 'image3' in request.FILES:
            item.Image3 = request.FILES['image3']

        # Save updated item details
        item.save()
        
        messages.success(request, 'Item updated successfully.')
        return redirect('list_donated_items')  # Redirect back to the item list after update
    
    # Pre-fill form with item details
    return render(request, 'donor_items_update.html', {
        'item': item,
        'categories': categories,
    })

def add_category(request):
    if 'user_id' in request.session:
        user_id = request.session['user_id']
        try:
            donor = Donor_Model.objects.get(UID=user_id)
        except Donor_Model.DoesNotExist:
            return redirect(reverse('login')) 

        if request.method == 'POST':
            category_name = request.POST['category_name']
            category_description = request.POST['description']
            
            # Filter Admin_Model for "Super Admin" or "Category Admin" roles
            try:
                admin = Admin_Model.objects.get(Role__in=["Category Admin"])
            except Admin_Model.DoesNotExist:
                return render(request, 'add_category.html', {"error": "Admin not found or unauthorized."})

            # Create and save the new category
            new_category = Category_Model(
                Admin_Id=admin,
                Donor_Id=donor,
                Category_Name=category_name,
                Category_Description=category_description,
                Date_Created=now(),
                Status='Pending' 
            )
            new_category.save()

            return render(request, 'add_category.html', {"success": "Category added successfully! Awaiting admin approval."})
        return render(request, 'add_category.html')

    else:
        return redirect('login')


def donor_manage_requests(request):
    if 'user_id' in request.session:
        user_id = request.session['user_id']
        donor = get_object_or_404(Donor_Model, UID=user_id)
        
        # Fetch all requests for this donor
        requests = Request_Model.objects.filter(Donor_Id=donor)
        categories=Category_Model.objects.filter(Status='Active')
        
        for request_obj in requests:
            print(f"Item: {request_obj.Item_Id.Item_Name}, Quantity: {request_obj.Item_Id.Quantity}")

        return render(request, 'donor_manage_request.html', {
            'categories': categories,
            'requests': requests
            
        })
    return redirect('login')


def approve_request(request, request_id):
    request_obj = get_object_or_404(Request_Model, Request_Id=request_id)

    #if request_obj.Status == 'Pending' or:
    request_obj.Status = 'Approved'
    request_obj.save()

        # Reduce the quantity of the item
    item = request_obj.Item_Id
    item.Quantity -= request_obj.Quantity
    item.save()

        # Update donor information
    donor = request_obj.Donor_Id
    donor.Donation_History_Count += 1
    donor.Last_Donation_Date = date.today()

        # Update Preferred Donation Categories
    donor.Preferred_Donation_Categories = item.Category_Id.Category_Name
    '''category_name = item.Category_Id.Category_Name
    if donor.Preferred_Donation_Categories:
            categories = donor.Preferred_Donation_Categories.split(", ")
            if category_name not in categories:
                categories.append(category_name)
                donor.Preferred_Donation_Categories = ", ".join(categories)
    else:
            donor.Preferred_Donation_Categories = category_name'''

    donor.save()

    return redirect('donor_manage_requests')


def reject_request(request, request_id):
    request_obj = get_object_or_404(Request_Model, Request_Id=request_id)

    if request_obj.Status == 'Pending':
        # Update request status to rejected
        request_obj.Status = 'Rejected'
        request_obj.save()

    return redirect('donor_manage_requests')


def donor_view_category_request(request):
    if 'user_id' in request.session:
        user_id = request.session['user_id']
        
        try:
            donor = Donor_Model.objects.get(UID=user_id)  # Fetch the donor from the UID
        except Donor_Model.DoesNotExist:
            return redirect(reverse('login'))  # Redirect if the donor doesn't exist

        category = Category_Model.objects.filter(Donor_Id=donor)  
        
        categories = Category_Model.objects.filter(Status='Active')

        return render(request, 'donor_view_category_request.html', {
            'categories': categories,
            'category': category,  
        })
    
    return redirect('login')

def delete_category_request(request, category_id):
    request_obj = get_object_or_404(Category_Model, Category_Id=category_id)

    if request_obj.Status == 'Pending':
        request_obj.delete()

    return redirect('donor_view_category_request')

def donor_chat_list(request):
    if 'user_id' in request.session:
        user_id = request.session['user_id']
        
        try:
            donor = Donor_Model.objects.get(UID=user_id)  # Fetch the donor from the UID
        except Donor_Model.DoesNotExist:
            return redirect(reverse('login')) 
        
        approved_requests = Request_Model.objects.filter(Donor_Id=donor, Status="Approved") \
                                                 .select_related('UID', 'Item_Id')
                                                 
        categories = Category_Model.objects.filter(Status='Active')
        
        #three_months_ago = now() - timedelta(days=90)
        #Chat_Model.objects.filter(Donor_Id=donor_id, Message_Date__lt=three_months_ago).delete()
    
        return render(request, 'donors_chat_list.html', {'approved_requests': approved_requests,
                                                        'categories':categories})
    return redirect('login')


def donor_user_chat(request, user_id):
    if 'user_id' in request.session:
        logged_in_user_id = request.session['user_id']
        user = Users_Model.objects.get(UID=user_id)  
        donor = Donor_Model.objects.get(UID=logged_in_user_id)  

        chat_messages = Chat_Model.objects.filter(UID=user, Donor_Id=donor).order_by('Message_Date')
        if request.method == "POST":
            message_content = request.POST.get('message_content')
            if message_content:

                new_message = Chat_Model(
                    UID=user,
                    Donor_Id=donor,
                    Content=message_content,
                    Message_Date=datetime.now(),
                    Sent_By=donor.Donor_Id 
                )
                new_message.save()

                return redirect('donor_user_chat', user_id=user_id)

        return render(request, 'donor_user_chat.html', {
            'chat_messages': chat_messages,
            'donor': donor,
            'user': user,
        })
    else:
        return redirect('login')

def donor_comments_view(request):
    if 'user_id' in request.session:
        user_id = request.session['user_id']
        try:
            donor = Donor_Model.objects.get(UID=user_id)  
        except Donor_Model.DoesNotExist:
            return redirect(reverse('login')) 
        comments = Comments_Model.objects.filter(Donor_Id=donor).order_by('-Comment_Date')
        context = {
        'donor': donor,
        'comments': comments,
        }
        return render(request, 'donor_comments_view.html', context)
    return redirect('login')



#-----------------------------------------------#ADMIN--------------------------------
def admin_dashboard(request):
    if 'user_id' in request.session:
        user_id = request.session['user_id']
        try:
            admin = Admin_Model.objects.get(UID=user_id)
        except Admin_Model.DoesNotExist:
            return redirect(reverse('login'))  
        

        last_login = request.session.get('last_login')
        last_login_time = timezone.datetime.fromisoformat(last_login) if last_login else None
        if last_login_time and timezone.now() - last_login_time > timedelta(hours=1):
            logout(request)
            return redirect(reverse('login'))
        
        categories = Category_Model.objects.filter(Status='Active').order_by('Category_Name')
        donors = Donor_Model.objects.all().order_by('UID__Name')
        registered_users = Users_Model.objects.filter(Admin_Flag='False').exclude(
            UID__in=Donor_Model.objects.values_list('UID', flat=True)
        ).count()

        # Registered donors
        registered_donors = Donor_Model.objects.count()

        # Total number of donations
        total_donations = Request_Model.objects.filter(Status='Approved').count()

        # Donors with the most donated items
        donors_donation_count = Donor_Model.objects.annotate(
            donation_count=Count('item_model__request_model', filter=Q(item_model__request_model__Status='Approved'))
            ).filter(donation_count__gt=0  # Only donors with at least 1 approved donation
                ).order_by('-donation_count')[:10]

        # Data for pie chart: Donations per category per month
        category_donations = Request_Model.objects.filter(Status='Approved').values('Item_Id__Category_Id__Category_Name') \
            .annotate(donation_count=Count('Request_Id')).order_by('-donation_count')

        # Data for bar graph: Total donations made each month by each donor
        #monthly_donations = Request_Model.objects.filter(Status='Approved').annotate(month=TruncMonth('Request_Date')) \
           # .values('Donor_Id__UID__Name', 'month') \
            #.annotate(donation_count=Count('Request_Id')) \
           # .order_by('month')
        
        monthly_donations = Request_Model.objects.filter(Status='Approved').annotate(
            month=TruncMonth('Request_Date')).values('month').annotate(
                donation_count=Count('Item_Id'))
        

        return render(request, 'admin_dashboard.html', {
            'registered_users': registered_users,
            'registered_donors': registered_donors,
            'total_donations': total_donations,
            'donors_donation_count': donors_donation_count,
            'category_donations': category_donations,
            'monthly_donations': monthly_donations,
            'categories': categories,
            'donors':donors
        })
    return redirect('login')



def manage_category_requests(request):
    if 'user_id' in request.session:
        user_id = request.session['user_id']
        try:
            # Fetch the admin details from the Admin_Model using the UID from session
            admin = Admin_Model.objects.get(UID=user_id)
        except Admin_Model.DoesNotExist:
            return redirect('login')  # Redirect to login if admin not found

        # Fetch all category requests
        categoriess = Category_Model.objects.filter(Status='Active').order_by('Category_Name')
        donors = Donor_Model.objects.all().order_by('UID__Name')
        categories = Category_Model.objects.all()

        # Pass categories and admin info to the template
        return render(request, 'admin_manage_category.html', {
            'categories': categories,
            'categoriess':categoriess,
            'admin': admin,
            'donors':donors
        })

    return redirect('login')

# Approve category request
def approve_category(request, category_id):
    if 'user_id' in request.session:
        user_id = request.session['user_id']
        admin = Admin_Model.objects.get(UID=user_id)  # Get the admin ID
        category = get_object_or_404(Category_Model, Category_Id=category_id)
        
        category.Status = 'Active'
        category.Admin_Id = admin  # Assign the admin who approved the category
        category.save()
        
        return redirect('manage_category_requests')

# Reject category request
def reject_category(request, category_id):
    if 'user_id' in request.session:
        user_id = request.session['user_id']
        admin = Admin_Model.objects.get(UID=user_id)  # Get the admin ID
        category = get_object_or_404(Category_Model, Category_Id=category_id)
        
        category.Status = 'Rejected'
        category.Admin_Id = admin  # Assign the admin who rejected the category
        category.save()
        
        return redirect('manage_category_requests')

# Delete category request (only for Super Admin)
def delete_category(request, category_id):
    if 'user_id' in request.session:
        user_id = request.session['user_id']
        admin = Admin_Model.objects.get(UID=user_id)
        

        if admin.Role == "Super Admin":  # Only Super Admin can delete
            category = get_object_or_404(Category_Model, Category_Id=category_id)
            category.delete()
            return redirect('manage_category_requests')

    return redirect('login')


def admin_manage_users(request):
    if 'user_id' in request.session:
        user_id = request.session['user_id']
        admin = Admin_Model.objects.get(UID=user_id)
        users = Users_Model.objects.exclude(
            UID__in=Donor_Model.objects.values_list('UID', flat=True)).exclude(
            UID__in=Admin_Model.objects.values_list('UID', flat=True))
        categories = Category_Model.objects.filter(Status='Active').order_by('Category_Name')
        donors = Donor_Model.objects.all().order_by('UID__Name')

        return render(request, 'admin_manage_user.html', 
                      {'users': users, 
                       'admin': admin,
                       'categories': categories,
                       'donors':donors
                       })
    return redirect('login')

def block_user(request, user_id):
    if 'admin_id' in request.session:
        admin_id = request.session['admin_id']
        try:
            # Retrieve the actual Admin_Model object using the admin_id
            admin = Admin_Model.objects.get(Admin_Id=admin_id)
            
            # Check if the admin's role is "Super Admin"
            if admin.Role == "Super Admin":
                user = get_object_or_404(Users_Model, UID=user_id)
                user.Status = 'Blocked'  # Change the user's status to "Blocked"
                user.save()
        except Admin_Model.DoesNotExist:
            return redirect('login')  # Redirect if the admin object is not found
    return redirect('admin_manage_users')


def unblock_user(request, user_id):
    if 'admin_id' in request.session:
        admin_id = request.session['admin_id']
        try:
            # Retrieve the Admin_Model object
            admin = Admin_Model.objects.get(Admin_Id=admin_id)
            
            # Check if the admin's role is "Super Admin"
            if admin.Role == 'Super Admin':
                user = get_object_or_404(Users_Model, UID=user_id)
                user.Status = 'Active'  # Change the user's status to "Active"
                user.save()
        except Admin_Model.DoesNotExist:
            return redirect('login')
    return redirect('admin_manage_users')


def admin_manage_donors(request):
    if 'user_id' in request.session:
        user_id = request.session['user_id']
        admin = Admin_Model.objects.get(UID=user_id)
        
        # Get all donors
        donors = Donor_Model.objects.select_related('UID').all()  # Fetch related user info
        
        return render(request, 'admin_manage_donors.html', {'donors': donors, 'admin': admin})
    
    return redirect('login')

def block_donor(request, user_id):
    if 'user_id' in request.session:
        user = get_object_or_404(Users_Model, UID=user_id)
        if user.Status != 'Blocked':
            user.Status = 'Blocked'
            user.save()
    return redirect('admin_manage_donors')

def unblock_donor(request, user_id):
    if 'user_id' in request.session:
        user = get_object_or_404(Users_Model, UID=user_id)
        if user.Status == 'Blocked':
            user.Status = 'Active'
            user.save()
    return redirect('admin_manage_donors')

def admin_manage_items(request):
    if 'user_id' in request.session:
        user_id = request.session['user_id']
        admin = Admin_Model.objects.get(UID=user_id)
        items_list = Item_Model.objects.all()  # Fetch all items
        paginator = Paginator(items_list, 10)  # Show 10 items per page
        page = request.GET.get('page')
        items = paginator.get_page(page)
        categories = Category_Model.objects.filter(Status='Active').order_by('Category_Name')
        donors = Donor_Model.objects.all().order_by('UID__Name')
        return render(request, 'admin_manage_items.html', 
                      {'items': items,
                       'categories':categories,
                       'donors':donors
                       })
    return redirect('login')
    

def block_item(request, item_id):
    item = get_object_or_404(Item_Model, pk=item_id)
    item.Status = 'Blocked'
    item.save()
    return redirect('admin_manage_items')

def unblock_item(request, item_id):
    item = get_object_or_404(Item_Model, pk=item_id)
    item.Status = 'Active'
    item.save()
    return redirect('admin_manage_items')

def admin_order_status_view(request):
    if 'user_id' in request.session:
        user_id = request.session['user_id']
        admin = Admin_Model.objects.get(UID=user_id)
        donors = Donor_Model.objects.all().order_by('UID__Name')
        categories = Category_Model.objects.filter(Status='Active').order_by('Category_Name')
        requests = Request_Model.objects.select_related('Item_Id', 'UID', 'Donor_Id').all()
        context = {
        'requests': requests,
        'donors':donors,
        'categories':categories
        }
        return render(request, 'admin_order_status_view.html', context)
    return redirect('login')

def admin_comment_list(request):
    if 'user_id' in request.session:
        user_id = request.session['user_id']
        admin = Admin_Model.objects.get(UID=user_id)
        approved_requests = Request_Model.objects.filter(Status="Approved") \
                                         .select_related('Donor_Id__UID') \
                                         .values('Donor_Id', 'Donor_Id__UID__Name', 'Donor_Id__Preferred_Donation_Categories') \
                                         .distinct() \
                                         .annotate(total_donations=Count('Donor_Id'))
        
        
        return render(request, 'admin_comment_list.html', {'approved_requests': approved_requests})
    return redirect('login')

def block_comment(request, comment_id,donor_id):
    if 'admin_id' in request.session:
        admin_id = request.session['admin_id']
        try:
            admin = Admin_Model.objects.get(Admin_Id=admin_id)
            comment = get_object_or_404(Comments_Model, Comment_Id=comment_id)
            comment.Status = 'Blocked' 
            comment.save()
        except Admin_Model.DoesNotExist:
            return redirect('login')  
    return redirect('leave_comment', donor_id=donor_id)


def unblock_comment(request, comment_id,donor_id):
    if 'admin_id' in request.session:
        admin_id = request.session['admin_id']
        try:
            admin = Admin_Model.objects.get(Admin_Id=admin_id)
            comment = get_object_or_404(Comments_Model, Comment_Id=comment_id)
            comment.Status = 'Active' 
            comment.save()
        except Admin_Model.DoesNotExist:
            return redirect('login')
    return redirect('leave_comment', donor_id=donor_id)

#--------------------------------------#PROFILE EDITS FOR AL USERS---------------
                                    
def change_password(request):
    if 'user_id' in request.session:
        last_login = request.session.get('last_login')
        last_login_time = timezone.datetime.fromisoformat(last_login) if last_login else None

        if last_login_time and timezone.now() - last_login_time > timedelta(hours=1):
            # Log out after 1 hour of inactivity
            logout(request)
            return redirect('login')

        is_admin = Admin_Model.objects.filter(UID=request.session['user_id']).exists()
        is_donor = Donor_Model.objects.filter(UID=request.session['user_id']).exists()

        categories = Category_Model.objects.filter(Status='Active').order_by('Category_Name')
        donors = Donor_Model.objects.all().order_by('UID__Name')

        if request.method == 'POST':
            old_password = request.POST.get('old_password')
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')

            # Fetch the Login_Model instance associated with the current user
            login_user = Login_Model.objects.get(UID=request.session['user_id'])

            # Validate the old password (direct comparison for plaintext)
            if old_password != login_user.Password:
                return render(request, 'change_password.html', {
                    'error': 'Old password is incorrect',
                    'is_admin': is_admin,
                    'is_donor': is_donor,
                    'categories': categories,
                    'donors': donors
                })

            # Ensure new passwords match
            if new_password != confirm_password:
                return render(request, 'change_password.html', {
                    'error': 'Passwords do not match',
                    'is_admin': is_admin,
                    'is_donor': is_donor,
                    'categories': categories,
                    'donors': donors
                })

            # Hash and save the new password
            hashed_password = make_password(new_password)
            login_user.Password = new_password
            login_user.save()

            return render(request, 'change_password.html', {
                'success': 'Password changed successfully',
                'is_admin': is_admin,
                'is_donor': is_donor,
                'categories': categories,
                'donors': donors
            })

        return render(request, 'change_password.html', {
            'is_admin': is_admin,
            'is_donor': is_donor,
            'categories': categories,
            'donors': donors
        })
    else:
        return redirect('login')
    
    
    
def search(request):
    categories = Category_Model.objects.filter(Status='Active').order_by('Category_Name')
    donors = Donor_Model.objects.filter(UID__Status='Active')

    if request.method == 'POST':
        searched = request.POST['searched']
        
        # Search categories
        category_search = Category_Model.objects.filter(Category_Name__icontains=searched, Status='Active').first()
        donor_search = Donor_Model.objects.filter(UID__Name__icontains=searched, UID__Status='Active').first()

        if donor_search:
            return redirect('donor_details_page', donor_id=donor_search.Donor_Id)
        
        elif category_search:
            return redirect('user_items_based_category', category_id=category_search.Category_Id)

        # Search for items that contain the search term in their name
        item_search = Item_Model.objects.filter(Item_Name__icontains=searched, Status='Active')

        if item_search.exists():
            # If items are found, render the results
            return render(request, 'user_items_Search.html', {'items': item_search, 'searched': searched, 'categories': categories, 'donors': donors})
        
        # If no results found for any category, donor, or item
        context = {
            'categories': categories,
            'donors': donors,
            'error': 'No results found for your search. Try something different.'
        }
        return render(request, 'user_dashboard.html', context)

    return redirect('login')

def notifications(request):
    if 'user_id' in request.session:
        user_id = request.session['user_id']
        
    is_donor = Donor_Model.objects.filter(UID=user_id).exists()
    notifications = []
    three_days_ago = now() - timedelta(days=3)
    sentby=Chat_Model.objects.filter(UID=user_id)

    if is_donor:
        # Fetch messages received by the donor in the last 3 days
        notifications = Chat_Model.objects.filter(
            Donor_Id__UID=user_id,
            Message_Date__gte=three_days_ago,
            Sent_By=1
        ).select_related('UID', 'Donor_Id').prefetch_related('UID__request_model_set')
    else:
        # Fetch messages received by the user in the last 3 days
        notifications = Chat_Model.objects.filter(
            UID=user_id,
            Message_Date__gte=three_days_ago,
            Sent_By=0
        ).select_related('UID', 'Donor_Id').prefetch_related('UID__request_model_set')

    return render(request, 'notifications.html', {
        'notifications': notifications,
        'is_donor': is_donor,
    })

#------------------------------------end-------------------------------------




