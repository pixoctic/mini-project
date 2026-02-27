from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import ServiceRequest

def home(request):
    return render(request, 'core/home.html')

# ==========================================
#         AUTHENTICATION VIEWS
# ==========================================

def register_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) # Automatically log the user in after signup
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'core/signup.html', {'form': form})

def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                # If the user is an admin/staff, route them directly to the Jazzmin dashboard
                if user.is_staff:
                    return redirect('/admin')
                # Otherwise, route normal customers to the homepage
                return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'core/login.html', {'form': form})

def logout_user(request):
    logout(request)
    return redirect('home')


# ==========================================
#         CORE SERVICE VIEWS
# ==========================================

@login_required(login_url='login')
def submit_request(request):
    if request.method == 'POST':
        brand = request.POST.get('brand')
        model = request.POST.get('model')
        imei = request.POST.get('imei')
        issue = request.POST.get('issue')
        
        # Save the new repair request to the database and link it to the logged-in user
        new_request = ServiceRequest.objects.create(
            customer=request.user,
            device_brand=brand,
            device_model=model,
            imei_number=imei,
            issue_description=issue
        )
        # Send them to the success page to see their new Tracking ID
        return render(request, 'core/success.html', {'tracking_id': new_request.tracking_id})
        
    return render(request, 'core/submit.html')

@login_required(login_url='login')
def track_repair(request):
    query = request.GET.get('q')
    context = {}
    
    if query:
        # SECURITY SECITON: 'customer=request.user' ensures a user can only pull up 
        # a repair ticket if they are the one who originally created it.
        repair = ServiceRequest.objects.filter(tracking_id=query, customer=request.user).first() or \
                 ServiceRequest.objects.filter(imei_number=query, customer=request.user).first()
                 
        context['repair'] = repair
        context['searched'] = True
        
    return render(request, 'core/track.html', context)
