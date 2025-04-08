from django.shortcuts import render,redirect
from .models import Moodboard, Category, Review, Purchase, Message, User, Payment, ContactMessage
from django.contrib.auth import login, authenticate, logout
from .forms import RegisterForm, MoodboardForm, ContactForm
from django.contrib.auth.decorators import login_required
from .decorators import creator_required
from django.contrib.auth.views import PasswordResetView
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Avg
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils.timezone import now
import os
from django.conf import settings
from django.http import Http404
from django.contrib import messages
from .tasks import send_welcome_email

'''class CustomPasswordResetView(PasswordResetView):
    def form_valid(self, form):
        email = form.cleaned_data.get('email')
        send_mail(
            'Password Reset Request',
            f'Click the link to reset your password.:{reset_link}',
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False  # Change to True for production
        )
        return super().form_valid(form)'''
        
        
import logging
logger = logging.getLogger(__name__)

#Password Reset View---------------------------
class CustomPasswordResetView(PasswordResetView):
    def form_valid(self, form):
        email = form.cleaned_data.get('email')
        User = get_user_model()
        
        try:
            user = User.objects.get(email=email)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            reset_link = self.request.build_absolute_uri(
                reverse('password_reset_confirm', kwargs={'uidb64': uid, 'token': token})
            )

            logger.debug(f"Sending email to {email} with reset link: {reset_link}")

            send_mail(
                'Password Reset Request',
                f'Click the link to reset your password: {reset_link}',
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False
            )

            logger.debug(f"Email sent successfully to {email}")

        except User.DoesNotExist:
            logger.error(f"User with email {email} not found")

        return super().form_valid(form)

#Home Page View---------------------------      
def home(request):
    moodboards = Moodboard.objects.all().order_by('-created_at')[:5] 
    creators = User.objects.filter(role='creator')[:4]  # Limit to 4
    categories = Category.objects.all()[:4]  # Limit to 4
    return render(request, 'moodboards/home.html', {"moodboards": moodboards,'creators': creators, 'categories': categories})
    

#Page not found view---------------------------
def custom_404(request, exception):
    return render(request, 'moodboards/404.html', status=404)

#Moodboard list view---------------------------
def moodboard_list(request, category_id):
    categories = Category.objects.all()
    moodboards = Moodboard.objects.filter(category_id=category_id).annotate(avg_rating=Avg('review__rating')).order_by('-avg_rating')
    return render(request, 'moodboards/moodboard_list.html', {'categories': categories, 'moodboards': moodboards, 'category_id': category_id})

#Create Moodboard View---------------------------
@login_required
@creator_required
def create_moodboard(request):
	if request.method=="POST":
		form = MoodboardForm(request.POST, request.FILES)
		if form.is_valid():
			moodboard = form.save(commit=False)
			moodboard.creator = request.user
			moodboard.save() 
			return redirect('creator_dashboard')
	else:
		form = MoodboardForm()
	return render(request,'moodboards/create_moodboard.html',{"form":form})
	
#Update Moodboard View---------------------------


'''def update_moodboard(request, id):
    moodboard = Moodboard.objects.get(id=id)

    if request.method == "POST":  # <-- Ensure this is indented properly
        form = MoodboardForm(request.POST, request.FILES, instance=moodboard)
        if form.is_valid():
            # Your logic here
            moodboard.save()
        	return redirect('creator_dashboard')

    else:
        form = MoodboardForm(instance=moodboard)

    return render(request, 'moodboards/update_moodboard.html', {'form': form, 'moodboard': moodboard})
'''
def update_moodboard(request,id):
	moodboard=Moodboard.objects.get(id=id)
	if request.method=="POST":
		moodboard.title=request.POST.get('title')
		moodboard.description=request.POST.get('description')
		new_image = request.FILES.get('image') 
		if new_image:
			if moodboard.image:
				old_image_path = os.path.join(settings.MEDIA_ROOT, str(moodboard.image))
				if os.path.exists(old_image_path):
					os.remove(old_image_path)

			moodboard.image = new_image  # Update the image field

		moodboard.updated_at = now()  # Update timestamp
		moodboard.save()
		return redirect('creator_dashboard')
	return render(request,'moodboards/update_moodboard.html',{'moodboard':moodboard})




#Delete moodboard view---------------------------	
@login_required
@creator_required
def delete_moodboard(request, id):
    moodboard = Moodboard.objects.get(id=id, creator=request.user)
    moodboard.delete()
    return redirect('moodboard_list')

#Creators list view---------------------------	
def creators_list(request):
	designers = User.objects.filter(role='creator')
	return render(request,'moodboards/creators_list.html', {'designers': designers})
	
#Categories list view---------------------------
def categories_list(request):
    categories = Category.objects.all()
    return render(request,'moodboards/categories_list.html',{'categories':categories})

#About view---------------------------	
def about(request):
	return render(request,'moodboards/about.html')
	
#Contact view---------------------------	
def contact(request):
	return render(request,'moodboards/contact.html')
	
# Signup View----------------------------------------------------
def register_user(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) # Auto-login after registration
            send_welcome_email.delay(user.email, user.username)  
            return redirect('dashboard')  # Redirect to dashboard based on role
    else:
        form = RegisterForm()
    return render(request, "moodboards/register.html", {"form": form})


def login_user(request):
    next_url = request.GET.get('next', 'dashboard')  # Get 'next' parameter or default to 'dashboard'
    
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect(next_url)  # Redirect to previous page or default page
        else:
            return render(request, "moodboards/login.html", {"error": "Invalid credentials"})
    
    return render(request, "moodboards/login.html")


# Logout View-----------------------------------------
@login_required
def logout_user(request):
    logout(request)
    return redirect("login")

#Profile view--------------------------------------
@login_required
def profile(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=request.user)

    return render(request, 'profile.html', {'form': form})


#Creator Profile------------------------------------
def creator_profile(request, creator_id):
	buyer = request.user if request.user.is_authenticated else None
	creator = User.objects.get(id=creator_id, role='creator')
	moodboards = Moodboard.objects.filter(creator=creator).annotate(avg_rating=Avg('review__rating')).order_by('-avg_rating')
	is_logged_in = request.user.is_authenticated
    
	return render(request, 'moodboards/creator_profile.html', {'creator': creator, 'moodboards': moodboards,'is_logged_in': is_logged_in,'buyer':buyer})

#Buyer Dashboard------------------------------------
@login_required
def buyer_dashboard(request):
    sent_hire_requests = Message.objects.filter(sender=request.user)

    # Fetch purchases related to the logged-in user
    purchases = Purchase.objects.filter(buyer=request.user).select_related('moodboard')

    return render(request, 'moodboards/buyer_dashboard.html', {
        'sent_hire_requests': sent_hire_requests,
        'purchases': purchases  # Add purchases to context
    })


#Creator Dashboard----------------------------
@login_required
def creator_dashboard(request):
	designer = User.objects.get(id=request.user.id,role='creator')
	moodboards = Moodboard.objects.filter(creator=designer)
	hire_requests = Message.objects.filter(recipient=designer).select_related('sender') 
	return render(request,'moodboards/creator_dashboard.html',{'moodboards':moodboards,'hire_requests':hire_requests})

#Dashboard view--------------------------------
@login_required
def dashboard(request):
    if request.user.role=='creator':
        return redirect('creator_dashboard')  # Redirect to creator's dashboard
    elif request.user.role=='buyer':
        return redirect('buyer_dashboard')  # Redirect to buyer's dashboard
    elif request.user.role=='admin':
        return redirect('/admin/')  # Redirect admin users to Django Admin
    return redirect('home')  # Default fallback

#Hire designer view-------------------------------
@login_required
def hire_designer(request, designer_id):
    designer = User.objects.get( id=designer_id, role='creator')

    if request.method == "POST":
        message_text = request.POST.get('message')
        Message.objects.create(sender=request.user, recipient=designer, message=message_text)

        messages.success(request, f"Hire request sent to {designer.username}!")
        return redirect('creators')  # Redirect to creators list after sending request

    return render(request, 'moodboards/hire_form.html', {'designer': designer})
 
@login_required(login_url='login') 
def buy_moodboard(request, moodboard_id):
    moodboard = Moodboard.objects.get(id=moodboard_id)
    buyer = request.user  # Fetch the logged-in user
	
    # Ensure only buyers can purchase
    if buyer.role != 'buyer':
        messages.error(request, "Only buyers can purchase moodboards.")
        return redirect('moodboard_list', category_id=moodboard.category.id)

    # Check if purchase already exists, else create one
    purchase, created = Purchase.objects.get_or_create(
        buyer=buyer,
        moodboard=moodboard,
        defaults={'price': moodboard.price}
    )

    # Check if payment already exists
    payment, _ = Payment.objects.get_or_create(
        purchase=purchase,
        defaults={'buyer': buyer, 'moodboard': moodboard, 'payment_status': 'Pending'}
    )

    if request.method == 'POST':
        payment.payment_status = 'Paid'  # Mark as paid
        payment.save()
        messages.success(request, "Payment successful! You can now view your moodboard.")
        return redirect('download_moodboard', moodboard_id=moodboard.id)

    return render(request, 'payments/payment.html', {"moodboard": moodboard, "payment": payment})


	
#Download Moodboard view-----------------------
@login_required
def download_moodboard(request, moodboard_id):
    moodboard = Moodboard.objects.get(id=moodboard_id)
    payment = Payment.objects.filter(buyer=request.user, moodboard=moodboard, payment_status='Paid').first()	

    if payment:
        return render(request, 'payments/download.html', {'moodboard': moodboard})
    
    messages.error(request, "You need to complete the payment before accessing this moodboard.")
    return redirect('buy_moodboard', moodboard_id=moodboard.id)



#Moodboard details--------------------------------------
def moodboard_details(request, category_id, moodboard_id):
    category = Category.objects.get(id=category_id)
    moodboard = Moodboard.objects.get(id=moodboard_id, category=category) 
    
    return render(request, 'moodboards/moodboard_details.html', {'category': category, 'moodboard': moodboard})
    
    
#Submit review-----------------------------------
def submit_review(request, moodboard_id):
    if not request.user.is_authenticated:
        messages.error(request, "You must be logged in to leave a review.")
        return redirect('login')  # Redirect to login if the user is not logged in

    try:
        moodboard = Moodboard.objects.get(id=moodboard_id)
    except Moodboard.DoesNotExist:
        raise Http404("Moodboard not found")

    if request.method == 'POST':
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')

        # Check if user already submitted a review for this moodboard
        existing_review = Review.objects.filter(buyer=request.user, moodboard=moodboard).first()

        if existing_review:
            messages.error(request, "You have already reviewed this moodboard.")
            return redirect('moodboard_list', category_id=moodboard.category.id)

        # Create a new review
        review = Review.objects.create(
            buyer=request.user,
            moodboard=moodboard,
            rating=rating,
            comment=comment
        )

        messages.success(request, "Your review has been submitted successfully!")
        return redirect('moodboard_list', category_id=moodboard.category.id)  # Redirect back to the moodboard list

    return redirect('moodboard_list', category_id=moodboard.category.id)
    
#Contact view------------------------------
def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your message has been sent successfully!")
            return redirect('contact')
    else:
        form = ContactForm()

    return render(request, "moodboards/contact.html", {"form": form})
    
#Respond to request
@login_required
def respond_to_hire_request(request, request_id, action):
    hire_request = Message.objects.get(id=request_id, recipient=request.user)

    if action == "accept":
        hire_request.status = "accepted"
        messages.success(request, f"You accepted {hire_request.sender.username}'s request!")
    elif action == "reject":
        hire_request.status = "rejected"
        messages.warning(request, f"You rejected {hire_request.sender.username}'s request!")

    hire_request.save()

    # Send Notification to the Sender
    if not hire_request.notification_sent:
        notification_message = f"Hello {hire_request.sender.username},\n\nYour hire request to {hire_request.recipient.username} has been {hire_request.status}."
        
        # Send email notification (optional)
        send_mail(
            subject="Hire Request Update",
            message=notification_message,
            from_email="admin@moodboard.com",  # Replace with your email
            recipient_list=[hire_request.sender.email],
            fail_silently=True,
        )

        # Mark notification as sent
        hire_request.notification_sent = True
        hire_request.save()

    return redirect('creator_dashboard')  # Redirect back to update UI


# After user signs up
def signup_view(request):
    if request.method == 'POST':
        # Assuming you've already created the user
        user = User.objects.create_user(...)
        send_welcome_email.delay(user.email, user.username)


