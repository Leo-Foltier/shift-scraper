import yaml

import scripts.data_processing as data_processing
import scripts.database_scripts as database_scripts
import scripts.web_data as web_data

with open('config.yml', 'r') as file:
    settings = yaml.safe_load(file)

days_of_week = [('Mon',2),('Tue',3),('Wed',4),('Thu',5),('Fri',6),('Sat',7),('Sun',8)]

weeks_to_run = data_processing.get_weeks_to_run(settings)
client = web_data.login(settings)

for week_beginning in weeks_to_run: #Cycles through weeks since last run date including last run week and current

    weekly_w_hours,weekly_sm_hours = 0,0

    created = database_scripts.check_exists(week_beginning,settings)

    rotatree, tipsheet, tablepos = web_data.get_web_info(week_beginning,client,settings)

    tips = web_data.get_tips(tipsheet,settings)
    database_scripts.modify_tips(created,week_beginning,tips,settings)

    for day_, index in days_of_week: #Goes through days of week using their index in the table to find our shift information

        rolelist, startendtimes, hoursworked, holiday = web_data.get_schedule(index, rotatree, tablepos)
        w_start, w_end, sm_start, sm_end, w_hours, sm_hours = data_processing.process_schedule(rolelist, startendtimes, hoursworked)

        weekly_w_hours += w_hours
        weekly_sm_hours += sm_hours

        database_scripts.modify_schedule(created,week_beginning,day_,sm_start,sm_end,w_start,w_end,holiday,settings)
    
    database_scripts.modify_hours(created,week_beginning,weekly_sm_hours,weekly_w_hours,settings)

