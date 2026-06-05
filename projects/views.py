from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect

from projects.forms import ProjectForm
from projects.models import Project
from vulnerabilities.models import Vulnerability


@login_required
def project_list(request):
    project_list = Project.objects.all()
    return render(request, 'projects/list.html', {'project_list': project_list})

@login_required
def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    vulnerability_set = project.vulnerability_set.all()
    return render(request, 'projects/detail.html', {'project':project,
                                                    'vulnerability_set': vulnerability_set})

# Create your views here.
@login_required
def project_create(request):
    if not request.user.is_staff:
        return HttpResponseForbidden("Nie masz uprawnień")
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            create_form = form.save(commit=False)

            create_form.save()
            return redirect("project_list")
    else:
        form = ProjectForm()
    return render(request, 'projects/create.html', {'form': form})

@login_required
def project_update(request, pk):
    if not request.user.is_staff:
        return HttpResponseForbidden("Nie masz uprawnień")
    project = get_object_or_404(Project, pk=pk)
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect("project_list")
    else:
        form = ProjectForm(instance=project)
    return render(request, 'projects/update.html', {'form': form})

@login_required
def project_delete(request, pk):
    if not request.user.is_staff:
        return HttpResponseForbidden("Nie masz uprawnień")
    project = get_object_or_404(Project, pk=pk)
    if request.method == 'POST':
        project.delete()
        return redirect("project_list")
    else:
        return render(request, 'projects/delete.html', {'project': project})