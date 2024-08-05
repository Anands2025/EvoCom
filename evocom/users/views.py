from django.contrib.auth import authenticate, login, logout,update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.utils.crypto import get_random_string
from evocom import settings
from .models import PasswordResetToken, User, UserDetails
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .decorators import nocache
from communities.models import Community



def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about-us.html')

def contacts(request):
    return render(request, 'contact.html')

@login_required
@nocache
def admin_index(request):
    return render(request, 'user/admin_index.html')
@login_required
@nocache
def community_admin_index(request):
    return render(request, 'user/community_admin_index.html')
@login_required
@nocache
def member_index(request):
    return render(request, 'user/member_index.html')

@login_required
@nocache
def user_profile(request):
    user = request.user
    user_details = user.details
    if request.method == 'POST':
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user_details.phone_number = request.POST.get('phone_number')
        user_details.gender = request.POST.get('gender')
        user_details.place = request.POST.get('place')
        user_details.address = request.POST.get('address')
        user.save()
        user_details.save()
        messages.success(request, 'Profile updated successfully!')
        return redirect('users:user_profile')

    return render(request, 'user/profile.html', {'user': user, 'user_details': user_details})

def login_page(request):
    if request.user.is_authenticated:
        return redirect('users:member_index')
    return render(request, 'user/login.html')

def send_welcome_email(user):
    subject = 'Welcome to EvoCom'
    context = {'user': user}
    html_content = render_to_string('user/welcome_mail.html', context)
    text_content = strip_tags(html_content)
    email = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER, [user.email])
    email.attach_alternative(html_content, 'text/html')
    email.send()

def send_password_reset_email(user, token):
    reset_url = f'{settings.SITE_URL}/reset_password/{token}/'
    subject = 'Password Reset Request'
    context = {
        'user': user,
        'reset_url': reset_url,
    }
    html_content = render_to_string('user/password_reset_email.html', context)
    text_content = strip_tags(html_content)
    email = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER, [user.email])
    email.attach_alternative(html_content, 'text/html')
    email.send()

@require_POST
def register_view(request):
    username = request.POST.get('username')
    email = request.POST.get('email')
    password1 = request.POST.get('password1')
    password2 = request.POST.get('password2')

    if password1 != password2:
        return render(request, 'user/register.html', {'error': 'Passwords do not match'})

    try:
        user = User.objects.create_user(username=username, email=email, password=password1)
        UserDetails.objects.create(user=user)
        send_welcome_email(user)
        return redirect('users:login')

    except Exception as e:
        return render(request, 'user/register.html', {'error': str(e)})

def login_view(request):
    if request.user.is_authenticated:
        user_details, created = UserDetails.objects.get_or_create(user=request.user)
        if user_details.role == "admin":
            return redirect('users:admin_index')
        profile_complete = user_details.role and user_details.phone_number and user_details.place
        if profile_complete:
            if user_details.role == "member":
                return redirect('users:member_index')
            if user_details.role == "community_admin":
                try:
                    community = Community.objects.get(admin=request.user)
                    has_community = community.name and community.description
                    if has_community:
                        return redirect('users:community_admin_index')
                    else:
                        return redirect('communities:create_community')
                except Community.DoesNotExist:
                    return redirect('communities:create_community')
        else:
            return redirect('users:select_user_type')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            user_details, created = UserDetails.objects.get_or_create(user=user)
            if user_details.role == "admin":
                return redirect('users:admin_index')
            profile_complete = user_details.role and user_details.phone_number and user_details.place
            if profile_complete:
                if user_details.role == "member":
                    return redirect('users:member_index')
                if user_details.role == "community_admin":
                    try:
                        community = Community.objects.get(admin=user)
                        has_community = community.name and community.description
                        if has_community:
                            return redirect('users:community_admin_index')
                        else:
                            return redirect('communities:create_community')
                    except Community.DoesNotExist:
                        return redirect('communities:create_community')
            else:
                return redirect('users:select_user_type')
        else:
            return render(request, 'user/login.html', {'error': 'Invalid username or password.'})

    return render(request, 'user/login.html')

def user_logout(request):
    logout(request)
    return redirect('users:index')

@login_required
def select_user_type(request):
    if request.method == 'POST':
        user_details = request.user.details
        role = request.POST.get('role')
        user_details.role = role
        user_details.save()
        return redirect('users:complete_profile')

    roles = UserDetails.ROLE_CHOICES
    context = {
        'roles': roles
    }
    return render(request, 'user/select_user_type.html', context)

@login_required
def complete_profile(request):
    user = request.user
    user_details = user.details
    if request.method == 'POST':
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user_details.phone_number = request.POST.get('phone_number')
        user_details.gender = request.POST.get('gender')
        user_details.place = request.POST.get('place')
        user_details.address = request.POST.get('address')
        user.save()
        user_details.save()
        messages.success(request, 'Profile updated successfully!')
        if user_details.role == "member":
            return redirect('users:member_index')
        if user_details.role == "community_admin":
            return redirect('communities:create_community')
        if user_details.role == "admin":
            return redirect('users:admin_index')

    return render(request, 'user/profile_completion.html')

def password_reset_request(request):
    if request.method == "POST":
        email = request.POST.get('email')
        associated_users = User.objects.filter(email=email)
        if associated_users.exists():
            for user in associated_users:
                token = PasswordResetToken.objects.create(user=user)
                send_password_reset_email(user, token.token)
            return HttpResponse('A password reset link has been sent to your email.')
        else:
            return HttpResponse('No user is associated with this email address.')
    return render(request, 'user/forgot_password.html')

def reset_password(request, token):
    reset_token = PasswordResetToken.objects.filter(token=token, expiry__gt=timezone.now()).first()
    if not reset_token:
        return HttpResponse("Invalid or expired token.")
    
    if request.method == "POST":
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if password1 == password2:
            reset_token.user.set_password(password1)
            reset_token.user.save()
            reset_token.delete()
            return HttpResponse("Your password has been reset successfully.")
        else:
            return HttpResponse("Passwords do not match.")
    
    return render(request, 'user/reset_password.html', {'token': token})

@login_required
def update_profile(request):
    user = request.user
    user_details = user.details
    if request.method == 'POST':
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user_details.phone_number = request.POST.get('phone_number')
        user_details.place = request.POST.get('place')
        user_details.address = request.POST.get('address')
        user.save()
        user_details.save()
        messages.success(request, 'Profile updated successfully!')
        return redirect('users:user_profile')
    return render(request, 'user/profile.html', {'user': user, 'user_details': user_details})
@login_required
def password_change(request):
    if request.method == 'POST':
        user = request.user
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if not user.check_password(current_password):
            return JsonResponse({'error': 'Current password is incorrect'}, status=400)
        
        if new_password != confirm_password:
            return JsonResponse({'error': 'New passwords do not match'}, status=400)
        
        if len(new_password) < 8:
            return JsonResponse({'error': 'Password must be at least 8 characters long'}, status=400)
        
        user.set_password(new_password)
        user.save()
        update_session_auth_hash(request, user)  # Important for keeping the user logged in
        return JsonResponse({'success': 'Password has been changed successfully'})
    return render(request, 'user/password_change.html')
def check_unique(request):
    username = request.POST.get('username')
    email = request.POST.get('email')

    data = {
        'username_exists': User.objects.filter(username=username).exists(),
        'email_exists': User.objects.filter(email=email).exists(),
    }
    return JsonResponse(data)