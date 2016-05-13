from django.conf.urls import include, url
import views

urlpatterns = [
    url(r'^signup', views.signup),
    url(r'^logout', views.logout),
    url(r'^', views.login),


]