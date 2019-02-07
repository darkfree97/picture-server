from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()

router.register(r'users', views.UserRegistrationAuthorization, base_name='users')
router.register(r'moderators', views.ModeratorRegistrationAuthorization, base_name='moderators')

router.register(r'categories', views.CategoryViewSet, base_name='categories')
router.register(r'hash-tags', views.HashTagViewSet, base_name='hash-tags')
router.register(r'images', views.ImageViewSet, base_name='images')

urlpatterns = router.urls
