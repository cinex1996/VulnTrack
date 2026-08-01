from django.contrib.auth import get_user_model
from rest_framework import serializers, viewsets, generics

from projects.models import Project
from vulnerabilities.models import Vulnerability


class VulnerabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Vulnerability
        fields = ["status","severity","description","reporter","created_at","updated_at","project","title"]
        read_only_fields = ["reporter","created_at","updated_at"]


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ["name", "description","created_at","is_active"]


