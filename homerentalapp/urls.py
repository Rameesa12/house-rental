"""homerentalapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from myapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.login),
    path('login_post',views.login_post),
    path('changepass',views.changepass),
    path('change_password_post',views.change_password_post),
    path('viewcustomers',views.viewcustomers),
    path('viewhouseowners',views.viewhouseowners),
    path('approve_house_owners/<id>',views.approve_house_owners),
    path('reject_house_owners/<id>',views.reject_house_owners),
    path('viewroomsanddetails/<id>',views.viewroomsanddetails),
    path('view_rating/<id>',views.view_rating),
    path('approved_owners',views.approved_owners),
    path('admin_home',views.admin_home),
    path('logout',views.logout),
#################################################################################################
    path('customer_register',views.customer_register),
    path('customer_register_post',views.customer_register_post),
    path('customer_home',views.customer_home),
    path('customer_view_profile',views.customer_view_profile),
    path('customer_view_house',views.customer_view_house),
    path('customer_book_house/<id>',views.customer_book_house),
    path('user_payment/<id>/<amt>',views.user_payment),
    path('customer_view_request',views.customer_view_request),
    path('customer_sen_rating/<hid>',views.customer_sen_rating),
    path('customer_send_rating_post/<hid>',views.customer_send_rating_post),
    path('customer_chatt/<u>',views.customer_chatt),
    path('customer_chatsnd/<u>',views.customer_chatsnd),
    path('customer_chatrply',views.customer_chatrply),

    #####################################Owner###################################
    path('houseowner_register',views.houseowner_register),
    path('houseowner_register_post',views.houseowner_register_post),
    path('owner_home',views.owner_home),
    path('view_profile',views.view_profile),
    path('view_house',views.view_house),
    path('add_house',views.add_house),
    path('add_house_post',views.add_house_post),
    path('update_house/<id>',views.update_house),
    path('update_house_post/<id>',views.update_house_post),
    path('delete_house/<id>',views.delete_house),
    path('view_request',views.view_request),
    path('approve_request/<id>',views.approve_request),
    path('reject_request/<id>',views.reject_request),
    path('view_payment',views.view_payment),
    path('oview_rating',views.oview_rating),
    path('owner_chatt/<u>',views.owner_chatt),
    path('owner_chatsnd/<u>',views.owner_chatsnd),
    path('owner_chatrply/<u>',views.owner_chatrply),
]
