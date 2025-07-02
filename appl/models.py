from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from django.db.models.signals import post_save
#cloudinary_model_settings
from cloudinary.models import CloudinaryField
#from cloudinary_storage.storage import VideoMediaCloudinaryStorage
#from cloudinary_storage.validators import validate_video
#from cloudinary_storage.storage import RawMediaCloudinaryStorage

#-------------------------------------------------------------------------
#---------------------code by Dr.James Atwiine----------------------------
#-------------------------------------------------------------------------

#--------------------POST--------------------------
class Post(models.Model):
    content = models.TextField()
    #image = models.ImageField(upload_to = 'img/posts/', blank=True, null=True ) 
    image = CloudinaryField('img/posts/', blank=True, null=True )
    #video = models.FileField(upload_to='videos/posts/', blank=True, null=True)
    video = CloudinaryField('videos/posts/', resource_type='video', blank=True, null=True)
    author = models.ForeignKey(User, on_delete = models.CASCADE, related_name='posts')
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)
    profile_pic = models.ImageField(upload_to = 'img/profile/', blank=True, null=True )
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Post by {self.author.username} on {self.created_at}"

    def number_of_likes(self):
            return self.likes.count()
#-------------------------------------------------------------------------
#---------------------code by Dr.James Atwiine----------------------------
#-------------------------------------------------------------------------

   
#-----------POST SAVE------------------------
class SavedPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    saved_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.profile.firstname} saved {self.post.content}"
#-------------------------------------------------------------------------
#---------------------code by Dr.James Atwiine----------------------------
#-------------------------------------------------------------------------
    

#-----------------PROFILE----------------------------------
class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    #profile_pic=models.ImageField(upload_to='img/profile/',blank=True, null=True)
    profile_pic = CloudinaryField('img/profile/', blank=True, null=True )
    firstname=models.CharField(max_length=50, blank=True, null=True)
    lastname=models.CharField(max_length=50, blank=True, null=True)
    bio=models.TextField(blank=True)
    location=models.CharField(max_length=100, blank=True, null=True)
    follows=models.ManyToManyField("self",
            symmetrical=False,
            blank=True,
            related_name="followed_by")

    def __str__(self):
         return self.user.username
    
# --------------------Create a profile for new user----------------------
def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = Profile(user=instance)
        user_profile.save()
        #--Have the users follow themselves------
        user_profile.follows.set([instance.profile.id])
        user_profile.save()
post_save.connect(create_profile, sender=User)
#-------------------------------------------------------------------------
#---------------------code by Dr.James Atwiine----------------------------
#-------------------------------------------------------------------------    

#------------------STORY-----------------------------not using it afterall-------
class Story(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='img/stories/', blank=True, null=True)
    video = models.FileField(upload_to='videos/stories/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.created_at = timezone.now()
        super(Story, self).save(*args, **kwargs)

    def delete_after_12_hours(self):
        if timezone.now() > self.created_at + timedelta(hours=12):
            self.delete()

    def __str__(self):
        return f"{self.author.username}'s story"
#-------------------------------------------------------------------------
#---------------------code by Dr.James Atwiine----------------------------
#-------------------------------------------------------------------------   

#---------------COMMENTS-------------------------------
class Comments(models.Model):
    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s comment on {self.post.content}"
#-------------------------------------------------------------------------
#---------------------code by Dr.James Atwiine----------------------------
#-------------------------------------------------------------------------   

#----------------MOVIE---------------------------
class Movie(models.Model):
    title=models.CharField(max_length=50, blank=True, null=True)
    description = models.TextField()
    actors = models.TextField()
    rating=models.CharField(max_length=50, blank=True, null=True)
    category=models.CharField(max_length=50, blank=True, null=True)
    #thumbnail = models.ImageField(upload_to = 'img/movie/', blank=True, null=True ) 
    thumbnail = CloudinaryField('img/movie/', blank=True, null=True )
    #movie = models.FileField(upload_to='videos/movie/', blank=True, null=True)
    movie = CloudinaryField('videos/movie/', resource_type='video', blank=True, null=True)
    author = models.ForeignKey(User, on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} movie by {self.author.username} on {self.created_at}"
#-------------------------------------------------------------------------
#---------------------code by Dr.James Atwiine----------------------------
#-------------------------------------------------------------------------


#----------------MUSIC---------------------------
class Music(models.Model):
    title=models.CharField(max_length=50, blank=True, null=True)
    artist = models.TextField()
    genre=models.CharField(max_length=50, blank=True, null=True)
    #poster = models.ImageField(upload_to = 'img/music/', blank=True, null=True )
    poster = CloudinaryField('img/music/', blank=True, null=True )
    #song = models.FileField(upload_to='videos/music/', blank=True, null=True)
    song = CloudinaryField('img/audio/', resource_type='raw', blank=True, null=True)
    author = models.ForeignKey(User, on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} song by {self.author.username} on {self.created_at}"
#-------------------------------------------------------------------------
#---------------------code by Dr.James Atwiine----------------------------
#-------------------------------------------------------------------------


#----------------PRODUCT---------------------------
class Product(models.Model):
    item=models.CharField(max_length=50, blank=True, null=True)
    description = models.TextField()
    price=models.CharField(max_length=50, blank=True, null=True)
    #image = models.ImageField(upload_to = 'img/product/', blank=True, null=True ) 
    image = CloudinaryField('img/product/', blank=True, null=True )
    author = models.ForeignKey(User, on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.item} product by {self.author.username} on {self.created_at}"
#-------------------------------------------------------------------------
#---------------------code by Dr.James Atwiine----------------------------
#-------------------------------------------------------------------------


#---------------ORDERS FROM SHOP-------------------------------
class Order(models.Model):
    product = models.ForeignKey(Product, related_name="orders", on_delete=models.CASCADE)
    buyer = models.ForeignKey(User, on_delete=models.CASCADE)
    telephone=models.CharField(max_length=50, blank=True, null=True)
    price=models.CharField(max_length=50, blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.buyer.username}'s order of {self.product.item}" 
#-------------------------------------------------------------------------
#---------------------code by Dr.James Atwiine----------------------------
#-------------------------------------------------------------------------    

    
#----------------PRODUCT---------------------------
class Hostel(models.Model):
    name=models.CharField(max_length=50, blank=True, null=True)
    about = models.TextField()
    residents=models.CharField(max_length=50, blank=True, null=True)
    location=models.CharField(max_length=50, blank=True, null=True)
    price=models.CharField(max_length=50, blank=True, null=True)
    #image = models.ImageField(upload_to = 'img/hostels/', blank=True, null=True )
    image = CloudinaryField('img/hostels/', blank=True, null=True )
    #video = models.FileField(upload_to='img/hostels/', blank='True', null= 'True')
    video = CloudinaryField('videos/hostels/', resource_type='video', blank=True, null=True) 
    contact=models.CharField(max_length=50, blank='True', null='True')
    author = models.ForeignKey(User, on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} service by {self.author.username} on {self.created_at}"
#-------------------------------------------------------------------------
#---------------------code by Dr.James Atwiine----------------------------
#-------------------------------------------------------------------------    

#------------------------MESSAGE-----------------------
class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    message = models.TextField()
    #image = models.ImageField(upload_to = 'img/message/', blank=True, null=True)
    image = CloudinaryField('img/message/', blank=True, null=True )
    seen = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
#-------------------------------------------------------------------------
#---------------------code by Dr.James Atwiine----------------------------
#-------------------------------------------------------------------------
