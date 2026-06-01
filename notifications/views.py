from django.shortcuts import render, redirect

from notifications.models import Notification


# Create your views here.
def notification_view(request):
    no_notifications_message = "Nie ma żadnych powiadomień"
    notifications = Notification.objects.all()
    if request.method == "GET":
        if not notifications.exists():
            return render(request, "notifications/notification.html",{'no_notifications_message':no_notifications_message})
    return render(request, "notifications/notification.html",{'notifications':notifications})

def mark_as_read(request,pk):
    no_notifications_message = "Nie istnieje takie powiadomienie"
    try:
        notification = Notification.objects.get(pk=pk)
        notification.is_read = True
        notification.save()
    except Notification.DoesNotExist:
        return render(request, "notifications/notification.html",{'notification':no_notifications_message})
    return render(request, "notifications/notification.html")