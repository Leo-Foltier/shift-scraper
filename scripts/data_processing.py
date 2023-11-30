from datetime import date, datetime, timedelta

import yaml

def get_weeks_to_run(settings): #Finds all week begginnings between last run and current day inculding current weekbeginning and returns them as a list as well as todays date as a string

    last_run_date = datetime.strptime(str(settings['last_run_date']), '%Y-%m-%d').date()
    todays_date = date.today()

    last_run_week_beginning = last_run_date - timedelta(days=last_run_date.weekday())
    current_week_beginning = todays_date - timedelta(days=todays_date.weekday())

    weeks_to_run = []
    while last_run_week_beginning <= current_week_beginning:

        weeks_to_run.append(last_run_week_beginning.strftime('%Y-%m-%d'))
        last_run_week_beginning += timedelta(days=7)

    update_last_run_date(todays_date.strftime('%Y-%m-%d'),settings)

    return(weeks_to_run)

def update_last_run_date(todays_date,settings): #Update last day since run in config to todays dates

    settings['last_run_date'] = todays_date

    with open('config.yml', 'w') as file:
        yaml.dump(settings, file, default_flow_style=False)

def process_schedule(rolelist, startendtimes, hoursworked): #Returns the start and end times for each role worked that day

    w_start_list, w_end_list, sm_start_list, sm_end_list, w_hours, sm_hours = [], [], [], [], 0, 0
    
    times = [jointimes.replace(" ", "").replace("\n", "").replace("-", " ").split() for jointimes in startendtimes]
    
    count = 0
    for count, role in enumerate(rolelist):

        if role == 'W':

            w_start_list.append(times[count][0])
            w_end_list.append(times[count][1])
            w_hours += float(hoursworked[count])

        elif role == 'SM':

            sm_start_list.append(times[count][0])
            sm_end_list.append(times[count][1])
            sm_hours += float(hoursworked[count])

    w_start = ",".join(w_start_list)
    w_end = ",".join(w_end_list)
    sm_start = ",".join(sm_start_list)
    sm_end = ",".join(sm_end_list)
    
    return(w_start, w_end, sm_start, sm_end, w_hours, sm_hours)