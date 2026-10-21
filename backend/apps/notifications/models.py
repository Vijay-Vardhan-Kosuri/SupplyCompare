from django.db import models
from apps.accounts.models import User

class Notification(models.Model):
    TYPE_CHOICES = (
        ('order_status', 'Purchase Order Update'),
        ('quote_expiry', 'Quotation Expiring'),
        ('low_stock', 'Low Stock Warning'),
        ('system', 'System Information'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=200)
    message = models.TextField()
    notification_type = models.CharField(max_length=30, choices=TYPE_CHOICES, default='system', db_index=True)
    is_read = models.BooleanField(default=False, db_index=True)
    link_url = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        db_table = 'notifications'
        verbose_name = 'Notification'
        verbose_name_plural = 'Notifications'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.email} - {self.title} ({'Read' if self.is_read else 'Unread'})"
