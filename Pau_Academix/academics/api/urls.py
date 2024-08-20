from rest_framework.routers import DefaultRouter
from academics.api.views import FacultyViewSet, DepartmentViewSet, ClassViewSet, SubjectViewSet

router = DefaultRouter()
router.register(r'faculties', FacultyViewSet)
router.register(r'departments', DepartmentViewSet)
router.register(r'classes',ClassViewSet)
router.register(r'subjects',SubjectViewSet)


urlpatterns = [


]

urlpatterns += router.urls