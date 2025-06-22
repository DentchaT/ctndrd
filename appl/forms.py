from django import forms 
from .models import Post, Profile,Story, Movie, Music, Product,Hostel
#-------------------------------------------------------------------------
#---------------------code by Dr.James Atwiine----------------------------
#-------------------------------------------------------------------------

#-------POST FORM--------------------------------
class Postform(forms.ModelForm):
    class Meta:
        model = Post 
        fields = ['content'] 

        widgets = {
            'content': forms.Textarea(attrs={'rows':2,'cols': 20})
        }

    def __init__(self, *args, **kwargs):
        super(Postform, self).__init__(*args, **kwargs) 

#-------------------------------------------------------------------------
#---------------------code by Dr.James Atwiine----------------------------
#-------------------------------------------------------------------------
#--------PROFILE FORM------------------------------
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('profile_pic','firstname','lastname','bio','location')

#-------------------------------------------------------------------------
#---------------------code by Dr.James Atwiine----------------------------
#-------------------------------------------------------------------------
#------------STORY FORM--------------------------------
class StoryForm(forms.ModelForm):
    class Meta:
        model = Story
        fields = ()
#-------------------------------------------------------------------------
#---------------------code by Dr.James Atwiine----------------------------
#-------------------------------------------------------------------------

#--------------MOVIE FORM--------------------------
class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ('title','description', 'actors','rating','category','thumbnail','movie')
#-------------------------------------------------------------------------
#---------------------code by Dr.James Atwiine----------------------------
#-------------------------------------------------------------------------

#--------------MUSIC FORM--------------------------
class MusicForm(forms.ModelForm):
    class Meta:
        model = Music
        fields = ('title', 'artist','genre','poster','song')
#-------------------------------------------------------------------------
#---------------------code by Dr.James Atwiine----------------------------
#-------------------------------------------------------------------------

#--------------PRODUCT FORM--------------------------
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('item', 'description','price','image')
#-------------------------------------------------------------------------
#---------------------code by Dr.James Atwiine----------------------------
#-------------------------------------------------------------------------

#---------HOSTEL FORM-----------------
class HostelForm(forms.ModelForm):
    class Meta:
        model=Hostel
        fields=('name','about','residents','image','contact','price','location','video') 
#-------------------------------------------------------------------------
#---------------------code by Dr.James Atwiine----------------------------
#-------------------------------------------------------------------------