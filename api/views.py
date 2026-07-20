from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from projects.models import Project
from vulnerabilities.models import Vulnerability
from .serializers import VulnerabilitySerializer, ProjectSerializer


class VulnerabilityViewSet(ModelViewSet):
    queryset = Vulnerability.objects.all()
    serializer_class = VulnerabilitySerializer
    permission_classes = [IsAuthenticated]
    def perform_create(self, serializer):
        serializer.save(reporter=self.request.user)

    def perform_update(self, serializer):
        # Tylko reporter lub staff
        if self.request.user != serializer.instance.reporter and not self.request.user.is_staff:
            return Response({'detail': 'Permission denied'}, status=403)
        serializer.save()

    @action(detail=False,methods=['get'])
    def latest(self, request):
        vulns = Vulnerability.objects.all().order_by('-created_at')[:10]
        serializer = VulnerabilitySerializer(vulns, many=True)
        return Response(serializer.data)


class ProjectViewSet(ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]
    filter_fields = ('name','is_active')