import argparse
import os
from datetime import datetime

import requests

parser = argparse.ArgumentParser(description='A tool to bulk apply elevation correction to TrainingPeaks activities')
parser.add_argument('--start-date', help='Beginning of date range for bulk elevation correction', required=True)
parser.add_argument('--end-date', help='End of date range for bulk elevation correction. Defaults to current date',
                    default=datetime.today().strftime('%Y-%m-%d'))
parser.add_argument('--tags',
                    help='A list of tags for identifying activities to be corrected, ex: --tags=running,cycling',
                    nargs='+', default=[])

args = vars(parser.parse_args())

start_date = args.get('start_date')
end_date = args.get('end_date')
tags = set(map(str.lower, args.get('tags')))

athlete_id = os.environ.get('TRAININGPEAKS_ATHLETE_ID')
user_agent = os.environ.get('TRAININGPEAKS_USER_AGENT')
cookie = os.environ.get('TRAININGPEAKS_SESSION_COOKIE')

headers = {
    'User-Agent': user_agent,
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'en-US,en;q=0.5',
    'Content-Type': 'application/json',
    'Origin': 'https://app.trainingpeaks.com',
    'Connection': 'keep-alive',
    'Referer': 'https://app.trainingpeaks.com/',
    'Cookie': cookie,
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
    'TE': 'trailers'
}

get_activities = requests.get(
    'https://tpapi.trainingpeaks.com/fitness/v1/athletes/{athlete_id}/workouts/{start_date}/{end_date}'.format(
        athlete_id=athlete_id, start_date=start_date, end_date=end_date), headers=headers)

workouts_json = get_activities.json()

runs = []

for workout in workouts_json:
    if len(tags) > 0:
        user_tags = workout['userTags']
        if user_tags is not None:
            user_tags = set(map(str.lower, user_tags.split(',')))
            if tags & user_tags:
                runs.append(workout['workoutId'])
    else:
        runs.append(workout['workoutId'])

for run in runs:
    correct_elevation = requests.post(
        'https://tpapi.trainingpeaks.com/groundcontrol/v2/commands/workouts/{run}/applyelevationstofile'.format(
            run=run), headers=headers, data={})

    print("Activity ID: {run}, Status Code: {status_code}".format(run=run, status_code=correct_elevation.status_code))
