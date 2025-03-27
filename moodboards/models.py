from django.db import models
from django.contrib.auth.models import AbstractUser

#Category Model-----------------------------
class Category(models.Model):
	name = models.CharField(max_length=100,unique=True)
	image = models.ImageField(upload_to='category_images/', blank=True, null=True)
	description = models.TextField()
	def __str__(self):
		return self.name
		
# Custom User Model-----------------------------
class User(AbstractUser):
    ROLE_CHOICES = [
        ('creator', 'Creator/Designer'),
        ('buyer', 'Buyer'),
    ]
   
    Categories = [
    		('All','All'),
		('Seasonal Theme','Seasonal Theme'),
		('Digital Design','Digital Design'),
		('Photography','Photography'),
		('Art & Illustration','Art & Illustration'),
		('Branding & Marketing','Branding & Marketing'),
		('Event Planning','Event Planning'),
		('Fashion','Fashion'),
		('Interior Design','Interior Design'),
	]
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='buyer')
    profile_image = models.ImageField(upload_to='profile_images/', default='/media/profile_images/default.jpeg', blank=True)
    speciality = models.CharField(max_length=30, choices=Categories, default='All')
    def __str__(self):
    	return f"{self.username} is the {self.role}"
    

#MoodBoard Model-----------------------------
class Moodboard(models.Model):
	creator = models.CharField(max_length=100)
	title = models.CharField(max_length=100)
	description = models.TextField()
	image = models.ImageField(upload_to='moodboards/',null=True,blank=True)
	category = models.ForeignKey(Category, on_delete=models.CASCADE)
	creator = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role':'creator'}) 
	price = models.DecimalField(max_digits=10,decimal_places=2)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	def __str__(self):
		 return f"{self.title} by {self.creator}"

# Purchase Model-----------------------------
class Purchase(models.Model):
	buyer = models.ForeignKey(User, on_delete=models.CASCADE)
	moodboard = models.ForeignKey(Moodboard, on_delete=models.CASCADE,)
	price = models.DecimalField(max_digits=10, decimal_places=2)
	purchase_date = models.DateTimeField(auto_now_add=True)
	
	def __str__(self):
		return f'{self.buyer.username} bought {self.moodboard.title}'
		
#Review Model-----------------------------
class Review(models.Model):
	buyer = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role':'buyer'})
	moodboard = models.ForeignKey(Moodboard, on_delete=models.CASCADE)
	rating = models.IntegerField(choices=[(i,str(i)) for i in range(1,6)])
	comment = models.TextField()
	created_at = models.DateTimeField(auto_now_add=True)
	
	def __str__(self):
	 return f'Review by {self.buyer.username} - {self.rating}'
	 
#Message Model--------------------------------
class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_messages")
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_messages")
    message = models.TextField()
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("accepted", "Accepted"),
        ("rejected", "Rejected"),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="pending")
    notification_sent = models.BooleanField(default=False)  # New field

    def __str__(self):
        return f"{self.sender.username} -> {self.recipient.username}: {self.status}"



# Payment Model-----------------------------
class Payment(models.Model):
	buyer = models.ForeignKey(User, on_delete=models.CASCADE)
	moodboard = models.ForeignKey(Moodboard, on_delete=models.CASCADE)
	purchase = models.OneToOneField(Purchase, on_delete=models.CASCADE)
	payment_status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Paid', 'Paid')], default='Pending')
	timestamp = models.DateTimeField(auto_now_add=True)
	
	def __str__(self):
		return f'Payment for {self.purchase.moodboard.title} - {self.payment_status} by {self.buyer}'

#Contact model---------------------------------------------
class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.subject}"

#Notification Model----------------------------------------
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user.username}"

	
