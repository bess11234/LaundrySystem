from django.db import models

# Create your models here.
class User(models.Model):
    MANAGER = "mgr"
    STAFF = "stf"
    CUSTOMER = "cus"
    ROLES = {CUSTOMER: "customer", STAFF: "staff", MANAGER: "manager"}
    
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=255)
    phone = models.CharField(max_length=10)
    password = models.TextField()
    role = models.CharField(choices=ROLES)
    status = models.BooleanField(default=1) # 0=suspend 1=active
    create_at = models.DateTimeField(auto_now_add = True)
    reserveMachine = models.ManyToManyField("laundry.Machine", through="Reserve_Machine")

class Service(models.Model):
    name = models.CharField(max_length=50)
    price = models.IntegerField()

class Machine_Size(models.Model):
    size = models.CharField(max_length=15)

class Machine(models.Model):
    machine_size = models.ForeignKey(Machine_Size, on_delete=models.CASCADE)
    code = models.CharField(max_length=10)
    capacity = models.IntegerField()
    cost = models.IntegerField()
    duration = models.IntegerField()
    status_available = models.IntegerField()
    status_health = models.IntegerField()
    create_at = models.DateTimeField(auto_now_add=True)

class Reserve_Machine(models.Model):
    # "waiting","workable","working","complete","retrivable"
    STATUS = {0: "waiting", 1: "workable", 2: "working", 3: "complete", 4: "retrivable"}
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE)
    machine_size = models.ForeignKey(Machine_Size, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    cost = models.IntegerField()
    arrive_at = models.DateTimeField()
    status = models.IntegerField(choices=STATUS)
    create_at = models.DateTimeField(auto_now_add=True)
    arrive_arrive = models.DateTimeField(null=True)
    work_at = models.DateTimeField(null=True)
    service = models.ManyToManyField(Service, related_name="reserve_service")

class Review_Reserve(models.Model):
    RATING = ((1,1), (2,2), (3,3), (4,4), (5,5))
    rating = models.IntegerField(choices=RATING)
    description = models.TextField()
    create_at = models.DateTimeField(auto_now_add = True)
