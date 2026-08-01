from rest_framework.routers import DefaultRouter
from ApiVulnTrack.views import VulnerabilityViewSet, ProjectViewSet
from django.urls import path, include

router = DefaultRouter()

router.register("vulnerabilities", VulnerabilityViewSet)
router.register("projects", ProjectViewSet)

urlpatterns = router.urls