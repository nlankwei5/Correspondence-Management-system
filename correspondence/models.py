from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from datetime import date
from cloudinary.models import CloudinaryField

# Create your models here.


class Department(models.Model):

    CHOICES = [
        ('INTERNAL', 'Internal'),
        ('REGIONAL', 'Regional'),
        ('EXT_FREQUENT', 'External_Frequent'),
        ('EXTERNAL', 'External'), 
    ]
    name = models.CharField(max_length=100, blank=False)
    code = models.CharField(max_length=10, blank=False)
    type = models.CharField(max_length=15, choices=CHOICES, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    

class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifier
    for authentication instead of usernames.
    """
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        
        return self.create_user(email, username, password, **extra_fields)


class CustomUser (AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    is_active = models.BooleanField(default=True) 
    is_superuser = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return f"{self.username} ({self.email})"
    


class IncomingCorrespondence(models.Model):

    subject = models.CharField(blank=False, max_length=150)
    source = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    source_external = models.CharField(max_length=100, blank=True, null=True)
    received_date  = models.DateField(default=date.today)
    filed = models.BooleanField(default=False)
    file = CloudinaryField('file', resource_type="raw", allowed_formats=['pdf'], blank=True, null=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.subject}"



class Dispatch(models.Model):
    subject = models.CharField(blank=False, max_length=150)
    destination = models.ManyToManyField(Department)
    dispatch_date  = models.DateField(default=date.today)
    filed = models.BooleanField(default=False)
    approval = models.BooleanField(default=False)
    file = CloudinaryField('file', resource_type='raw', allowed_formats=['pdf'], blank=True, null=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL,null=True )
    
    def __str__(self):
        return f"{self.subject}"


class Letters(models.Model):
    subject = models.CharField(max_length=150, blank=False)
    reference_number = models.CharField(max_length=10)
    receipient = models.CharField(max_length=150, blank=True, null=True)
    date_sent= models.DateField(default=date.today)
    file = CloudinaryField('file', resource_type="raw", allowed_formats=['pdf'], blank=True, null=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL,null=True )

    def __str__(self):
        return f"{self.subject}"

