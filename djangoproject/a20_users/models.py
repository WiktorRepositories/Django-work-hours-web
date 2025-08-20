from django.db import models
from django.contrib.auth.models import User
from a10_topics.models import ProjectMachines, NetzplanVorgang
from a11_informations.models import WorkTimesStandard
from mylib.timecalculations import time_to_float, time, date

# Create your models here.

#-----------------------------------------------------------------------------------------------------------
class UserSettings(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    weekSelected = models.DateField(auto_now= False, auto_now_add= False, unique= False, null= True)
    monthSelected = models.DateField(auto_now= False, auto_now_add= False, unique= False, null= True)
    
    rangeStart = models.DateField(auto_now= False, auto_now_add= False, unique= False, null= True)
    rangeEnd = models.DateField(auto_now= False, auto_now_add= False, unique= False, null= True)
    
    def __str__(self) -> str:
        return f"{self.user}"
#===========================================================================================================

#-----------------------------------------------------------------------------------------------------------
class UsersWorkTimes(models.Model):

    class Meta:
        db_table = "a20_users_usersworktimes" 
        
    user = models.ForeignKey(to= User, on_delete=models.CASCADE, null= True)

    date = models.DateField(auto_now= False, auto_now_add= False, unique= False)

    travel_start = models.TimeField(auto_now= False, auto_now_add= False, unique= False, null= True)
    travel_end = models.TimeField(auto_now= False, auto_now_add= False, unique= False, null= True)

    work_start = models.TimeField(auto_now= False, auto_now_add= False, unique= False, null= True)
    work_end = models.TimeField(auto_now= False, auto_now_add= False, unique= False, null= True)

    workimes_standard = models.ForeignKey(to= WorkTimesStandard, on_delete=models.CASCADE, null= True)

    # project_machine = models.ForeignKey(to= ProjectMachines, null= True, on_delete= models.SET_NULL)
    # netzplan_vorgang = models.ForeignKey(to= NetzplanVorgang, null= True, on_delete= models.SET_NULL)

    project_machine = models.CharField(max_length= 32, unique= False, null= True)
    netzplan_vorgang = models.CharField(max_length= 32, unique= False, null= True)

    def __str__(self):
        return f"{self.user}, {self.date}"

    def date_to_iso(self):
        if self.date:
            return self.date.isoformat()
        return ""
    
    @property
    def travelstart_to_float(self):
        return time_to_float(self.travel_start)
    
    @property
    def travelend_to_float(self):
        return time_to_float(self.travel_end)
    
    #-------------------------------------------
    
    @property
    def travelstart_to_iso(self):
        return self.travel_start.strftime("%H:%M")
    
    @property
    def travelend_to_iso(self):
        return self.travel_end.strftime("%H:%M")
    
    #----------------------------------------------
    
    @property
    def workstart_to_iso(self):
        return self.work_start.strftime("%H:%M")
    
    @property
    def workend_to_iso(self):
        return self.work_end.strftime("%H:%M")
    
    #-----------------------------------------------
    
    @property
    def traveltim_diverence_float(self):
        return time_to_float(self.travel_end) - time_to_float(self.travel_start)
    
    @property
    def worktime_diverence_float(self):
        return time_to_float(self.work_start) - time_to_float(self.work_end)
    
    @property
    def normal_time(self):
        standardtime = self.workimes_standard.workTime_float
        usertime = self.worktime_diverence_float

        return usertime if usertime <= standardtime else standardtime

    @property
    def over_time(self):
        standardtime = self.workimes_standard.workTime_float
        usertime = self.worktime_diverence_float

        return (usertime - standardtime) if usertime > standardtime else 0.0
#===========================================================================================================