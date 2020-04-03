import requests
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

gi.require_version('AppIndicator3', '0.1')
from gi.repository import AppIndicator3 as appindicator

APPINDICATOR_ID = 'Coronabar'

class CoronaMenu(Gtk.Menu):
    def __init__(self):
        Gtk.Menu.__init__(self)

        item_select_country = Gtk.MenuItem(label='Select Country')
        #item_select_country.connect('activate', self.select_country)
        self.append(item_select_country)
        self.sub_menu = Gtk.Menu()
        item_select_country.set_submenu(self.sub_menu)
        submenu_item = Gtk.MenuItem(label="Test")
        submenu_item.connect('activate', self.test)
        self.sub_menu.append(submenu_item)

        item_quit = Gtk.MenuItem(label='Quit')
        item_quit.connect('activate', self.quit)
        self.append(item_quit)

        self.show_all()

    def test(self, widget):
        print("Hello China, this is a test")    
    def select_country(self, widget):
        pass

    def quit(self, widget):
        Gtk.main_quit()



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