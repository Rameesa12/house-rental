from django.db import models

# Create your models here.
class login_tb(models.Model):
    username=models.CharField(max_length=200)
    password=models.CharField(max_length=200)
    usertype=models.CharField(max_length=400)

class houseowners_tb(models.Model):
    name=models.CharField(max_length=250)
    place=models.CharField(max_length=200)
    pin=models.CharField(max_length=200)
    post=models.CharField(max_length=200)
    email=models.CharField(max_length=250)
    phone=models.CharField(max_length=250)
    proof=models.CharField(max_length=250)
    LOGIN=models.ForeignKey(login_tb,default=1,on_delete=models.CASCADE)


class customers_tb(models.Model):
    name=models.CharField(max_length=250)
    place=models.CharField(max_length=200)
    pin=models.CharField(max_length=200)
    post=models.CharField(max_length=200)
    age=models.CharField(max_length=200)
    image=models.CharField(max_length=300)
    proof=models.CharField(max_length=500)
    email=models.CharField(max_length=250)
    phone=models.CharField(max_length=250)
    latitude=models.CharField(max_length=400)
    longitude=models.CharField(max_length=400)
    LOGIN=models.ForeignKey(login_tb,default=1,on_delete=models.CASCADE)


class housedetail_tb(models.Model):
    latitude=models.CharField(max_length=400)
    longitude=models.CharField(max_length=400)
    rent=models.CharField(max_length=400)
    OWNER=models.ForeignKey(houseowners_tb,default=1,on_delete=models.CASCADE)
    image1=models.CharField(max_length=300)
    image2=models.CharField(max_length=300)
    image3=models.CharField(max_length=300)
    information=models.CharField(max_length=400)
    type=models.CharField(max_length=200)

class rating_tb(models.Model):
    rating=models.CharField(max_length=200)
    date=models.CharField(max_length=200)
    CUSTOMER=models.ForeignKey(customers_tb,default=1,on_delete=models.CASCADE)
    HOUSE_DETAILS=models.ForeignKey(housedetail_tb,default=1,on_delete=models.CASCADE)

class booking_tb(models.Model):
    date=models.CharField(max_length=200)
    CUSTOMER=models.ForeignKey(customers_tb,default=1,on_delete=models.CASCADE)
    status=models.CharField(max_length=200)
    ROOM=models.ForeignKey(housedetail_tb,default=1,on_delete=models.CASCADE)
    payment_status=models.CharField(max_length=400)
    payment_date=models.CharField(max_length=400)
    payment_mode=models.CharField(max_length=400)
    amount=models.CharField(max_length=400)


class chat_tb(models.Model):
    chat=models.CharField(max_length=600)
    date=models.CharField(max_length=200)
    CUSTOMER=models.ForeignKey(customers_tb,default=1,on_delete=models.CASCADE)
    OWNER=models.ForeignKey(houseowners_tb,default=1,on_delete=models.CASCADE)
    type=models.CharField(max_length=200)
