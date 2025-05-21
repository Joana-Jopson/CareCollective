from django.db import models
from django.utils.timezone import now
from django.utils import timezone

class State_Model(models.Model):
    State_Id = models.AutoField(primary_key=True)  # Use AutoField for auto-incrementing
    State_Name = models.CharField(max_length=100)
    class Meta:
        db_table = "states_of_india"

class Users_Model(models.Model):
    UID = models.AutoField(primary_key=True)  # Use AutoField for auto-incrementing
    Name = models.CharField(max_length=100)
    Mobile_Number = models.CharField(max_length=10)  # Use CharField for phone numbers
    Email_Id = models.EmailField(max_length=100)    # Use EmailField for email
    Date_Of_Join = models.DateField(default=now)
    #Address = models.CharField(max_length=100)
    State_Id=models.ForeignKey(State_Model, on_delete=models.RESTRICT,db_column='State_Id')
    Admin_Flag = models.CharField(max_length=20,default="False")  # Use BooleanField for flags
    Status = models.CharField(max_length=10, default="Active")

    class Meta:
        db_table = "users"

class Login_Model(models.Model):
    Login_ID = models.AutoField(primary_key=True)  # Use AutoField for auto-incrementing
    UID = models.ForeignKey(Users_Model, on_delete=models.CASCADE,db_column='UID')  # ForeignKey with cascade delete
    Username = models.CharField(max_length=100, unique=True)  # Ensure uniqueness
    Password = models.CharField(max_length=100)

    class Meta:
        db_table = "login"
        
        
        
class Donor_Model(models.Model):
    Donor_Id = models.AutoField(primary_key=True)
    UID = models.ForeignKey(Users_Model, on_delete=models.CASCADE,db_column='UID')  # ForeignKey with cascade delete
    Donation_History_Count = models.IntegerField(default=0) 
    Verified_Date  = models.DateField(default=now)
    Last_Donation_Date = models.DateField(null=True, blank=True)
    Preferred_Donation_Categories= models.CharField(max_length=200, default='None')

    class Meta:
        db_table = "donor"
        

class Admin_Model(models.Model):
    Admin_Id = models.AutoField(primary_key=True)
    UID = models.ForeignKey(Users_Model, on_delete=models.CASCADE,db_column='UID')  # ForeignKey with cascade delete
    Role = models.CharField(max_length=50) 
    Last_Logged_In  = models.DateField(default=now)
    Last_Activity = models.CharField(max_length=200)

    class Meta:
        db_table = "admin"



class Category_Model(models.Model):
    Category_Id = models.AutoField(primary_key=True)
    Admin_Id = models.ForeignKey(Admin_Model, on_delete=models.CASCADE,db_column='Admin_Id')  
    Donor_Id=models.ForeignKey(Donor_Model, on_delete=models.CASCADE,db_column='Donor_Id')
    Category_Name = models.CharField(max_length=100) 
    Category_Description  = models.CharField(max_length=100)
    Date_Created = models.DateField()
    Status= models.CharField(max_length=50)

    class Meta:
        db_table = "category"
        
        
class Item_Model(models.Model):
    Item_Id = models.AutoField(primary_key=True)
    Category_Id = models.ForeignKey(Category_Model, on_delete=models.CASCADE,db_column='Category_Id')  
    Donor_Id=models.ForeignKey(Donor_Model, on_delete=models.CASCADE,db_column='Donor_Id')
    Item_Name = models.CharField(max_length=100) 
    Item_Description  = models.CharField(max_length=300)
    Quantity=models.IntegerField(default=1)
    Expiry_Date = models.DateField(null=True, blank=True)
    Image1 = models.ImageField(upload_to='images/', null=True, blank=True)  # Change to ImageField
    Image2 = models.ImageField(upload_to='images/', null=True, blank=True)
    Image3 = models.ImageField(upload_to='images/', null=True, blank=True)
    Status= models.CharField(max_length=50)

    class Meta:
        db_table = "item"
        
        
class Request_Model(models.Model):
    Request_Id = models.AutoField(primary_key=True)
    UID = models.ForeignKey(Users_Model, on_delete=models.CASCADE,db_column='UID')  
    Donor_Id=models.ForeignKey(Donor_Model, on_delete=models.CASCADE,db_column='Donor_Id')
    Item_Id =models.ForeignKey(Item_Model, on_delete=models.CASCADE,db_column='Item_Id')
    Quantity=models.IntegerField(default=1)
    Request_Date = models.DateField()
    Urgency=models.CharField(max_length=100) 
    Reason=models.CharField(max_length=100) 
    Status= models.CharField(max_length=50)

    class Meta:
        db_table = "request"
        

class Maps_Model(models.Model):
    Map_Id = models.AutoField(primary_key=True)
    State_Id = models.ForeignKey(State_Model, on_delete=models.CASCADE, db_column='State_Id')  # Foreign key to state
    City = models.CharField(max_length=100)  # City or Area
    Latitude = models.FloatField()  # Latitude for map
    Longitude = models.FloatField()  # Longitude for map
    Map_URL = models.URLField(max_length=500, null=True, blank=True)  # Optional map URL
    Created_Date = models.DateField(default=now)

    class Meta:
        db_table = "location_maps"

class Chat_Model(models.Model):
    Message_Id = models.AutoField(primary_key=True)
    UID = models.ForeignKey(Users_Model, on_delete=models.RESTRICT,db_column='UID')  
    Donor_Id=models.ForeignKey(Donor_Model, on_delete=models.RESTRICT,db_column='Donor_Id')
    Content = models.CharField(max_length=100) 
    Sent_By=models.IntegerField()
    Message_Date = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "chat_messages"

class Comments_Model(models.Model):
    Comment_Id = models.AutoField(primary_key=True)
    UID = models.ForeignKey(Users_Model, on_delete=models.RESTRICT,db_column='UID')  
    Donor_Id=models.ForeignKey(Donor_Model, on_delete=models.RESTRICT,db_column='Donor_Id')
    Comment = models.CharField(max_length=100) 
    Comment_Date = models.DateTimeField(default=timezone.now)
    Status=models.CharField(max_length=50) 

    class Meta:
        db_table = "user_comments"