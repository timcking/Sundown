import kivy
from kivy.app import App
from datetime import date
from astral import Astral

class Sundown():
    def __init__(self, **kwargs):
        super(Sundown, self).__init__(**kwargs)

    def get_astral(self):

        today = date.today()
        long_date = today.strftime("%B %d, %Y")

        city_name = 'Sacramento'

        a = Astral()
        a.solar_depression = 'civil'

        city = a[city_name]

        city_info = str('%s, %s' % (city.name, city.region))

        timezone = city.timezone
        print('Timezone: %s' % timezone)

        lat_lon = ('Latitude: %.03f, Longitude: %.03f\n' % (city.latitude, city.longitude))

        sun = city.sun(date=today)

        # Convert time to 12 hr.
        sunrise_time = sun['sunrise'].strftime("%I:%M %p")
        sunset_time = sun['sunset'].strftime("%I:%M %p")

        return lat_lon, long_date, city_info, sunrise_time, sunset_time
  
class SundownApp(App):
    def on_start(self):
        sd = Sundown()
        lat_lon, long_date, city_info, sunrise, sunset = sd.get_astral()

        self.root.ids.label_sunrise.text = sunrise
        self.root.ids.label_sunset.text = sunset
        date_city = city_info + '\n' + long_date + '\n' + lat_lon
        self.root.ids.label_datetime.text = date_city

if __name__ == '__main__':
    SundownApp().run()
