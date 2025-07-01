from django.shortcuts import render,HttpResponse,redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from .models import Post, Profile, Story, Comments, Movie, Order,Message,SavedPost
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from .forms import *

def terms(request):
    return render(request, 'terms/terms.html')
#------------------SIGNUP, LOGIN, LOGOUT START HERE -------------------
#-------------------------------------------------------------------------
#---------------------code by Dr.James Atwiine----------------------------
#-------------------------------------------------------------------------
#--------------HOME PAGE-----------------------------------------
@login_required
def HomePage(request):
    profile=Profile.objects.get(user=request.user)

    followed_users=request.user.profile.follows.all()
    posts=Post.objects.filter(author_id__in=followed_users.values_list('user_id', flat=True)).order_by('-created_at')
    stories=Story.objects.filter(author_id__in=followed_users.values_list('user_id', flat=True)).order_by('-created_at')
    
    followers=request.user.profile.followed_by.exclude(id__in=request.user.profile.follows.all())
    saved_posts = SavedPost.objects.filter(user=request.user).values_list('post_id', flat=True)

    #---------------------Messages on the right------------------------------
    messages=[]
    followerz=profile.follows.all()
    for follow in followerz:
        conversation_messages = Message.objects.filter(
            (Q(sender=profile.user) & Q(receiver=follow.user)) |
            (Q(sender = follow.user) & Q(receiver=profile.user))
        ).order_by('-timestamp')

        if conversation_messages.exists():
            latest_message=conversation_messages.first()
            messages.append({
                'follow':follow,
                'latest_message':latest_message
            })

    post_form = Postform()
    story_form = StoryForm()


    if request.method == 'POST':
        if 'post_submit' in request.POST:
            post_form = Postform(request.POST, request.FILES)
            if post_form.is_valid():
                post_content = request.POST.get('content')
                post_media = request.FILES.get('media')
                post = Post(
                    content=post_content,
                    author=request.user
                )
                if post_media:
                    file_type = post_media.content_type.split('/')[0]
                    if file_type == 'image':
                        post.image = post_media
                    elif file_type == 'video':
                        post.video = post_media
                        
                post.save()
                return redirect('home')
        elif 'story_submit' in request.POST:
            story_form = StoryForm(request.POST, request.FILES)
            if story_form.is_valid():
                media = request.FILES.get('media')
                if media.content_type.startswith('image'):
                    story=Story(author=request.user, image=media)
                elif media.content_type.startswith('video'):
                    story=Story(author=request.user, video=media)

                story.save()
                return redirect('home')

        #for comment    
        elif 'comment_submit' in request.POST:
            post_id = request.POST.get('post_id')
            post = Post.objects.get(id=post_id)
            comment = Comments.objects.create(post=post, user=request.user, body=request.POST.get('body'))
            comment.save()
            return redirect('home')

    return render(request, 'another home/home.html', 
    {'post_form': post_form, 
    'story_form': story_form, 
    'posts': posts, 
    'stories': stories, 
    'profile': profile,
    'messages':messages,
    'followers':followers,
    'saved_posts':saved_posts})   
#--------------HOME PAGE END HERE-----------------------------------------
#-------------------------------------------------------------------------
#---------------------code by Dr.James Atwiine----------------------------
#-------------------------------------------------------------------------
#-------POST LIKE--------------------------------
from django.http import JsonResponse
@login_required

def post_like(request, pk):
    post = get_object_or_404(Post, id=pk)
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True
    like_count = post.likes.count()
    return JsonResponse({'liked': liked, 'like_count': like_count})
#-------POST LIKE END HERE--------------------------------
#-------------------------------------------------------------------------
#---------------------code by Dr.James Atwiine----------------------------
#-------------------------------------------------------------------------
#--------------------POST SAVE---------------------
@login_required
def post_save(request, pk):
    post = get_object_or_404(Post, id=pk)
    savedpost = SavedPost.objects.filter(user=request.user, post=post)
    if savedpost.exists():
        savedpost.delete()
        saved = False
    else:
        SavedPost.objects.create(user=request.user, post=post)
        saved = True
    return JsonResponse({'saved': saved})
#--------------------POST SAVE END  HERE---------------------
#-------------------------------------------------------------------------
#---------------------code by Dr.James Atwiine----------------------------
#-------------------------------------------------------------------------
#------------------BOOKMARKED/SAVED POSTS---------------------
@login_required
def bookmark(request):
    profile=Profile.objects.get(user=request.user)
    followers=request.user.profile.followed_by.exclude(id__in=request.user.profile.follows.all())

    query=request.GET.get('q')
    if query:
        posts = Post.objects.filter(
            Q(content__icontains=query) |
            Q(savedpost__user=request.user)
            ).order_by('-savedpost__saved_at')
    else:
        posts = Post.objects.filter(savedpost__user=request.user).order_by('-savedpost__saved_at')

    #---------------------Messages on the right------------------------------
    messages=[]
    followerz=profile.follows.all()
    for follow in followerz:
        conversation_messages = Message.objects.filter(
            (Q(sender=profile.user) & Q(receiver=follow.user)) |
            (Q(sender = follow.user) & Q(receiver=profile.user))
        ).order_by('-timestamp')

        if conversation_messages.exists():
            latest_message=conversation_messages.first()
            messages.append({
                'follow':follow,
                'latest_message':latest_message
            })

    if request.method=='POST':
        if 'comment_submit' in request.POST:
            post_id = request.POST.get('post_id')
            post = Post.objects.get(id=post_id)
            comment = Comments.objects.create(post=post, user=request.user, body=request.POST.get('body'))
            comment.save()
            return redirect('bookmark')
        
    return render(request, 'another home/bookmark.html', {'posts':posts,
                                                          'profile':profile,
                                                          'messages':messages,
                                                          'followers':followers}) 
#------------------BOOKMARKED/SAVED POSTS END HERE---------------------
#-------------------------------------------------------------------------
#---------------------code by Dr.James Atwiine----------------------------
#-------------------------------------------------------------------------
#------------------DISCOVER POSTS---------------------
@login_required
def discover(request):

    query=request.GET.get('q')
    if query:
        posts = Post.objects.filter(
            Q(author__profile__firstname__icontains=query) |
            Q(author__profile__lastname__icontains=query) |
            Q(content__icontains=query)
            ).order_by('-id')
    else:
        posts = Post.objects.all().order_by('-id')

    profile=Profile.objects.get(user=request.user)
    
    followers=request.user.profile.followed_by.exclude(id__in=request.user.profile.follows.all()) #---for requests on the right--

    #---------------------Messages on the right------------------------------
    messages=[]
    followerz=profile.follows.all()
    for follow in followerz:
        conversation_messages = Message.objects.filter(
            (Q(sender=profile.user) & Q(receiver=follow.user)) |
            (Q(sender = follow.user) & Q(receiver=profile.user))
        ).order_by('-timestamp')

        if conversation_messages.exists():
            latest_message=conversation_messages.first()
            messages.append({
                'follow':follow,
                'latest_message':latest_message
            })

    if request.method=='POST':
        if 'comment_submit' in request.POST:
            post_id = request.POST.get('post_id')
            post = Post.objects.get(id=post_id)
            comment = Comments.objects.create(post=post, user=request.user, body=request.POST.get('body'))
            comment.save()
            return redirect('discover')

    return render(request, 'another home/discover.html', {'posts':posts,
                                                          'profile':profile,
                                                          'messages':messages,
                                                          'followers':followers})
#------------------DISCOVER POSTS END HERE---------------------
#-------------------------------------------------------------------------
#---------------------code by Dr.James Atwiine----------------------------
#-------------------------------------------------------------------------
#-------------MY POSTS------------------------
@login_required
def my_posts(request):

    query=request.GET.get('q')
    if query:
        posts = Post.objects.filter(content__icontains=query,author=request.user).order_by('-id')
    else:
        posts = Post.objects.filter(author=request.user).order_by('-id')

    profile=Profile.objects.get(user=request.user)
    
    followers=request.user.profile.followed_by.exclude(id__in=request.user.profile.follows.all()) #---for requests on the right--

    #---------------------Messages on the right------------------------------
    messages=[]
    followerz=profile.follows.all()
    for follow in followerz:
        conversation_messages = Message.objects.filter(
            (Q(sender=profile.user) & Q(receiver=follow.user)) |
            (Q(sender = follow.user) & Q(receiver=profile.user))
        ).order_by('-timestamp')

        if conversation_messages.exists():
            latest_message=conversation_messages.first()
            messages.append({
                'follow':follow,
                'latest_message':latest_message
            })

    if request.method=='POST':
        if 'comment_submit' in request.POST:
            post_id = request.POST.get('post_id')
            post = Post.objects.get(id=post_id)
            comment = Comments.objects.create(post=post, user=request.user, body=request.POST.get('body'))
            comment.save()
            return redirect('discover')

    return render(request, 'another home/my_posts.html', {'posts':posts,
                                                          'profile':profile,
                                                          'messages':messages,
                                                          'followers':followers})
#-------------MY POSTS END HERE------------------------
#-------------------------------------------------------------------------
#---------------------code by Dr.James Atwiine----------------------------
#-------------------------------------------------------------------------
#--------POST DELETE-----------------------
@login_required
def delete_post(request,pk):
    post=get_object_or_404(Post,pk=pk)
    if post.author==request.user:
        post.delete()
    return redirect('my_posts')
#--------POST DELETE END HERE-----------------------
#-------------------------------------------------------------------------
#---------------------code by Dr.James Atwiine----------------------------
#-------------------------------------------------------------------------
#-------------------------SIGNUP------------------------
def SignupPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')
        gender = request.POST.get('gender')
        if pass1 != pass2:
            return HttpResponse("Your password and comfirm password are not the same.")
        else:
            my_user = User.objects.create_user(username,email,pass1)  
            my_user.save()
            return redirect('login')

    return render(request, 'login&signup/signup.html')
#-------------------------SIGNUP END HERE------------------------
#-------------------------------------------------------------------------
#---------------------code by Dr.James Atwiine----------------------------
#-------------------------------------------------------------------------
#-----------------------LOGIN ------------------------------
def LoginPage(request):
    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['pass']
        user = authenticate(request,username=username,password=pass1) 
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            return HttpResponse("Attention, Username or password is incorrect")
    return render(request, 'login&signup/login.html')
#-----------------------LOGIN END HERE ------------------------------
#-------------------------------------------------------------------------
#---------------------code by Dr.James Atwiine----------------------------
#-------------------------------------------------------------------------
#----------------------------LOGOUT---------------------------
def Logout(request):
    return redirect('login')
#----------------------------LOGOUT END HERE---------------------------
#-------------------------------------------------------------------------
#---------------------code by Dr.James Atwiine----------------------------
#-------------------------------------------------------------------------
#------------PROFILE PAGE------------------------------
@login_required
def profile(request):
    profile=Profile.objects.get(user=request.user)
    suggestion=Profile.objects.all().order_by('-follows')
    followers=request.user.profile.followed_by.exclude(id__in=request.user.profile.follows.all())
    
    query=request.GET.get('q')
    if query:
        suggestion=Profile.objects.filter(firstname__icontains=query) 

   #---------------------Messages on the right------------------------------
    messages=[]
    followerz=profile.follows.all()
    for follow in followerz:
        conversation_messages = Message.objects.filter(
            (Q(sender=profile.user) & Q(receiver=follow.user)) |
            (Q(sender = follow.user) & Q(receiver=profile.user))
        ).order_by('-timestamp')

        if conversation_messages.exists():
            latest_message=conversation_messages.first()
            messages.append({
                'follow':follow,
                'latest_message':latest_message
            })

    if request.method =='POST':
        if 'product_submit' in request.POST:
            product =Product(item=request.POST.get('item'),
                        description=request.POST.get('description'),
                        price=request.POST.get('price'),
                        image=request.FILES.get('image'),
                        author=request.user,
                        )
            product.save()
            return redirect('shop')
        elif 'movie_submit' in request.POST:
            movie =Movie(title=request.POST.get('title'),
                     description=request.POST.get('description'),
                     actors=request.POST.get('actors'),
                     rating=request.POST.get('rating'),
                     category=request.POST.get('category'),
                     thumbnail=request.FILES.get('poster'),
                     movie=request.FILES.get('movie'),
                     author=request.user,
                     )
            movie.save()
            return redirect('movie')
        elif 'hostel_submit' in request.POST:
            hostel = Hostel(
                author=request.user,
                name=request.POST.get('name'),
                about=request.POST.get('about'),
                residents=request.POST.get('residents'),
                location=request.POST.get('location'),
                price=request.POST.get('price'),
                image=request.FILES.get('image'),
                video=request.FILES.get('video'),
                contact=request.POST['contact']
            )
            hostel.save()
            return redirect('hostel')
        elif 'music_submit' in request.POST:
            music =Music(title=request.POST.get('title'),
                     artist=request.POST.get('artist'),
                     genre=request.POST.get('genre'),
                     poster=request.FILES.get('poster'),
                     song=request.FILES.get('song'),
                     author=request.user,
                     )
            music.save()
            return redirect('music')
        
        elif 'order_submit' in request.POST:
            product_id=request.POST.get('product_id')
            product=Product.objects.get(id=product_id)
            buyer=request.user
            telephone=request.POST.get('telephone')
            price=request.POST.get('price')
            
            order=Order.objects.create(product=product,buyer=buyer,telephone=telephone,price=price)
            order.save()
            return redirect('profile')
    return render(request, 'profile/profile-page.html', {'profile':profile,
                                                         'suggestion':suggestion,
                                                         'messages':messages,
                                                         'followers':followers}) 
#------------PROFILE PAGE END HERE------------------------------
#-------------------------------------------------------------------------
#---------------------code by Dr.James Atwiine----------------------------
#-------------------------------------------------------------------------
#------------VIEW PROFILE PAGE------------------------------
@login_required
def view_profile(request, pk):
    profile=Profile.objects.get(user=request.user)
    follower=Profile.objects.get(id=pk)
    followers=request.user.profile.followed_by.exclude(id__in=request.user.profile.follows.all()) #for requests in the right

    #---------------------Messages on the right------------------------------
    messages=[]
    followerz=profile.follows.all()
    for follow in followerz:
        conversation_messages = Message.objects.filter(
            (Q(sender=profile.user) & Q(receiver=follow.user)) |
            (Q(sender = follow.user) & Q(receiver=profile.user))
        ).order_by('-timestamp')

        if conversation_messages.exists():
            latest_message=conversation_messages.first()
            messages.append({
                'follow':follow,
                'latest_message':latest_message
            })

    if request.method== 'POST':
        if 'order_submit' in request.POST:
            product_id=request.POST.get('product_id')
            product=Product.objects.get(id=product_id)
            buyer=request.user
            telephone=request.POST.get('telephone')
            price=request.POST.get('price')
            
            order=Order.objects.create(product=product,buyer=buyer,telephone=telephone,price=price)
            order.save()
            return redirect('view_profile',pk=follower.id)
        
    return render(request, 'profile/view-profile-page.html', {'profile':profile,
                                                              'follower':follower,
                                                              'messages':messages,
                                                              'followers':followers})
#------------VIEW PROFILE PAGE END HERE------------------------------
#-------------------------------------------------------------------------
#---------------------code by Dr.James Atwiine----------------------------
#-------------------------------------------------------------------------
#---------------------------FOLLOW-----------------------------
@login_required
def follow_user(request, pk):
    user_to_follow = get_object_or_404(Profile, pk=pk)
    if request.user.profile in user_to_follow.followed_by.all():
        user_to_follow.followed_by.remove(request.user.profile)
    else:
        user_to_follow.followed_by.add(request.user.profile)
    return redirect('view_profile', pk=pk)
#---------------------------FOLLOW END HERE-----------------------------
#-------------------------------------------------------------------------
#---------------------code by Dr.James Atwiine----------------------------
#-------------------------------------------------------------------------
#-----------------------DECLINE CONNECT-----------------------------
@login_required
def decline_user(request, pk):
    user_to_decline = get_object_or_404(Profile, pk=pk)
    if user_to_decline in request.user.profile.followed_by.all():
        request.user.profile.followed_by.remove(user_to_decline)

    return redirect('view_profile', pk=pk)
#-----------------------DECLINE CONNECT END HERE-----------------------------
#-------------------------------------------------------------------------
#---------------------code by Dr.James Atwiine----------------------------
#-------------------------------------------------------------------------
#---------------------MOVIE -------------------------------
@login_required
def movie(request):
    profile=Profile.objects.get(user=request.user) 
    actions=Movie.objects.filter(category__icontains='action')
    followers=request.user.profile.followed_by.exclude(id__in=request.user.profile.follows.all()) #for requests in the right
    
    query = request.GET.get('q')
    if query:
        movie=Movie.objects.filter(title__icontains=query)
    else:
        movie=Movie.objects.all().order_by('-created_at')
    
    #---------------------Messages on the right------------------------------
    messages=[]
    followerz=profile.follows.all()
    for follow in followerz:
        conversation_messages = Message.objects.filter(
            (Q(sender=profile.user) & Q(receiver=follow.user)) |
            (Q(sender = follow.user) & Q(receiver=profile.user))
        ).order_by('-timestamp')

        if conversation_messages.exists():
            latest_message=conversation_messages.first()
            messages.append({
                'follow':follow,
                'latest_message':latest_message
            })
    
    #form=MovieForm()
    if request.method== 'POST':
        movie =Movie(title=request.POST.get('title'),
                     description=request.POST.get('description'),
                     actors=request.POST.get('actors'),
                     rating=request.POST.get('rating'),
                     category=request.POST.get('category'),
                     thumbnail=request.FILES.get('poster'),
                     movie=request.FILES.get('movie'),
                     author=request.user,
                     )
        movie.save()
        return redirect('movie')

    
    return render(request, 'Movie/movie.html', {'profile':profile,
                                                'movie':movie,
                                                'messages':messages,
                                                'followers':followers,
                                                'actions':actions})    
#---------------------MOVIE END HERE-------------------------------
#-------------------------------------------------------------------------
#---------------------code by Dr.James Atwiine----------------------------
#-------------------------------------------------------------------------
#---------------------VIEW MOVIE -------------------------------
@login_required
def viewmovie(request, pk):
    profile=Profile.objects.get(user=request.user)
    movie = get_object_or_404(Movie, pk=pk)
    movies=Movie.objects.all().order_by('-created_at')
    followers=request.user.profile.followed_by.exclude(id__in=request.user.profile.follows.all()) #for requests in the right


    #---------------------Messages on the right------------------------------
    messages=[]
    followerz=profile.follows.all()
    for follow in followerz:
        conversation_messages = Message.objects.filter(
            (Q(sender=profile.user) & Q(receiver=follow.user)) |
            (Q(sender = follow.user) & Q(receiver=profile.user))
        ).order_by('-timestamp')

        if conversation_messages.exists():
            latest_message=conversation_messages.first() 
            messages.append({
                'follow':follow,
                'latest_message':latest_message
            })
    
    return render(request, 'Movie/movi.html', {'profile':profile,
                                               'movie':movie,
                                               'messages':messages,
                                               'followers':followers,
                                               'movies':movies}) 

#---------------------VIEW MOVIE END HERE-------------------------------
#-------------------------------------------------------------------------
#---------------------code by Dr.James Atwiine----------------------------
#-------------------------------------------------------------------------
#------------------MESSAGES---------------------------
@login_required
def messages(request):
    profile=Profile.objects.get(user=request.user)
    follower=profile.follows.all()
    followers=request.user.profile.followed_by.exclude(id__in=request.user.profile.follows.all()) #for requests in the right

    
    messages=[]
    for follow in follower:
        conversation_messages = Message.objects.filter(
            (Q(sender=profile.user) & Q(receiver=follow.user)) |
            (Q(sender = follow.user) & Q(receiver=profile.user))
        ).order_by('-timestamp')

        if conversation_messages.exists():
            latest_message=conversation_messages.first()
            messages.append({
                'follow':follow,
                'latest_message':latest_message
            })
    

    return render(request, 'messages/messages.html', {'profile':profile,
                                                      'follower':follower,
                                                      'followers':followers,
                                                      'messages':messages})
#------------------MESSAGES END HERE---------------------------
#-------------------------------------------------------------------------
#---------------------code by Dr.James Atwiine----------------------------
#-------------------------------------------------------------------------
#------------------------CHATTING------------------------
@login_required
def chat(request, pk): 
    profile=Profile.objects.get(user=request.user)
    follower=profile.follows.get(id=pk)
    followers=request.user.profile.followed_by.exclude(id__in=request.user.profile.follows.all()) #for requests in the right

    chats = Message.objects.filter(
        (Q(sender=profile.user) & Q(receiver=follower.user)) | 
        (Q(sender=follower.user) & Q(receiver=profile.user))
    ).order_by('-timestamp')


    #---------------------Messages on the right------------------------------
    messages=[]
    followerz=profile.follows.all()
    for follow in followerz:
        conversation_messages = Message.objects.filter(
            (Q(sender=profile.user) & Q(receiver=follow.user)) |
            (Q(sender = follow.user) & Q(receiver=profile.user))
        ).order_by('-timestamp')

        if conversation_messages.exists():
            latest_message=conversation_messages.first()
            messages.append({
                'follow':follow,
                'latest_message':latest_message
            })

    

    if request.method == 'POST':
        message = request.POST['message']
        image=request.FILES.get('image')
        receiver_id = request.POST['receiver_id']
        receiver = Profile.objects.get(id=receiver_id)
        Message.objects.create(
            sender=request.user,
            receiver=receiver.user,
            message=message,
            image=image
        )
        return redirect('chat', pk=follower.id)
    return render(request, 'Chat/chat.html', {'profile':profile,
                                              'follower':follower,
                                              'messages':messages,
                                              'followers':followers,
                                              'chats':chats})
#------------------------CHATTING END HERE------------------------
#-------------------------------------------------------------------------
#---------------------code by Dr.James Atwiine----------------------------
#-------------------------------------------------------------------------
#-------------------SHOPPING VIEW------------------------
@login_required
def shop(request):

    followers=request.user.profile.followed_by.exclude(id__in=request.user.profile.follows.all()) #for requests in the right

    query=request.GET.get('q')
    if query:
        product=Product.objects.filter(item__icontains=query)
    else:
        product=Product.objects.all().order_by('-created_at')

    profile=Profile.objects.get(user=request.user)


    #---------------------Messages on the right------------------------------
    messages=[]
    followerz=profile.follows.all()
    for follow in followerz:
        conversation_messages = Message.objects.filter(
            (Q(sender=profile.user) & Q(receiver=follow.user)) |
            (Q(sender = follow.user) & Q(receiver=profile.user))
        ).order_by('-timestamp')

        if conversation_messages.exists():
            latest_message=conversation_messages.first()
            messages.append({
                'follow':follow,
                'latest_message':latest_message
            })


    

    if request.method== 'POST':
        if 'product_submit' in request.POST:
            product =Product(item=request.POST.get('item'),
                        description=request.POST.get('description'),
                        price=request.POST.get('price'),
                        image=request.FILES.get('image'),
                        author=request.user,
                        )
            product.save()
            return redirect('shop')
        elif 'order_submit' in request.POST:
            product_id=request.POST.get('product_id')
            product=Product.objects.get(id=product_id)
            buyer=request.user
            telephone=request.POST.get('telephone')
            price=request.POST.get('price')
            
            order=Order.objects.create(product=product,buyer=buyer,telephone=telephone,price=price)
            order.save()
            return redirect('shop')

            
    return render(request, 'shop/shopping.html', {'profile':profile,
                                                  'followers':followers,
                                                  'messages':messages,
                                                  'product':product}) 
#-------------------SHOPPING VIEW END HERE------------------------
#-------------------------------------------------------------------------
#---------------------code by Dr.James Atwiine----------------------------
#-------------------------------------------------------------------------
#-------------------VIEW ORDER------------------------
@login_required
def vieworder(request):
    query = request.GET.get('q')
    profile=Profile.objects.get(user=request.user)
    followers=request.user.profile.followed_by.exclude(id__in=request.user.profile.follows.all()) #for requests in the right
    products=Product.objects.filter(author=request.user)

    #---------------------Messages on the right------------------------------
    messages=[]
    followerz=profile.follows.all()
    for follow in followerz:
        conversation_messages = Message.objects.filter(
            (Q(sender=profile.user) & Q(receiver=follow.user)) |
            (Q(sender = follow.user) & Q(receiver=profile.user))
        ).order_by('-timestamp')

        if conversation_messages.exists():
            latest_message=conversation_messages.first()
            messages.append({
                'follow':follow,
                'latest_message':latest_message
            })

    if query:
        orders = Order.objects.filter(
            product__in = products, 
            product__item__icontains=query
            ).order_by('-date_added')
    else:
        orders = Order.objects.filter(product__in = products).order_by('-date_added')

    
    return render (request, 'shop/orders.html', {'profile':profile,
                                                 'followers':followers,
                                                 'messages':messages,
                                                 'orders':orders,}) 
#-------------------VIEW ORDER END HERE------------------------
#-------------------------------------------------------------------------
#---------------------code by Dr.James Atwiine----------------------------
#-------------------------------------------------------------------------
#----------------------HOSTEL-----------------------
def hostel(request):
    profile=Profile.objects.get(user=request.user)
    followers=request.user.profile.followed_by.exclude(id__in=request.user.profile.follows.all()) #for requests in the right
    query1=request.GET.get('s')
    query2=request.GET.get('l')
    query3=request.GET.get('p')

    if query1:
        hostel=Hostel.objects.filter(name__icontains=query1).order_by('-created_at')
    elif query2:
        hostel=Hostel.objects.filter(location__icontains=query2).order_by('-created_at')
    elif query3:
        hostel=Hostel.objects.filter(price__icontains=query3).order_by('-created_at')
    elif query1 and query2 and query3:
        hostel=Hostel.objects.filter(name__icontains=query1,location__icontains=query2,price__icontains=query3).order_by('-created_at')
    else:
        hostel=Hostel.objects.all().order_by('-created_at') 


    #---------------------Messages on the right------------------------------
    messages=[]
    followerz=profile.follows.all()
    for follow in followerz:
        conversation_messages = Message.objects.filter(
            (Q(sender=profile.user) & Q(receiver=follow.user)) |
            (Q(sender = follow.user) & Q(receiver=profile.user))
        ).order_by('-timestamp')

        if conversation_messages.exists():
            latest_message=conversation_messages.first()
            messages.append({
                'follow':follow,
                'latest_message':latest_message
            })
    

    if request.method=='POST':
        if 'hostel_submit' in request.POST:
            hostel = Hostel(
                author=request.user,
                name=request.POST.get('name'),
                about=request.POST.get('about'),
                residents=request.POST.get('residents'),
                location=request.POST.get('location'),
                price=request.POST.get('price'),
                image=request.FILES.get('image'),
                video=request.FILES.get('video'),
                contact=request.POST['contact']
            )
            hostel.save()
            return redirect('hostel')
    return render(request, 'hostel/hostel.html', {'profile':profile,
                                                  'followers':followers,
                                                  'messages':messages,
                                                  'hostel':hostel})
#----------------------HOSTEL END HERE-----------------------
#-------------------------------------------------------------------------
#---------------------code by Dr.James Atwiine----------------------------
#-------------------------------------------------------------------------
#------------------------MUSIC VIEW------------------------
@login_required
def music(request):
    query=request.GET.get('q')
    if query:
        music=Music.objects.filter(title__icontains=query)
    else:
        music=Music.objects.all().order_by('-created_at')

    profile=Profile.objects.get(user=request.user)
    followers=request.user.profile.followed_by.exclude(id__in=request.user.profile.follows.all()) #for requests in the right

    #---------------------Messages on the right------------------------------
    messages=[]
    followerz=profile.follows.all()
    for follow in followerz:
        conversation_messages = Message.objects.filter(
            (Q(sender=profile.user) & Q(receiver=follow.user)) |
            (Q(sender = follow.user) & Q(receiver=profile.user))
        ).order_by('-timestamp')

        if conversation_messages.exists():
            latest_message=conversation_messages.first()
            messages.append({
                'follow':follow,
                'latest_message':latest_message
            })

    if request.method== 'POST':
        music =Music(title=request.POST.get('title'),
                     artist=request.POST.get('artist'),
                     genre=request.POST.get('genre'),
                     poster=request.FILES.get('poster'),
                     song=request.FILES.get('song'),
                     author=request.user,
                     )
        music.save()
        return redirect('music')
    return render(request, 'music/music.html', {"profile":profile,
                                                'followers':followers,
                                                'messages':messages,
                                                'music':music})
#------------------------MUSIC END HERE-----------------------
#-------------------------------------------------------------------------
#---------------------code by Dr.James Atwiine----------------------------
#-------------------------------------------------------------------------
#---------------------ACCOUNT SETTINGS--------------------------
@login_required 
def acc_settings(request):
    try:
        profile=Profile.objects.get(user=request.user)

    except Profile.DoesNotExist:
        profile=Profile.objects.create(User=request.user)

    followers=request.user.profile.followed_by.exclude(id__in=request.user.profile.follows.all()) #for requests in the right

    #---------------------Messages on the right------------------------------
    messages=[]
    followerz=profile.follows.all()
    for follow in followerz:
        conversation_messages = Message.objects.filter(
            (Q(sender=profile.user) & Q(receiver=follow.user)) |
            (Q(sender = follow.user) & Q(receiver=profile.user))
        ).order_by('-timestamp')

        if conversation_messages.exists():
            latest_message=conversation_messages.first()
            messages.append({
                'follow':follow,
                'latest_message':latest_message
            })

    if request.method == 'POST':
        form=ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile') 
        
    else:
        form=ProfileForm(instance=profile)

    return render(request, 'account settings/acc-sets.html', {'profile':profile,
                                                              'followers':followers,
                                                              'messages':messages,
                                                              'form':form})
#---------------------ACCOUNT SETTINGS END HERE--------------------------
#-------------------------------------------------------------------------
#-------------------------------------------------------------------------
#---------------------code by Dr.James Atwiine----------------------------
#-------------------------------------------------------------------------
#-------------------------------------------------------------------------



