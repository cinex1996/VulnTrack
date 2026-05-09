from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404

from .forms import VulnerabilityForm, CommentForm, StatusUpdateForm
from .models import Vulnerability, Comment


# Create your views here.
@login_required
def index(request):
    vulnerabilities = Vulnerability.objects.all()
    return render(request, 'vulnerabilities/index.html', {'vulnerabilities': vulnerabilities})


@login_required
def vulnerability_detail(request, id):
    vulnerability = get_object_or_404(Vulnerability, id=id)
    comments = vulnerability.comment_set.all()
    status_form = StatusUpdateForm(instance=vulnerability)
    comment_form = CommentForm(request.POST)
    if request.method == 'POST':
        if "comment_submit" in request.POST:
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.author = request.user
                comment.vulnerability = vulnerability
                comment.save()
                return redirect(vulnerability_detail, id=vulnerability.id)
        if status_form.is_valid():
            status_form.save()
            return HttpResponseRedirect(request.path)
    else:
        comment_form = CommentForm()

    return render(request, 'vulnerabilities/detail.html', {'vulnerability': vulnerability,
                                                           'comments': comments, 'comment_form': comment_form,
                                                           'status_form': status_form})


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
    if request.user != vulnerability.reporter:
        return HttpResponseForbidden("Nie masz uprawnień")
    if request.method == 'POST':
        vulnerability.delete()
        return redirect("index")
    return render(request, 'vulnerabilities/delete.html', {'vulnerability': vulnerability})



