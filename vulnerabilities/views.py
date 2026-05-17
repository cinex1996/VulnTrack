from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404

from .forms import VulnerabilityForm, CommentForm, StatusUpdateForm
from .models import Vulnerability, Comment, History


# Create your views here.
@login_required
def index(request):
    vulnerabilities = Vulnerability.objects.all()
    total_vulnerabilities = vulnerabilities.count()
    critical_vulnerabilities = vulnerabilities.filter(severity="critical").count()
    fixed_vulnerabilities = vulnerabilities.filter(status="fixed").count()
    open_vulnerabilities = vulnerabilities.filter(status="open").count()
    return render(request, 'vulnerabilities/index.html', {'vulnerabilities': vulnerabilities,
                                                          'total_vulnerabilities': total_vulnerabilities,
                                                          'critical_vulnerabilities': critical_vulnerabilities,
                                                          'fixed_vulnerabilities': fixed_vulnerabilities,
                                                          'open_vulnerabilities': open_vulnerabilities})


@login_required
def vulnerability_detail(request,id):
    vulnerability = get_object_or_404(Vulnerability, id=id)
    comments = vulnerability.comment_set.all()
    status_form = StatusUpdateForm(instance=vulnerability)
    is_analyst = request.user.groups.filter(name='Analyst').exists()
    history  = vulnerability.history.all().order_by('-created_at')
    is_admin = request.user.is_superuser
    if request.method == 'POST':
        if "comment_submit" in request.POST:
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.author = request.user
                comment.vulnerability = vulnerability
                comment.save()
                return redirect(vulnerability_detail, id=vulnerability.id)
        elif 'status_submit' in request.POST and is_analyst:
            old_status = vulnerability.status
            status_form = StatusUpdateForm(request.POST, instance=vulnerability)
            if status_form.is_valid():
                status_form.save()
                new_status = vulnerability.status
                if new_status != old_status:
                    History.objects.create(vulnerability=vulnerability, old_status=old_status,
                                                         new_status=new_status,changed_by=request.user)
                return HttpResponseRedirect(request.path)
    else:
        comment_form = CommentForm()

    return render(request, 'vulnerabilities/detail.html', {'vulnerability': vulnerability,
                                                           'comments': comments, 'comment_form': comment_form,
                                                           'status_form': status_form,'is_analyst':is_analyst,
                                                           'history': history,
                                                           'is_admin':is_admin})


@login_required
def create_vulnerability(request):
    if request.method == 'POST':
        form = VulnerabilityForm(request.POST)
        if form.is_valid():
            create_form = form.save(commit=False)
            create_form.reporter = request.user
            create_form.save()
            return redirect("vulnerability_detail", id=create_form.id)
    else:
        form = VulnerabilityForm()
    return render(request, 'vulnerabilities/create.html', {'form': form})


@login_required
def update_vulnerability(request,id):
    vulnerability = get_object_or_404(Vulnerability, id=id)
    if request.user != vulnerability.reporter:
        return HttpResponseForbidden("Nie masz uprawnień")
    if request.method == 'POST':
        form = VulnerabilityForm(request.POST, instance=vulnerability)
        if form.is_valid():
            form.save()
            return redirect("vulnerability_detail", id=vulnerability.id)
    else:
        form = VulnerabilityForm(instance=vulnerability)
    return render(request, 'vulnerabilities/edit.html', {'form':form,'vulnerability': vulnerability})


@login_required
def delete_vulnerability(request,id):
    vulnerability = get_object_or_404(Vulnerability, id=id)
    if not request.user.is_staff:
        return HttpResponseForbidden("Nie masz uprawnień")
    if request.method == 'POST':
        vulnerability.delete()
        return redirect("index")
    return render(request, 'vulnerabilities/delete.html', {'vulnerability': vulnerability})
