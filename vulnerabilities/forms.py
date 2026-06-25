from django import forms
from vulnerabilities.models import Vulnerability, Comment


class _BootstrapStyledForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if isinstance(field.widget, forms.Select):
                field.widget.attrs.update({'class': 'form-select'})
            else:
                field.widget.attrs.update({'class': 'form-control'})


class VulnerabilityForm(_BootstrapStyledForm):
    class Meta:
        model = Vulnerability
        fields = ('title', 'description', 'severity', 'project',)

class CommentForm(_BootstrapStyledForm):
    class Meta:
        model = Comment
        fields = ('content',)

class StatusUpdateForm(_BootstrapStyledForm):
    class Meta:
        model = Vulnerability
        fields = ('status',)
