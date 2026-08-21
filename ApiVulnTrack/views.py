from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import PermissionDenied
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from projects.models import Project
from vulnerabilities.models import Vulnerability
from .serializers import VulnerabilitySerializer, ProjectSerializer


class VulnerabilityViewSet(ModelViewSet):
    queryset = Vulnerability.objects.all()
    serializer_class = VulnerabilitySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['created_at']


    def perform_create(self, serializer):
        serializer.save(reporter=self.request.user)

    def perform_update(self, serializer):
        if self.request.user != serializer.instance.reporter and not self.request.user.is_staff:
            raise PermissionDenied("You can't update a vulnerability")
        serializer.save()

class ProjectViewSet(ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    filter_backends = [DjangoFilterBackend]
    permission_classes = [IsAuthenticated]
    filterset_fields = ['name','is_active']