import csv
import fitbit
import json
import time
import datetime
import os
import pprint
import sys
import webbrowser
import keys

from fitbit.api import FitbitOauthClient

class FitbitDownloader:
    AUTHD_CLIENT = None
    OWNER_KEY = None
    OWNER_SECRET = None
    CLIENT_KEY = keys.CLIENT_KEY
    CLIENT_SECRET = keys.CLIENT_SECRET

    def gather_keys(self):
        # setup
        pp = pprint.PrettyPrinter(indent=4)
        client = FitbitOauthClient(self.CLIENT_KEY, self.CLIENT_SECRET)

        # get request token
        print('* Obtain a request token ...')
        token = client.fetch_request_token()
        print('* Authorize the request token in your browser')
        stderr = os.dup(2)
        os.close(2)
        os.open(os.devnull, os.O_RDWR)
        webbrowser.open(client.authorize_token_url())
        os.dup2(stderr, 2)
        try:
            verifier = raw_input('Verifier: ')
        except NameError:
            # Python 3.x
            verifier = input('Verifier: ')

        # get access token
        print('* Obtain an access token ...')
        token = client.fetch_access_token(verifier)
        print('RESPONSE')
        pp.pprint(token)
        self.OWNER_KEY = token['oauth_token']
        self.OWNER_SECRET = token['oauth_token_secret']
        print self.OWNER_KEY
        print self.OWNER_SECRET
        print('')

    def create_client(self):
        # You'll have to gather the user keys on your own, or try 
        # ./fitbit/gather_keys_cli.py <con_key> <con_sec> for development
        self.AUTHD_CLIENT = fitbit.Fitbit(
                self.CLIENT_KEY, 
                self.CLIENT_SECRET, 
                resource_owner_key=self.OWNER_KEY, 
                resource_owner_secret=self.OWNER_SECRET
                )

    def print_1w_steps(self):
        print json.dumps(selfAUTHD_CLIENT.time_series(
            'activities/minutesVeryActive', 
            base_date='today', period='1w'), 
            indent=4, sort_keys=True)

    def get_all_data(self):
        memberSince = datetime.datetime.strptime(
                self.get_membership_since(), '%Y-%m-%d').date()
        current_date = datetime.datetime.now().date()
        num_of_weeks = ((current_date - memberSince).days / 7) + 1
        week_counter = 1
        data = []

        while current_date > memberSince:
            print "Week %d of %d \r" % (week_counter, num_of_weeks)
            data.extend(reversed(self.AUTHD_CLIENT.time_series('activities/steps', 
                base_date=current_date.strftime('%Y-%m-%d'), 
                period='1w')['activities-steps']))
            current_date -= datetime.timedelta(weeks=1)
            week_counter += 1

        return data


    def get_todays_steps(self):
            return self.AUTHD_CLIENT.time_series(
                'activities/steps', 
                base_date='today', period='1d')['activities-steps'][0]['value']

    def get_membership_since(self):
            return self.AUTHD_CLIENT.user_profile_get()['user']['memberSince']

    def createCsv(self, jsonData, csvFile='data.csv'):
        with open(csvFile, 'wb+') as outfile:
            f = csv.writer(outfile)
            f.writerow(['date', 'value'])

            for row in jsonData:
                f.writerow([row['dateTime'], row['value']])

if __name__ == '__main__':

    fd = FitbitDownloader()

    print "Fitbit data downloader, getting access to your account..."
    fd.gather_keys()
    print "Grabbing some info about you..."
    fd.create_client()
    print "Member since: %s" % fd.get_membership_since()
    print "Todays steps: %s" % fd.get_todays_steps()
    print "Exporting data to scv file"
    fd.createCsv(fd.get_all_data()) 

