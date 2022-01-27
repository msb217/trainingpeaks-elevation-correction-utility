# TrainingPeaks Elevation Correction Utility
This utility will select an athlete's activities in TrainingPeaks within a specified date range and apply elevation correction to them.

TrainingPeaks does not support auto-applying elevation correction to activities, nor does it support bulk applying elevation correction to many activities at a time.

This script is useful if you have hundreds of activities you'd like to apply elevation correction to and do not want to manually correct all of them via the web app.

## Usage
1. Sign into TrainingPeaks via your web browser  
2. Navigate to the 'Network' tab of your browser's dev tools  
3. Obtain the two request headers `Cookie` and `User-Agent` from a request to `tpapi.trainingpeaks.com`. You may need to check multiple requests for `Cookie`. You will need to update `Cookie` whenever your TrainingPeaks session is closed.
4. Set `Cookie` and `User-Agent` as environment variables with the names `TRAININGPEAKS_SESSION_COOKIE` and `TRAININGPEAKS_USER_AGENT`
5. Find a request to `tpapi.trainingpeaks.com` with the path prefix `/fitness/v1/athletes/{athlete_id}`.
6. Set the numeric `athlete_id` to an environment variable `TRAININGPEAKS_ATHLETE_ID`

```
➜  python correct.py --start-date 2021-01-01 --tags running cycling

➜  python correct.py -h
usage: correct.py [-h] --start-date START_DATE [--end-date END_DATE]
                 [--tags TAGS [TAGS ...]]

A tool to bulk apply elevation correction to TrainingPeaks activities

optional arguments:
  -h, --help            show this help message and exit

  --start-date START_DATE
                        Beginning of date range for bulk elevation correction (YYYY-mm-dd)

  --end-date END_DATE   End of date range for bulk elevation correction (YYYY-mm-dd)
                        Defaults to current date

  --tags TAGS [TAGS ...]
                        A list of tags for identifying activities to be
                        corrected, ex: '--tags running cycling'
```
