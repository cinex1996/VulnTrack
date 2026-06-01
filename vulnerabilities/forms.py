from django import forms
from vulnerabilities.models import Vulnerability, Comment


class VulnerabilityForm(forms.ModelForm):
    class Meta:
        model = Vulnerability
        fields = ('title', 'description', 'severity', 'project')

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)

class StatusUpdateForm(forms.ModelForm):
    class Meta:
        model = Vulnerability
        fields = ('status',)