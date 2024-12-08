from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class User(models.Model):
    USER_TYPE_CHOICES = (
        ('admin', 'Administrator'),
        ('investigator', 'Investigator'),
        ('whistleblower', 'Whistleblower'),
    )

    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(unique=True)
    user_type = models.CharField(max_length=15, choices=USER_TYPE_CHOICES)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def _str_(self):
        return self.email

    def has_permission(self, permission):
        return self.user_type == permission


class Case(models.Model):
    STATUS_CHOICES = (
        ('reported', 'Reported'),
        ('under_investigation', 'Under Investigation'),
        ('resolved', 'Resolved'),
    )

    title = models.CharField(max_length=255)
    description = models.TextField()
    reported_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reported_cases')
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_cases')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='reported')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def _str_(self):
        return f"Case {self.title} (Status: {self.status})"


class Evidence(models.Model):
    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name='evidences')
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uploaded_evidences')
    evidence_file = models.FileField(upload_to='evidences/')
    description = models.TextField(blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return f"Evidence for {self.case.title} by {self.uploaded_by.username}"


class Feedback(models.Model):
    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name='feedbacks')
    provided_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='provided_feedback')
    feedback_text = models.TextField()
    provided_at = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return f"Feedback for case {self.case.title} by {self.provided_by.username}"