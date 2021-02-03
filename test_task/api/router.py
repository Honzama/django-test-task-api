from rest_framework import routers
from api import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'categories', views.CategoryViewSet)
router.register(r'tags', views.TagViewSet)
router.register(r'blogs', views.BlogViewSet)
router.register(r'comments', views.CommentViewSet)
