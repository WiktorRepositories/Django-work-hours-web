from collections import namedtuple
from django.db import models

# Create your models here.

#-----------------------------------------------------------
# Data Base Model for machine data
class ProjectMachines(models.Model):
    project = models.CharField(max_length= 16, null= True)
    machine = models.CharField(max_length= 16, null= True)
    description = models.CharField(max_length= 64, null= True)

    def __str__(self) -> str:
        return f"{self.project}/{self.machine}"
    
    @property
    def project_machine(self):
        return f"{self.project}{self.machine}"

# machineData_t = namedtuple("machineData_t", ["code", "text", "description"])
# machineData = machineData_t("code", "text", "description")
#===========================================================

#****************************************************************************************************************
#-------------------------------------------------------------------
# Sub Data Base Model for work type category 
class Netzplan(models.Model):
    # Base work types data
    number = models.CharField(max_length= 16)
    description = models.CharField(max_length= 64, null= True)

    def __str__(self) -> str:
        return f"{self.number}: {self.description}"

# workTypes_t = namedtuple("workTypes_t", ["code", "description"])
# workTypes = workTypes_t("code", "description")
#===================================================================

#****************************************************************************************************************
#-------------------------------------------------------------------
# Sub Data Base Model for work type category 
class Vorgang(models.Model):
    # Base work types data
    number = models.CharField(max_length= 16)
    description = models.CharField(max_length= 64, null= True)

    def __str__(self) -> str:
        return f"{self.number}: {self.description}"

# workTypes_t = namedtuple("workTypes_t", ["code", "description"])
# workTypes = workTypes_t("code", "description")
#===================================================================

#-------------------------------------------------------------------
# Data Base Model for work type descriprion 
# Data for users
class NetzplanVorgang(models.Model):
    # External data pointers
    netzplan = models.ForeignKey(to= Netzplan, null= True, on_delete= models.SET_NULL)
    vorgang = models.ForeignKey(to= Vorgang, null= True, on_delete= models.SET_NULL)
    # Descriptions 
    description = models.CharField(max_length= 64, null= True)

    def __str__(self) -> str:
        netz = self.netzplan.number
        vorg = self.vorgang.number
        dsc = self.netzplan.description + ", " + self.vorgang.description
        return f"{netz} / {vorg} | {dsc}"

# workData_t = namedtuple("workData_t", ["code", "text", "description", "workType_id"])
# workData = workData_t("code", "text", "description", "workType_id")
#===================================================================
#****************************************************************************************************************