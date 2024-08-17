
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('<slug:category_slug>', views.ourproduct, name='product_by_category'),
    path('base/', views.base, name='base'),
    path('ourproduct/', views.ourproduct, name='ourproduct'),
    path('settlement/', views.settlement, name='settlement'),
    path('contact/', views.contact, name='contact'),
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('signout/', views.signout, name='signout'),
    path('about/', views.about, name='about'),
    path('receivedmessage/', views.receivedmessage, name='receivedmessage'),
    path('detailed_product/<int:id>/', views.detailed_product, name='detailed_product'),
    path('ItemPost/', views.ItemPost.as_view(), name='ItemPost'),
    path('add_to_cart/<int:id>/', views.add_to_cart, name="add_to_cart"),
    path('remove_from_cart/<int:id>/', views.remove_from_cart, name="remove_from_cart"),
    path('remove_single_from_cart/<int:id>/', views.remove_single_from_cart, name="remove_single_from_cart"),
    path('order_summary/', views.OrderSummaryView.as_view(), name='order_summary'),

]

