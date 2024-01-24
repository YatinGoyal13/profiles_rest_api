from django.urls import path
from . import views
from django.urls import include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('hello-viewset',views.HelloViewSet,basename='hello-viewset')
router.register('profile',views.UserProfileViewset)

urlpatterns=[
    path('hello-view/',views.HelloApiView.as_view()),
    path('',include(router.urls)),
]
