from rest_framework import routers
from Venter import views as myapp_views

router = routers.DefaultRouter()
router.register(r'categories', myapp_views.CategoryViewset)
router.register(r'organisations', myapp_views.OrganisationViewset)