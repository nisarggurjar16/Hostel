from django.db import models
from django.contrib.auth.models import User


class StudentInformation(models.Model):
    user = models.OneToOneField(
        User, null=True, blank=True, related_name='Student', on_delete=models.CASCADE)
    mobile = models.CharField(max_length=13, null=True, blank=True)
    profilePicture = models.FileField(null=True, blank=True)
    joiningDate = models.DateTimeField(
        auto_now_add=True, null=True, blank=True)
    monthlyFees = models.IntegerField(default=1500, null=True, blank=True)
    percentage = models.IntegerField(null =True, blank=True)

    def __str__(self):
        return self.user.username


class Perferences(models.Model):
    user = models.OneToOneField(
        User, blank=True, null=True, on_delete=models.CASCADE, related_name="main_user")
    choice1 = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.SET_NULL, related_name="choice1")
    choice2 = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.SET_NULL, related_name="choice2")
    choice3 = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.SET_NULL, related_name="choice3")
    choice4 = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.SET_NULL, related_name="choice4")
    choice5 = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.SET_NULL, related_name="choice5")


class PaymentDetail(models.Model):
    std = models.ForeignKey(StudentInformation, blank=True, null=True, on_delete= models.CASCADE)
    pay_id = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=128, blank=True, null=True)