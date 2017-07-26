import requests

class Dust():
    google_url = "https://maps.googleapis.com/maps/api/geocode/json"

    def __init__(self, api_key):
        self.api_key = api_key

    def getLocation(self, location):
        response = requests.get(self.google_url, params={'address': location}).json()
        if response['status'] == 'OK':
            location_code = response['results'][0]['geometry']['location']
            print(location_code)
            return location_code
        else:
            return None

    def getDust(self, location):
        pass

if __name__ == '__main__':
    dust = Dust('test')
    #dust.getLocation('서울')
    #dust.getLocation('광주')
    #dust.getLocation('경기')
    dust.getLocation('서울 광진구')
