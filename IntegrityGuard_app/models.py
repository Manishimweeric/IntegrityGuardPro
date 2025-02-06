from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class User(models.Model):
    USER_TYPE_CHOICES = (
        ('admin', 'Administrator'),
        ('investigator', 'Investigator'),
        ('reporter', 'Reporter'),
    )

    fullname = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)    
    email = models.EmailField(unique=True)    
    password = models.CharField(max_length=128)    
    user_type = models.CharField(max_length=15, choices=USER_TYPE_CHOICES , default='reporter')
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
    Legal_assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='Legal_cases')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='reported')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    reported = models.TextField(max_length=255, blank=True, null=True)

    def _str_(self):
        return f"Case {self.title} (Status: {self.status})"

class Feedback(models.Model):
    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name='feedbacks')
    provided_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='provided_feedback')
    reported_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='feedbacks')
    feedback_message = models.TextField(max_length=255, blank=True, null=True)
    feedback_file = models.FileField(upload_to='feedback_files/',blank=True, null=True)
    provided_at = models.DateTimeField(auto_now_add=True)    
    def __str__(self):
        return f"Feedback for Case {self.case.id} by {self.uploaded_by.username}"
    

class Evidence(models.Model):
    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name='evidence')
    provided_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='provided_evidence')
    reported_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='evidence')
    feedback_file = models.FileField(upload_to='Evidence_files/',blank=True, null=True)
    provided_at = models.DateTimeField(auto_now_add=True)    
    def __str__(self):
        return f"Feedback for Case {self.case.id} by {self.uploaded_by.username}"
    

class Collabration (models.Model):
    Reciever_email = models.CharField(max_length=100,null=False, blank=True)
    message = models.TextField(max_length=100,null=False, blank=True)
    sender_email = models.CharField(max_length=100)
    user = models.ForeignKey(User,on_delete=models.CASCADE, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class ContactMessage(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name} - {self.email}"    