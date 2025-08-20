import pytest
from django.contrib.contenttypes.models import ContentType
from a10_topics.models import ProjectMachines, Netzplan, Vorgang

@pytest.fixture()
def projectmachines():#{
    mylist = []
    
    a = "GM7200"
    b = "01-1010"
    c = "Ford stator 1 line, OP10"
    mylist.append(ProjectMachines.objects.create(project=a, machine=b, description=c))

    a = "GM7200"
    b = "01-1020"
    c = "Ford stator 1 line, OP20"
    mylist.append(ProjectMachines.objects.create(project=a, machine=b, description=c))

    a = "GM7200"
    b = "01-1030"
    c = "Ford stator 1 line, OP30"
    mylist.append(ProjectMachines.objects.create(project=a, machine=b, description=c))

    a = "GM7200"
    b = "01-1040"
    c = "Ford stator 1 line, OP40"
    mylist.append(ProjectMachines.objects.create(project=a, machine=b, description=c))

    return mylist
#}

@pytest.fixture()
def netzplan():#{
    mylist = []
    
    a = "4637843"
    b = "Ford OP10"
    netzplanitem = Netzplan.objects.create(number= a, description= b)
    mylist.append(netzplanitem)

    a = "4697845"
    b = "Ford OP20"
    netzplanitem = Netzplan.objects.create(number= a, description= b)
    mylist.append(netzplanitem)

    a = "4687844"
    b = "Ford OP30"
    netzplanitem = Netzplan.objects.create(number= a, description= b)
    mylist.append(netzplanitem)

    a = "4657847"
    b = "Ford OP40"
    netzplanitem = Netzplan.objects.create(number= a, description= b)
    mylist.append(netzplanitem)

    return mylist
#}

@pytest.fixture()
def vorgang(worktypes):
    mylist = []

    a = "0950"
    b = "EPLAN design"
    vorgangitem = Vorgang.objects.create(number= a, description= b)
    mylist.append(vorgangitem)

    a = "2450"
    b = "Software design"
    vorgangitem = Vorgang.objects.create(number= a, description= b)
    mylist.append(vorgangitem)

    a = "4045"
    b = "Virtual IBN"
    vorgangitem = Vorgang.objects.create(number= a, description= b)
    mylist.append(vorgangitem)

    a = "4040"
    b = "Drives parametrization"
    vorgangitem = Vorgang.objects.create(number= a, description= b)
    mylist.append(vorgangitem)

    a = "4040"
    b = "Drives parametrization"
    vorgangitem = Vorgang.objects.create(number= a, description= b)
    mylist.append(vorgangitem)

    a = "2066"
    b = "Base IBN MN"
    vorgangitem = Vorgang.objects.create(number= a, description= b)
    mylist.append(vorgangitem)

    a = "4065"
    b = "Base IBN"
    vorgangitem = Vorgang.objects.create(number= a, description= b)
    mylist.append(vorgangitem)

    a = "2067"
    b = "Drive input MN"
    vorgangitem = Vorgang.objects.create(number= a, description= b)
    mylist.append(vorgangitem)

    a = "3400"
    b = "Safety tests"
    vorgangitem = Vorgang.objects.create(number= a, description= b)
    mylist.append(vorgangitem)

    a = "4130"
    b = "Laser calibartion"
    vorgangitem = Vorgang.objects.create(number= a, description= b)
    mylist.append(vorgangitem)

    a = "4230"
    b = "IBN automatic"
    vorgangitem = Vorgang.objects.create(number= a, description= b)
    mylist.append(vorgangitem)

    a = "4260"
    b = "Quality check"
    vorgangitem = Vorgang.objects.create(number= a, description= b)
    mylist.append(vorgangitem)

    a = "4395"
    b = "Technical support"
    vorgangitem = Vorgang.objects.create(number= a, description= b)
    mylist.append(vorgangitem)

    a = "5148"
    b = "Standby"
    vorgangitem = Vorgang.objects.create(number= a, description= b)
    mylist.append(vorgangitem)

    return mylist
#}