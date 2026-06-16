from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from notifications.models import Notification


# Create your views here.
@login_required
def notification_view(request):
    no_notifications_message = "Nie ma żadnych powiadomień"
    notifications = Notification.objects.filter(recipient=request.user)
    if request.method == "GET":
        if not notifications.exists():
            return render(request, "notifications/notification.html",{'no_notifications_message':no_notifications_message})
    return render(request, "notifications/notification.html",{'notifications':notifications})

@login_required
def mark_as_read(request,pk):
    if request.method == "GET":
        return redirect("notifications")
    notification = get_object_or_404(Notification, pk=pk, recipient=request.user)
    notification.is_read = True
    notification.save()
    return redirect("notifications")

@login_required
def mark_all_as_read(request):
    if request.method == "GET":
        return redirect("notifications")
    notifications = Notification.objects.filter(recipient=request.user).update(is_read=True)
    return redirect("notifications")