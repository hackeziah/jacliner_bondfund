from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
import uuid
from datetime import datetime



class MyAccountManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):  # Create user method

        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('Users must have a username')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            # is_user=1
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password, **extra_fields):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            username=username,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.is_user = True
        user.save(using=self._db)
        return user


# ramdom = uuid.uuid4().hex[:6].upper()


class UserAccount(AbstractBaseUser):
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    username = models.CharField(max_length=30, unique=True)
    date_joined = models.DateTimeField(
        verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_user = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = MyAccountManager()

    # For checking permissions. to keep it simple all admin have ALL permissons
    def has_perm(self, perm, obj=None):
        return self.is_admin

    # Does this user have permission to view this app? (ALWAYS YES FOR SIMPLICITY)
    def has_module_perms(self, app_label):
        return True

    # def __str__(self):
    #     return self.email


class Company(models.Model):
    company_name = models.CharField(
        verbose_name="Company Name", max_length=50)
    description = models.CharField(
        verbose_name="Company Description", max_length=50, default="")
    trash = models.BooleanField(verbose_name="Trash", default=0)


    def __str__(self):
        return self.company_name


class Position(models.Model):
    position_name = models.CharField(
        verbose_name="Position Name", max_length=50)
    description = models.CharField(
        verbose_name="Position Description", max_length=50, default="")
    trash = models.BooleanField(verbose_name="Trash", default=0)

    def __str__(self):
        return self.position_name


class UserInfo(models.Model):
    emp_no = models.CharField(
        verbose_name="Employee No", max_length=200, blank=False, unique=True)

    user = models.OneToOneField(
        UserAccount,
        on_delete=models.CASCADE,
        verbose_name="User",
    )
    first_name = models.CharField(
        verbose_name="First Name", max_length=40, blank=False)
    last_name = models.CharField(
        verbose_name="Last Name", max_length=40, blank=False)
    mobile_number = models.CharField(max_length=10, blank=True)
    company_name = models.ForeignKey(
        Company, on_delete=models.CASCADE)
    position_name = models.ForeignKey(
        Position, on_delete=models.CASCADE)
    status = models.IntegerField(
        verbose_name="Status", default="")
    trash = models.BooleanField(verbose_name="Trash", default=False)
    date_created = models.DateTimeField()
    date_modified = models.DateTimeField()

    def save(self):
        if self.date_created == None:
            self.date_created = datetime.now()
            self.date_modified = datetime.now()
            super(UserInfo, self).save()

    def __str__(self):
        return self.emp_no
