from rest_framework.routers import DefaultRouter
from students.api.views import StudentViewSet

router = DefaultRouter()
router.register(r'students', StudentViewSet)

urlpatterns = [

]

urlpatterns += router.urls