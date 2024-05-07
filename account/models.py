from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.utils import timezone

# Define maximum failed login attempts and account lockout duration
MAX_FAILED_LOGIN_ATTEMPTS = 5
ACCOUNT_LOCKOUT_DURATION = timezone.timedelta(minutes=5)


class MyUserManager(BaseUserManager):
    def create_user(self, email, name, password=None, password2=None):
        """
        Creates and saves a User with the given email, name, and password.
        """
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
            name=name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password=None):
        """
        Creates and saves a superuser with the given email, name, and password.
        """
        user = self.create_user(
            email,
            password=password,
            name=name,
        )
        user.is_admin = True
        user.is_staff = True
        user.save(using=self._db)
        return user

    def create_staff(self, email, name, password=None):
        """
        Creates and saves a staff member with the given email, name, and password.
        """
        user = self.create_user(
            email=email,
            password=password,
            name=name,
        )
        user.is_staff = True
        user.is_admin = False
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    """
    Custom user model representing a user of the system.
    """

    email = models.EmailField(
        verbose_name="Email",
        max_length=255,
        unique=True,
    )
    name = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    has_account = models.BooleanField(default=False)
    has_loan=models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = MyUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        """
        Does the user have a specific permission?
        Simplest possible answer: Yes, always
        """
        return self.is_admin

    def has_module_perms(self, app_label):
        """
        Does the user have permissions to view the app `app_label`?
        Simplest possible answer: Yes, always
        """
        return True

    failed_login_attempts = models.IntegerField(default=0)
    last_failed_login = models.DateTimeField(null=True, blank=True)

    def increase_failed_login_attempts(self):
        """
        Increase the count of failed login attempts and update the timestamp of the last failed attempt.
        """
        self.failed_login_attempts += 1
        self.last_failed_login = timezone.now()
        self.save()

    def reset_failed_login_attempts(self):
        """
        Reset the count of failed login attempts and clear the timestamp of the last failed attempt.
        """
        self.failed_login_attempts = 0
        self.last_failed_login = None
        self.save()

    def is_account_locked(self):
        """
        Check if the user's account is locked due to exceeding maximum failed login attempts.
        """
        if self.failed_login_attempts >= MAX_FAILED_LOGIN_ATTEMPTS:
            if self.last_failed_login:
                lockout_time = self.last_failed_login + ACCOUNT_LOCKOUT_DURATION
                if lockout_time > timezone.now():
                    return True
                else:
                    self.reset_failed_login_attempts()
                    return False
        return False
