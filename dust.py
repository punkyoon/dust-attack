import requests

class Dust():
    google_url = 'https://maps.googleapis.com/maps/api/geocode/json'
    wapi_url = 'https://api.waqi.info/feed/geo:'

    def __init__(self, api_key):
        self.api_key = api_key

    def getLocation(self, location):
        response = requests.get(self.google_url, params={'address': location}).json()
        if response['status'] == 'OK':
            location_code = response['results'][0]['geometry']['location']
            return location_code
        else:
            return None

    def getDust(self, location_code):
        formats = (location_code['lat'], location_code['lng'])
        url = 'https://api.waqi.info/feed/geo:%s;%s/' % formats
        response = requests.get(url, params={'token': self.api_key}).json()
        dust = response['data']['aqi']

        msg = None

        if dust > 300:
            msg = '위험: 환자군 및 민감군에게 응급 조치가 발생되거나, 일반인에게 유해한 영향이 유발될 수 있는 수준'
        elif dust > 200:
            msg = '매우 나쁨: 환자군 및 민감군에게 급성 노출시 심각한 영향 유발, 일반인도 약한 영향이 유발될 수 있는 수준'
        elif dust > 150:
            msg = '나쁨: 환자군 및 민감군에게 유해한 영향 유발, 일반인도 건강상 불쾌감을 느낄 수 있는 수준'
        elif dust > 100:
            msg = '민감군 영향: 환자군 및 민감군에게 유해한 영향이 유발될 수 있는 수준'
        elif dust > 50:
            msg = '보통: 환자군에게 만성 노출시 경미한 영향이 유발될 수 있는 수준'
        else:
            msg = '좋음: 대기오염 관련 질환자군에서도 영향이 유발되지 않을 수준'
        
        full_msg = '현재 대기 품질 지수(AQI)는 ' + str(dust) + '이며, 현재 대기상황은 ' + msg + '입니다.'

        return full_msg

if __name__ == '__main__':
    dust = Dust('demo')
    location = dust.getLocation('서울 광진구')
    print(dust.getDust(location))
