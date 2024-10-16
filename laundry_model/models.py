from django.db import models
from django.db.models import Sum
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import BaseUserManager
from django.utils.timezone import timedelta

# Create your models here.
# จัดการ การ registor ให้ username ตาม email
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

# Overide class User ที่ Django มีให้
# extend มาจากสิ่งที่ django มีให้ 
# override เมื่อชื่อ field ใน django เหมือนกัน
class Users(AbstractUser):
    MANAGER = "mgr"
    STAFF = "stf"
    CUSTOMER = "cus"
    ROLES = {CUSTOMER: "customer", STAFF: "staff", MANAGER: "manager"}
    
    username = models.CharField(max_length=50, blank=True, null=True, unique=False) # ของ AbstractUser blank != null
    
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=255, unique=True)
    phone = models.CharField(max_length=10)
    
    password = models.TextField()
    role = models.CharField(choices=ROLES, default=CUSTOMER) # เพิ่ม attribute
    status = models.BooleanField(default=1) # 0=suspend 1=active
    create_at = models.DateTimeField(auto_now_add = True)
    reserveMachine = models.ManyToManyField("laundry_model.Machine", through="Reserve_Machine")# overide
    
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    
    def get_full_name(self):
        return "%s %s"%(self.first_name, self.last_name)
    
    def display_role(self):
        return self.ROLES[self.role]

class Service(models.Model):
    name = models.CharField(max_length=50)
    price = models.IntegerField()
    
    def __str__(self):
        return "%s +%d"%(self.name, self.price)
    
    def display_name(self):
        return self.name

class Machine_Size(models.Model):
    size = models.CharField(max_length=15)
    cost = models.IntegerField()
    capacity = models.IntegerField()

    def __str__(self):
        show = f"{self.capacity}kg ({self.size})"
        return show

class Machine(models.Model):
    machine_size = models.ForeignKey(Machine_Size, null=True, on_delete=models.SET_NULL)
    code = models.CharField(max_length=10, unique=True)
    duration = models.IntegerField()
    status_available = models.BooleanField(default=1)
    status_health = models.BooleanField(default=1)
    create_at = models.DateTimeField(auto_now_add=True)

    def usage_count(self):
        return Reserve_Machine.objects.filter(machine=self, status=3).count()
    
    # นำไปใช้แสดงรายได้ในหน้า Machine
    def revenue(self):
        result = Reserve_Machine.objects.filter(machine=self, status=3).aggregate(totol_cost=Sum("cost"))
        return result['totol_cost'] if result['totol_cost'] is not None else 0

class Reserve_Machine(models.Model):
    # "waiting","workable","working","complete","retrivable"
    STATUS = {0: "waiting", 1: "workable", 2: "working", 3: "complete", 4: "cancel"}
    
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    machine = models.ForeignKey(Machine, null=True, on_delete=models.SET_NULL)
    machine_size = models.ForeignKey(Machine_Size, null=True, on_delete=models.SET_NULL)
    code = models.CharField(max_length=6)
    cost = models.IntegerField()
    arrive_at = models.DateTimeField()
    status = models.IntegerField(choices=STATUS, default=0)
    create_at = models.DateTimeField(auto_now_add=True)
    actual_arrive = models.DateTimeField(null=True)
    work_at = models.DateTimeField(null=True)
    service = models.ManyToManyField(Service, related_name="reserve_service")

    def status_context(self):
        return self.STATUS[self.status]
    
    def working_til(self):
        return self.work_at + timedelta(minutes=self.machine.duration)

class Review_Reserve(models.Model):
    RATING = ((1,1), (2,2), (3,3), (4,4), (5,5))
    reserve = models.OneToOneField(Reserve_Machine, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=RATING)
    description = models.TextField(null=True, blank=True)
    create_at = models.DateTimeField(auto_now_add = True)