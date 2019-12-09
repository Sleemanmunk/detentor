import json
import os
from datetime import datetime, timedelta
from pprint import pprint

MAX_DETENTION_OPPORTUNITIES = 4

if __name__=="__main__":
    if os.path.exists('infractions.json'):
        with open('infractions.json','r') as f:
            infractions = json.load(f)
    else:
        infractions = []

    command = ""
    state = "START"

    prompt_suffix = "\nq to quit \nr to restart"

    new_infraction = {}
    while command.lower() != 'q':
        if command == 'r' or state=="START":
            for infraction in infractions:
                print(infraction['student'], "must attend detention for infraction \""+
                      infraction['description']+
                      "\" committed on", infraction['date'])
                infraction_date = datetime.strptime(infraction['date'], '%m/%d/%y').date()
                current_date = datetime.now().date()
                delta = current_date-infraction_date
                detention_opportunities = []
                for i in range(delta.days + 1):
                    day = infraction_date + timedelta(days=i)
                    if day.strftime("%a") in  ["Wed","Thu"]:
                        detention_opportunities.append(day)
                if len(detention_opportunities) >= MAX_DETENTION_OPPORTUNITIES:
                    for day in detention_opportunities:
                        print(f"check if {infraction['student']} attended detention on {day.strftime('%m/%d/%y')}")
                        command = input("(y/n)")
                        if (command == "y"):
                            print (f"removing {infraction['student']} from detention list")
                            infractions.remove(infraction)
                            break
                    print (f"{infraction['student']} has missed {MAX_DETENTION_OPPORTUNITIES} or more detention opportunities. Raise infraction level and reset date?")
                    command = input("(y/n)")
                    if(command=="y"):
                        infraction['level']+=1
                        infraction['date'] = current_date.strftime('%m/%d/%y')
                        print(f"{infraction['student']}'s infraction level has risen to {infraction['level']}")
                else:
                    print(f"{infraction['student']} still has {MAX_DETENTION_OPPORTUNITIES - len(detention_opportunities)}"
                          f" opportunity to visit detention")

            state = "STUDENT"
            new_infraction = {}
        if state == "STUDENT":
            print("Record a new infraction")
            command = input("enter a student name"+prompt_suffix)
            new_infraction['student'] = command
            state = "DESCRIPTION"
        elif state == "DESCRIPTION":
            command=input("enter an infraction description (must be one line)" + prompt_suffix)
            new_infraction['description'] = command
            state = "REVIEW"
        elif state == "REVIEW":
            new_infraction['date'] = datetime.now().date().strftime("%D")
            new_infraction['level'] = 0
            pprint(new_infraction)
            command = input("press ENTER to submit." + prompt_suffix)
            state = "SUBMIT"
        elif state == "SUBMIT":
            infractions.append(new_infraction)
            state = "START"

    with open('infractions.json','w') as f:
        json.dump(infractions,f)