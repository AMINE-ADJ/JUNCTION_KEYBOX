# from django.conf.urls import url
from django.urls import path
from . import views


urlpatterns = [
path('index/', views.index, name="index"),
path('courses/', views.learning_list, name="learning_list"),
path('mes-courses/', views.mescourses, name="learning_list"),
path('course/<int:id>/', views.email_application, name="email_application"),
path('course/<int:id>/quiz/<int:chapiter>/', views.quiz, name="quiz"),
path('add-course/', views.addcourse, name="addcourse"),
path('mycourses/', views.mycourses, name="mycourses"),
path('result/<int:id>/quiz/<int:chapiter>/', views.result, name="result"),
path('course/analyse/', views.courseanalyse, name="courseanalyse"),




path('signup_home',views.signup_home,name='signup_home'),
path('login_home', views.login_home, name="login_home"),
path('logout_view', views.logout_view, name="logout_view"),
]