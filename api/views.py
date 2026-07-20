from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from projects.models import Project
from vulnerabilities.models import Vulnerability
from .serializers import VulnerabilitySerializer, ProjectSerializer


class VulnerabilityViewSet(ModelViewSet):
    queryset = Vulnerability.objects.all()
    serializer_class = VulnerabilitySerializer
    @action(detail=False,methods=['get'])
    def latest(self, request):
        vulns = Vulnerability.objects.all().order_by('-created_at')[:10]
        serializer = VulnerabilitySerializer(vulns, many=True)
        return Response(serializer.data)


class ProjectViewSet(ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    filter_fields = ('name','is_active')