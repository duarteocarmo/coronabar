import requests
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib

gi.require_version('AppIndicator3', '0.1')
from gi.repository import AppIndicator3 as appindicator

import datetime
import webbrowser

APPINDICATOR_ID = 'Coronabar'

class CoronaMenu(Gtk.Menu):
    base_api_url = "https://coronavirus-19-api.herokuapp.com/countries"
    update_interval = 900  # seconds
    about_url = "https://github.com/duarteocarmo/coronabar"
    
    def __init__(self):
        Gtk.Menu.__init__(self)
        self.default_country = "USA"

        item_select_country = Gtk.MenuItem(label='Select Country')
        
        self.append(item_select_country)
        self.sub_menu = Gtk.Menu()
        item_select_country.set_submenu(self.sub_menu)
        submenu_about = Gtk.MenuItem(label="About")
        submenu_about.connect('activate', self.open_page)
        self.append(submenu_about)

        item_quit = Gtk.MenuItem(label='Quit')
        item_quit.connect('activate', self.quit)
        self.append(item_quit)

        #self.country = self.default_country
        country_list = self.get_country_list()
        self.setup(country_list)

        self.show_all()


    def open_page(self, sender):
        try:
            webbrowser.open(self.about_url)
        except Exception as e:
            print(str(e))
            return False
        

    def setup(self, country_list):
        for country in country_list:
            t = Gtk.MenuItem(label=f"{country}")
            t.connect('activate', self.update_menu, country)
            self.sub_menu.append(t)

        self.create_country_listing(self.default_country)
        current = Gtk.MenuItem(label=f"{self.default_country}")
        self.append(current)
                  
    def create_country_listing(self, country):
        data = self.get_country_data(country)
        for k, v in data.items():
            self.append(Gtk.MenuItem(label=self.string_mapper(k, v)))
        current_time = datetime.datetime.now().strftime("%H:%M")
        self.append(Gtk.MenuItem(label=f"Updated at {current_time}"))
        self.timer = GLib.timeout_add(self.update_interval, self.update_menu, self, country)
        self.show_all()
                    
    def on_update(self):
        for k in self:
            if k.get_properties('label')[0] not in ["Select Country", "Quit", "About"]:
                k.destroy() 
    
    def update_menu(self, widget, country):
        print(country)
        print("updating menu")
        self.on_update()
        data = self.get_country_data(country)
        for k, v in data.items():
            self.insert(
                Gtk.MenuItem(label=self.string_mapper(k, v)), 1
            )
        
        current_time = datetime.datetime.now().strftime("%H:%M")
        self.insert(Gtk.MenuItem(label=f"Updated at {current_time}"), 1
        )
        self.show_all()


    def quit(self, widget):
        Gtk.main_quit()


    # DATA
    def get_country_list(self):
        response = requests.request("GET", self.base_api_url)
        data = response.json()
        country_list = [e["country"] for e in data]
        return sorted(country_list)[1:]

    def get_country_data(self, country):
        response = requests.request("GET", f"{self.base_api_url}/{country}")
        data = response.json()
        return data

    # STRING MAPPER
    def string_mapper(self, key, value):
        if not self.is_camel_case(key):

            return f"{key.title()}: {value}"
        elif key == "todayCases":
            return f"Cases Today: {value}"

        elif key == "todayDeaths":
            return f"Deaths Today: {value}"

        elif key == "casesPerOneMillion":
            return f"Per Million: {value}"

        else:
            return f"{key}: {value}"

    @staticmethod
    def is_camel_case(s):
        # https://stackoverflow.com/a/10182901 thanks :)
        return s != s



class Gui:
    def __init__(self):
        self.indicator = appindicator.Indicator.new(APPINDICATOR_ID,
                                           Gtk.STOCK_DIALOG_INFO,
                                           appindicator.IndicatorCategory.APPLICATION_STATUS)
        self.indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
        self.my_menu = CoronaMenu()
        self.indicator.set_menu(self.my_menu)



def start():

    gui = Gui()
    Gtk.main()

    # goodbye message
    print("Bye!")



if __name__ == "__main__":
    start()
