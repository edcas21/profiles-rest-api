from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager

class UserProfileManager(BaseUserManager):
    """Manages the creation of users"""

    def create_user(self, email, name, password=None):
        """Create a new user profile"""   
        if not email:
            raise ValueError('User must have an email address')
        """Normalize the email address - lowercases the domain of the email"""
        email = self.normalize_email(email)
        user = self.model(email=email, name=name)

        """This sets the password and hashes it"""
        user.set_password(password)
        """Saves the new user to the db"""
        user.save(using=self.db)

        """Returns the new user object"""
        return user
    
    def create_superuser(self, email, name, password):
        """Create and save a new superuser with given details"""
        user = self.create_user(email, name, password)

        user.is_superuser = True
        user.is_staff = True
        user.save(using=self.db)

        return user

# Create your models here.
class UserProfile(AbstractBaseUser, PermissionsMixin):
    """Database model for a user in the system"""
    
    """Columns in the user table"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    """Django needs to have a custom model manager for the user model. Needs to be able to create users and control users using the Django CLI tools"""
    objects = UserProfileManager() # Must be objects

    USERNAME_FIELD ='email'
    REQUIRED_FIELDS=['name']

    def get_full_name(self):
        """Retrieve full name of user"""
        return self.name
    
    def get_short_name(self):
        """Retrieve short name of the user"""
        return self.name
    
    def __str__(self):
        """Return string representation of our user"""
        return self.email
    


