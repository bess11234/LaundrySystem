from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


# Create your models here.
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)

class Users(AbstractUser):
    MANAGER = "mgr"
    STAFF = "stf"
    CUSTOMER = "cus"
    ROLES = {CUSTOMER: "customer", STAFF: "staff", MANAGER: "manager"}
    
    # username = models.CharField(max_length=50, blank=True, null=True, unique=False) # ของ AbstractUser
    
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=255, unique=True)
    phone = models.CharField(max_length=10)
    
    password = models.TextField()
    role = models.CharField(choices=ROLES, default=CUSTOMER)
    status = models.BooleanField(default=1) # 0=suspend 1=active
    create_at = models.DateTimeField(auto_now_add = True)
    reserveMachine = models.ManyToManyField("laundry_model.Machine", through="Reserve_Machine")
    
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    
    def display_role(self):
        return self.ROLES[self.role]

class Service(models.Model):
    name = models.CharField(max_length=50)
    price = models.IntegerField()

class Machine_Size(models.Model):
    size = models.CharField(max_length=15)
    capacity = models.IntegerField()

class Machine(models.Model):
    machine_size = models.ForeignKey(Machine_Size, null=True, on_delete=models.SET_NULL)
    code = models.CharField(max_length=10)
    cost = models.IntegerField()
    duration = models.IntegerField()
    status_available = models.IntegerField(default=1)
    status_health = models.IntegerField(default=1)
    create_at = models.DateTimeField(auto_now_add=True)

class Reserve_Machine(models.Model):
    # "waiting","workable","working","complete","retrivable"
    STATUS = {0: "waiting", 1: "workable", 2: "working", 3: "complete", 4: "retrivable"}
    
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE)
    machine_size = models.ForeignKey(Machine_Size, null=True, on_delete=models.SET_NULL)
    code = models.CharField(max_length=6)
    cost = models.IntegerField()
    arrive_at = models.DateTimeField()
    status = models.IntegerField(choices=STATUS, default=0)
    create_at = models.DateTimeField(auto_now_add=True)
    arrive_arrive = models.DateTimeField(null=True)
    work_at = models.DateTimeField(null=True)
    service = models.ManyToManyField(Service, related_name="reserve_service")

class Review_Reserve(models.Model):
    RATING = ((1,1), (2,2), (3,3), (4,4), (5,5))
    rating = models.IntegerField(choices=RATING)
    description = models.TextField(null=True, blank=True)
    create_at = models.DateTimeField(auto_now_add = True)