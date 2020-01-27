import time
import kivy
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.app import App
from datetime import date
from astral import Astral

class Sundown():
    def __init__(self, **kwargs):
        super(Sundown, self).__init__(**kwargs)

    def get_astral(self, city_name):

        today = date.today()
        long_date = today.strftime("%B %d, %Y")

        a = Astral()
        a.solar_depression = 'civil'

        # If city not found, set to default Sacramento
        try:
            city = a[city_name]
            city_info = str('%s, %s' % (city.name, city.region))
        except Exception as e:
            popup = Popup(title='Sundown',
               content=Label(text='City ' + city_name + ' not found.'), size_hint=(.6, .4))
            popup.open()

            city = a['Sacramento']
            city_info = str('%s, %s' % (city.name, city.region))

        # timezone = city.timezone
        # print('Timezone: %s' % timezone)

        lat_lon = ('Latitude: %.03f, Longitude: %.03f\n' % (city.latitude, city.longitude))

        sun = city.sun(date=today)

        # Convert time to 12 hr.
        sunrise_time = sun['sunrise'].strftime("%I:%M %p")
        sunset_time = sun['sunset'].strftime("%I:%M %p")

        return lat_lon, long_date, city_info, sunrise_time, sunset_time

class SundownApp(App):
    sd = Sundown()

    def on_start(self):
        self.icon = './data/sunset.png'

        # Initially default to Sacramento
        self.search_city('Sacramento')

    def on_search(self):
        city = self.root.ids.search_text.text

        if city:
            self.search_city(city)
            self.root.ids.search_text.text = ''

    def search_city(self, city):
        lat_lon, long_date, city_info, sunrise, sunset = self.sd.get_astral(city)

        self.root.ids.label_sunrise.text = sunrise + '\nSunrise'
        self.root.ids.label_sunset.text = sunset + '\nSunset'
        date_city = city_info + '\n' + long_date + '\n' + lat_lon
        self.root.ids.label_datetime.text = date_city

if __name__ == '__main__':
    SundownApp().run()
