"""
URL configuration for djangoecommercetwo project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_view
from django.urls import path

from app import views
from app.forms import *

urlpatterns = [
                  path('', views.home, name='home'),
                  path('contact/', views.home, name='contact'),
                  path('add-to-cart/', views.add_to_cart, name='add_to_cart'),
                  path('cart/', views.show_cart, name='show_cart'),
                  path('checkout/', views.checkout, name='checkout'),

                  path('aboout/', views.home, name='about'),
                  path('profile/', views.ProfileView.as_view(), name='profile'),
                  path('address/', views.address, name='address'),
                  path('category/<slug:val>', views.CategoryView.as_view(), name='category'),
                  # path('category-detail/<val>', views.CategoryView.as_view(), name='category-title'),
                  path('product-detail/<int:pk>', views.ProductDetail.as_view(), name='product-detail'),
                  path('profile-view/<int:pk>', views.ProfileView.as_view(), name='profile-view'),
                  path('registration/', views.CustomerRegistrationView.as_view(), name='customer-registration'),
                  path('accounts/login/',
                       auth_view.LoginView.as_view(template_name='base/login.html', authentication_form=LoginForm),
                       name='login'),
                  path('password-reset/', auth_view.PasswordResetView.as_view(template_name='base/password_reset.html',
                                                                              form_class=MyPasswordResetForm),
                       name='password-reset'),
                  path('password-change/',
                       auth_view.PasswordChangeView.as_view(template_name='base/password_change.html',
                                                            form_class=MyPasswordChangeForm, success_url='/'),
                       name='password-change'),
                  path('password-change-done/',
                       auth_view.PasswordResetView.as_view(template_name='base/password_change_done.html'),
                       name='password-change-done'),
                  path('logout/',
                       auth_view.LogoutView.as_view(next_page='login'),
                       name='logout'),



                  path('password-reset/', auth_view.PasswordResetView.as_view(template_name='base/password_reset.html',
                                                                              form_class=MyPasswordResetForm),
                       name='password-reset'),

                  path('password-reset/done',
                       auth_view.PasswordResetDoneView.as_view(template_name='base/password_reset_done.html',),name='password-reset-done'),

                  path('password-reset-confirm/<uidb64>/<token>/',
                       auth_view.PasswordResetConfirmView.as_view(template_name='base/password_reset_confirm.html', form_class=MySetPasswordForm),
                       name='password-reset-confirm'),

                  path('password-reset-complete/',
                       auth_view.PasswordResetCompleteView.as_view(template_name='base/password_reset_complete.html'),
                       name='password-reset-complete'),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
