from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from .forms import LoginForm, MyPasswordChangeForm, \
    MyPasswordResetForm, MySetPasswordForm


urlpatterns = [
                  # path('', views.index, name='index'),
                  # path('/<slug:data>', views.ProductView.as_view(), name='indexdata'),
                  path('', views.ProductView.as_view(), name='index'),
                  path('search',views.search,name='search'),
                 # path('checkoutan', views.checkoutan, name='checkoutan'),
                  path('theme', views.theme, name='theme'),
                  path('product-detail/<int:prod_id>', views.ProductDetailView.as_view(), name='product-detail'),
                  path('about', views.about, name='about'),
                  path("add-to-cart/", views.add_to_cart, name='add-to-cart'),
                  path('submit_review/<int:product_id>/', views.submit_review, name='submit_review'),
                  path("cart/", views.show_cart, name='showcart'),
                  path("update_item/", views.updateItem, name='update_item'),
                  path('add-wishlist', views.add_wishlist, name='add_wishlist'),
                  path('my-wishlist', views.my_wishlist, name='my_wishlist'),
                  path("pluscart", views.plus_cart, name='pluscart'),
                  path('profile/', views.ProfileView.as_view(), name='profile'),
                  path('address/', views.address, name='address'),
                  path("minuscart", views.minus_cart, name='minuscart'),
                  path("removecart", views.remove_cart, name='removecart'),
                  # path("add-to-cart/", views.add_to_cart, name='add-to-cart'),
                  path('blog', views.blog, name='blog'),
                  path('blog-single', views.blog_single, name='blog-single'),
                  path('cart', views.cart, name='cart'),
                  path('cartnew/', views.cartnew, name='cartnew'),
                  path('404', views.Pagenotfound, name='404'),
                  path('womens/', views.womens, name='womens'),
                  path('womens/<slug:data>', views.womens, name='womensdata'),
                  path('mens/', views.mens, name='mens'),
                  path('mens/<slug:data>', views.mens, name='mensdata'),
                  # path('profile/', views.ProfileView.as_view(), name='profile'),
                  path('checkout', views.checkout, name='checkout'),
                  path('checkoutnew/', views.CheckoutnewView.as_view(), name='checkoutnew'),
                  path('process_order/', views.processOrder, name="process_order"),
                  #path('checkout1/', views.CheckoutView.as_view(), name='checkout1'),
                  path('filter-data',views.filter_data,name='filter_data'),
                  path('contact-us', views.contact_us, name='contact-us'),
                  # path('login', views.login, name='login'),
                  path('accounts/login/', auth_views.LoginView.as_view
                  (template_name='login.html', authentication_form=LoginForm), name='login'),
                  path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
                  path('passwordchange/', auth_views.PasswordChangeView.as_view
                  (template_name='passwordchange.html', form_class=MyPasswordChangeForm,
                   success_url='/passwordchangedone/'), name='passwordchange'),
                  path("passwordchangedone/", auth_views.PasswordChangeDoneView.
                       as_view(template_name='passwordchangedone.html'),
                       name='passwordchangedone'),
                  path("password-reset/", auth_views.PasswordResetView.as_view(template_name
                                                                               ='password_reset.html',
                                                                               form_class=MyPasswordResetForm),
                       name='password_reset'),
                  path("password-reset/done/", auth_views.PasswordResetDoneView.
                       as_view(template_name='password_reset_done.html'),
                       name='password_reset_done'),
                  path("password-reset-confirm/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.
                       as_view(template_name='password_reset_confirm.html', form_class=
                  MySetPasswordForm),
                       name='password_reset_confirm'),
                  path("password-reset-complete/", auth_views.PasswordResetCompleteView.as_view(template_name
                  ='password_reset_complete.html'),name='password_reset_complete'),
                  # path('signup', views.signup, name='signup'),
                  path('registration/', views.CustomerRegistrationView.as_view(), name='customerregistration'),
                  # path('product-details', views.product_details, name='product-details'),
                  path('shop', views.shop, name='shop'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
