from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.
class MyAccountManager(BaseUserManager):
    def create_user(self, first_name, last_name, username, email, password=None):
        if not email:
            raise ValueError('User must have an email address')
        if not username:
            raise ValueError('User must have a username')
        
        user = self.model(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, first_name, last_name, username, email, password):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user
    
# Creating Account
class Account(AbstractBaseUser):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    mobile_number = models.CharField(
        max_length=10,
        unique=True,
        null=True,
        blank=True,
        validators=[
            RegexValidator(
                regex=r'^[6-9]\d{9}$',
                message="Enter a valid 10-digit mobile number"
            )
        ]
    )
    date_joined = models.DateTimeField(auto_now_add=True)
    last_logined = models.DateTimeField(auto_now_add=True)

    # Required fields
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    objects = MyAccountManager()

    def __str__(self):
        return self.email
    
    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    def has_module_perms(self, add_label):
        return True
    
    def full_name(self):
        return f'{self.first_name} {self.last_name}'
    
    def formatted_mobile(self):
        if self.mobile_number:
            num = self.mobile_number[-10:]  # last 10 digits
            return f"+91 {num[:5]} {num[5:]}"
        return ""
    
class UserProfile(models.Model):
    user = models.OneToOneField(Account, on_delete=models.CASCADE)
    profile_picture = models.ImageField(blank=True, upload_to='user_profile/')
    address_line_1 = models.CharField(blank=True, max_length=150)
    address_line_2 = models.CharField(blank=True, max_length=150)
    country = models.CharField(blank=True, max_length=50)
    state = models.CharField(blank=True, max_length=50)
    city = models.CharField(blank=True, max_length=50)
    pincode = models.CharField(
        max_length=6,
        validators=[RegexValidator(r'^\d{6}$', message="Enter a valid 6-digit PIN code")],
        help_text="Enter 6 digit PIN code"
    )

    def __str__(self):
        return self.user.full_name()