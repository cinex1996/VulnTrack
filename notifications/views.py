from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from notifications.models import Notification


@login_required
def notification_view(request):
    notifications = Notification.objects.filter(recipient=request.user)
    return render(request, "notifications/notification.html", {'notifications': notifications})


@login_required
def mark_as_read(request, pk):
    notification = get_object_or_404(Notification, pk=pk, recipient=request.user)
    notification.is_read = True
    notification.save()
    if notification.url:
        return redirect(notification.url)
    return redirect('notifications')
