from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **kwargs):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(email=self.normalize_email(email), **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(email=email, password=password, is_active=True, is_staff = True, is_admin=True)
        user.save(using=self._db)
        return user

class UserRole(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.role_name

class User(AbstractBaseUser):
    objects = UserManager()

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=255, unique=True)
    user_type = models.ForeignKey(UserRole, on_delete=models.SET_NULL, blank=True, null=True)
    
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

class Project(models.Model):
    name = models.CharField(max_length=100)
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, limit_choices_to={'role__role_name': "Manager"})
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{}".format(self.name)


class Task(models.Model):
    STATUS_CHOICES = (
        ("Open", "Open"),
        ("In Progress", "In Progress"),
        ("Completed", "Completed")
    )
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    task = models.TextField()
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, limit_choices_to={'role__role_name': "Employee"})
    status = models.CharField(choices=STATUS_CHOICES, max_length=50, default=STATUS_CHOICES[0][0])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)