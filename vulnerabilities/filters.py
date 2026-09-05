import django_filters
from .models import Vulnerability

class VulnerabilityFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains')
    severity = django_filters.ChoiceFilter(choices=Vulnerability.Severity.choices)
    status = django_filters.ChoiceFilter(choices=Vulnerability.Status.choices)

    class Meta:
        model = Vulnerability
        fields = ['title', 'severity', 'status']