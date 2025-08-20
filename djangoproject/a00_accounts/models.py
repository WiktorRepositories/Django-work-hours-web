from django.db import models

from django.contrib.auth.models import User
from a10_topics.models import ProjectMachines

#---------------------------------------------------------------------------------------------
# Custom dislay of user
def user_str_display(self):
    return f"{self.first_name} {self.last_name}"
User.__str__ = user_str_display
#==============================================================================================

#---------------------------------------------------------------------------------------------
#
class Cooperation(models.Model):
    description = models.CharField(max_length= 32, null= True, unique= False)
    
    users = models.ManyToManyField(to= User)
    projects = models.ManyToManyField(to= ProjectMachines)

    def __str__(self) -> str:
        str1 = ", ".join([str(i) for i in self.users.all()])
        str2 = ", ".join([str(i) for i in self.projects.all()])
        return f"{str1} | {str2} | {self.description}"
    
    @property
    def get_users(self):
        return self.users.all()
    
    @property
    def get_projects(self):
        return self.projects.all()
#==============================================================================================