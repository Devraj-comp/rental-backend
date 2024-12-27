from django.urls import path
from .views import *

urlpatterns = [
    path('notifications/create/', NotificationCreateView.as_view(), name='notifications-create'),
    path('notifications/', NotificationListView.as_view(), name='notifications'),
    path('notifications/curent/', CurrentUserNotificationListView.as_view(), name='notifications-current'),
    path('notifications/<int:pk>/', NotificationListView.as_view(), name='notifications-mark'),
    path('notifications/<int:notification_id>/read', MarkNotificationAsReadView.as_view(), name='notification-mark'),
]