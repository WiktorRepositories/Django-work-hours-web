from datetime import time, date

def time_to_float(t:time|None)->float:
    if t:
        fullsec = t.second + t.minute*60 + t.hour*3600
        return round((fullsec * 0.00027778) , 2)
    return 0.0

def divtime_float1(t1:time|None, t2:time|None)->float:
    if t1 and t2:
        return time_to_float(t2) - time_to_float(t1)
    return 0.0

def divtime_float2(startH= 0, startM=0, startS=0, endH=0, endM=0, endS=0)->float:
    return time_to_float(time(endH, endM, endS)) - time_to_float(time(startH, startM, startS))
#}

def isoformat_date(date_str:str)->(None | date):#{
    if date_str:
        try:
            retdate = date.fromisoformat(date_str)
        except ValueError:# Convert error
            return None
        return retdate
    return None
#}


# divtime = divtime_float1(time(8,15,0), time(17,45,0))
# print("Time diferences:", divtime)

# divtime = divtime_float2(startH=8, endH=17, endM=45)
# print("Time diferences:", divtime)

# def time_to_float(start_time, end_time):
#     if start_time and end_time:
#         delta = datetime.combine(date.min, end_time) - datetime.combine(date.min, start_time)
#         return round(delta.total_seconds() / 3600, 2)
#     return 0.0


# total_hours = UserData_db.objects.filter(
#     user=request.user, daydate__month=7
# ).aggregate(Sum('workTime'))['workTime__sum']

# data['workTime'] = time_to_float(cleaned_data['workstart'], cleaned_data['workend'])