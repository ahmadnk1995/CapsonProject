"""ecommerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from mainapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.MainView.as_view(),name="main"),
    path('contact',views.ContactView.as_view(),name="contact"),
    path('login',views.LoginView,name="login"),
    path('cart/chekout',views.CheckoutView,name="chekout"),
    path('reg',views.RegestrView,name="reg"),
    path('logout/', views.LogoutView,name="logout"),
    path('categories',views.CategoriesView.as_view(),name="categories"),
    path('products/<int:fk>', views.ProductsListView,name="products"),
    path('product/<int:pk>', views.ProductDetailView.as_view(),name="product"),
    path('cart/', views.chartView,name="cart"),
    path('delete/<int:dproduct_id>', views.DeleteFromChartView,name="delete"),
    path('cart/<int:product_id>', views.AddToChartView,name="chart"),
    path('comment/<int:pid>', views.Addcomment,name="comment"),
    path('search', views.searchView,name="search"),
    
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
