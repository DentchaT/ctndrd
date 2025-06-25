from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
from django.urls import path
from appl import views 
#-------------------------------------------------------------------------
#---------------------code by Dr.James Atwiine----------------------------
#-------------------------------------------------------------------------
urlpatterns = [
    path('admin/',admin.site.urls),
    path('signup/',views.SignupPage,name='signup'),
    path('login/',views.LoginPage,name='login'),
    path('',views.LoginPage,name='login_page'),
    path('home',views.HomePage,name='home'),
    path('post_like/<int:pk>', views.post_like, name='post_like'),
    path('post_save/<int:pk>', views.post_save, name='post_save'),
    path('my_posts/',views.my_posts,name='my_posts'),
    path('logout/',views.Logout,name='logout'),
    path('profile/',views.profile,name='profile'),
    path('view_profile/<int:pk>/',views.view_profile,name='view_profile'),
    path('delete_post/<int:pk>/',views.delete_post,name='delete_post'),
    path('bookmark/',views.bookmark, name='bookmark'),
    path('discover/',views.discover, name='discover'),
    path('follow/<int:pk>/', views.follow_user, name='follow_user'),
    path('decline/<int:pk>/', views.decline_user, name='decline_user'),
    path('movie/',views.movie,name='movie'),
    path('viewmovie/<int:pk>/',views.viewmovie,name='viewmovie'),
    path('chat/<int:pk>/', views.chat, name='chat'),
    path('shop/',views.shop,name='shop'),
    path('orders/',views.vieworder,name='orders'),
    path('hostel/',views.hostel,name='hostel'),
    path('music', views.music, name='music'),
    path('acc-settings', views.acc_settings, name='account-settings'),
    path('messages/',views.messages, name='messages'),
    path('terms', views.terms, name='terms'),
]

#-------------------------------------------------------------------------
#---------------------code by Dr.James Atwiine----------------------------
#-------------------------------------------------------------------------
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#-------------------------------------------------------------------------
#---------------------code by Dr.James Atwiine----------------------------
#-------------------------------------------------------------------------