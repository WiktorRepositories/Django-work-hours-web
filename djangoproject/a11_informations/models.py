from django.db import models

from datetime import time
from mylib.timecalculations import time_to_float
# Create your models here.

#--------------------------------------------------------------------------------------------------------------------
# Data Base for constant waork and break time
class WorkTimesStandard(models.Model):
    # Base data types
    country = models.CharField(max_length= 8, null= False)
    description = models.CharField(max_length= 16, null= True)
    workTime = models.TimeField(auto_now= False, auto_now_add= False)
    breakTime = models.TimeField(auto_now= False, auto_now_add= False)

    # Django admin display
    def __str__(self):
        return f"{self.country}, {self.workTime_float}, {self.breakTime_float}"
    
    @property
    def work_break(self):
        return f"{self.workTime}/{self.breakTime}"

    @property
    def workTime_float(self):
        return time_to_float(self.workTime)

    @property
    def breakTime_float(self):
        return time_to_float(self.breakTime)

    @property
    def workTime_iso(self):
        return self.workTime.strftime("%H:%M")

    @property
    def breakTime_iso(self):
        return self.breakTime.strftime("%H:%M")
#====================================================================================================================

#--------------------------------------------------------------------------------------------------------------------
class MailReciever(models.Model):
    # Base data types
    short_name = models.CharField(max_length= 8, unique= False)
    email = models.CharField(max_length= 32) # obcy to User

    firstName = models.CharField(max_length= 16)
    lastName = models.CharField(max_length= 16)
    description = models.CharField(max_length= 32, null= True) 

    # Django admin display
    def __str__(self):
        return f"mail: {self.email}, {self.firstName} {self.lastName}"
#====================================================================================================================