from datetime import datetime, timedelta

def get_birthdays_per_week(users):

    today = datetime.now().date() # 2020-10-09 
    next_week = today + timedelta(days=7)
    print(f"next weeek {next_week}")
    days_list = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    users_to_congratulate = {}

    for day in days_list:
        users_to_congratulate[day] = []

    for i in users:
        dr = i['birthday'].date().replace(year=today.year) # взяли дату, наприклад 2023-05-17
        print(dr)
        weekday = days_list[dr.weekday()] # знаходим день тижня
        if dr >= today and dr <= next_week:
            users_to_congratulate[weekday].append(i["name"])
        elif dr < today and dr.weekday() == 5 or dr.weekday() == 6:
            users_to_congratulate["Monday"].append(i["name"])

    for k, v in users_to_congratulate.items():
        if v:
            print (f"{k}: {','.join(v)}")

res = get_birthdays_per_week ( [
        {'name':'ivan', 'birthday': datetime(1970, 5, 17)}, 
        {'name':'oleg', 'birthday': datetime(1988, 5, 13)},
        {'name':'petro', 'birthday': datetime(1956, 5, 21)},
        {'name':'vita', 'birthday': datetime(1999, 5, 30)}
        ])
print (res)