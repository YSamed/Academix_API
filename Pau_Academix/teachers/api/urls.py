from rest_framework.routers import DefaultRouter
from teachers.api.views import TeacherViewSet

router = DefaultRouter()
router.register(r'teachers', TeacherViewSet)

urlpatterns = [

]

urlpatterns += router.urls