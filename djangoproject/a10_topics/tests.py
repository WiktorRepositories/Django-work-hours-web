import pytest
from django.test import TestCase
from django.test import Client
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
from a10_topics.models import ProjectMachines, Netzplan, Vorgang

#=============================================================================================================
# GET machines and projects overview
@pytest.mark.django_db
def test_projectmachine_overview_get(projectmachines):#{
    client = Client()
    url = reverse("machines_overview")
    response = client.get(url)

    assert response.status_code == 200
    assert response.context["machines"].count() == len(projectmachines)
    for m in projectmachines:
        assert m in response.context["machines"]
#}

@pytest.mark.parametrize("a, b, c, d", [
    ("GM5060", "02-510", "Renault line 2 OP10", 1),
    ("GM5060", "02-520", "Renault line 2 OP20", 1),
    ("GM5060", "02-550", "Renault line 2 OP30", 1),
])
@pytest.mark.django_db
def test_projectmachine_overview_post(a, b, c, d):#{
    client = Client()
    url = reverse("machines_overview")
    data = {"project" : a, "machine" : b, "description" : c}
    response = client.post(path= url, data=data)

    assert response.status_code == 302
    assert ProjectMachines.objects.get(**data)

    query_set = ProjectMachines.objects.all()
    assert query_set.count() > 0
#}

#=============================================================================================================
# GET correct data
@pytest.mark.parametrize("idx", [0,1,2,3])
@pytest.mark.django_db
def test_projectmachine_modify_get_1(projectmachines, idx):#{
    pk = projectmachines[idx].pk
    client = Client()
    url = reverse(viewname= "machine_modify", args=[pk])
    response = client.get(path= url)
    assert response.status_code == 200
#}

# GET error data
@pytest.mark.parametrize("id", [5,6,7,8])
@pytest.mark.django_db
def test_projectmachine_modify_get_2(projectmachines, id):#{
    client = Client()
    url = reverse(viewname= "machine_modify", args=[id])
    response = client.get(path= url)

    assert response.status_code == 200
    assert response.context["error"]
#}

# POST add items to data base
@pytest.mark.parametrize("a, b, c, idx", [
    ("GM5860", "03-510", "Ford line 2 OP10", 0),
    ("GM5860", "03-520", "Ford line 2 OP20", 1),
    ("GM5860", "03-550", "Ford line 2 OP30", 2),
])
@pytest.mark.django_db
def test_projectmachine_modify_post(projectmachines, a,b,c, idx):#{
    pk = projectmachines[idx].pk
    client = Client()
    url = reverse(viewname= "machine_modify", args=[pk])
    data = {"project" : a, "machine" : b, "description" : c}
    response = client.post(url, data)

    assert response.status_code == 302
    assert ProjectMachines.objects.get(**data)
    query_set = ProjectMachines.objects.all()
    assert query_set.count() > 0
#}

#=============================================================================================================

@pytest.mark.parametrize("idx", [0,1,2,3])
@pytest.mark.django_db
def test_proectmachine_delete_get(projectmachines, idx):#{
    client = Client()
    url = reverse(viewname= "machine_delete", args=[projectmachines[idx].pk])
    response = client.get(path= url)
    assert response.status_code == 200
#}

@pytest.mark.parametrize("idx", [0,1,2,3])
@pytest.mark.django_db
def test_machine_delete_post(projectmachines, idx):#{
    pk = projectmachines[idx].pk
    client = Client()
    data = {"operation" : "delete"}
    url = reverse(viewname= "machine_delete", args=[pk])
    response = client.post(path= url, data= data)

    assert response.status_code == 302
    try:
        ProjectMachines.objects.get(pk=pk)
        assert False
    except ProjectMachines.DoesNotExist:
        assert True
#}

#=============================================================================================================

@pytest.mark.django_db
def test_netzplan_overview_get(netzplan):
    client = Client()
    url = reverse(viewname= "netzplan_overview")
    response = client.get(path= url)

    assert response.status_code == 200

    assert response.context["netzplan_items"].count() > 0
    assert response.context["netzplan_items"].count() == len(netzplan)
    for i in netzplan:
        assert i in response.context["netzplan_items"]


@pytest.mark.parametrize("c, d", [
    ("4637843", "VW line 2"),
    ("4637843", "VW line 2")
])
@pytest.mark.django_db
def test_netzplan_overview_post(netzplan, c, d):
    client = Client()
    data = {"code" : c,
            "description" : d}
    url = reverse(viewname= "work_types_overview")
    response = client.post(path= url, data= data)

    assert response.status_code == 302
    assert Netzplan.objects.get(**data)

#-------------------------------------------------------------------------

@pytest.mark.django_db
def test_workdata_overview_get(workdatas, worktypes):
    client = Client()
    url = reverse(viewname= "work_datas_overview")
    response = client.get(path= url)

    assert response.status_code == 200
    
    assert response.context["workdatas"].count() > 0
    assert response.context["worktypes"].count() > 0

    assert response.context["workdatas"].count() == len(workdatas)
    assert response.context["worktypes"].count() == len(worktypes)
    for i in workdatas:
        assert i in response.context["workdatas"]

@pytest.mark.django_db
def test_workdata_overview_post1(workdatas, worktypes):
    client = Client()
    url = reverse("work_datas_overview")
    data = {"code" : "DC11",
            "text" : "DT11",
            "description" : "DD11",
            "workType_id" : "1"}
    
    response = client.post(url, data)
    assert response.status_code == 302

@pytest.mark.parametrize("c, t, d, i", [
    ("dc4", "dt4", "dd1", "1"),
    ("dc5", "dt5", "dd2", "2"),
    ("dc6", "dt6", "dd3", "3"),
    ("dc7", "dt7", "dd3", "4"),
])
@pytest.mark.django_db
def test_workdata_overview_post2(workdatas, c, t, d, i):
    client = Client()
    data = {"code" : c,
            "text" : t,
            "description" : d,
            "workType_id" : i}
    url = reverse(viewname= "work_datas_overview")
    response = client.post(path= url, data= data)
    assert response.status_code == 302

#-------------------------------------------------------------------------