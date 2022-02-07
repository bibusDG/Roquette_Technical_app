import time
from kivy.base import runTouchApp
from kivy.uix.dropdown import DropDown
from kivy.properties import ObjectProperty
from product_lists_json import data
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.button import ButtonBehavior
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from product_lists_json import hi_cat
from kivy.uix.popup import Popup
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.scrollview import ScrollView
from kivy.properties import StringProperty, ListProperty
from kivy.clock import Clock

product_label = []
#################################################################################

class ProductScreen(Screen):

    pass



class DetailedProductScreen(Screen):
    #
    # def __init__(self, **kwargs):
    #     super(DetailedProductScreen, self).__init__(**kwargs)
    #     self.build_grid()
    # def on_enter(self, *args):
    #     self.build_grid()

    color_list = {}

    def on_enter(self):
        # pr_grid = GridLayout(cols=3, spacing=7, row_force_default=True, row_default_height=40, pos_hint={'top': .80, 'center_x': .5}, size_hint=(1, .6))



        for name in data['product'][HomeScreen.tab]:
            if data['product'][HomeScreen.tab][name]['Raw material'] == 'Wheat':
                color = (1, 1, 1, 1)
            if data['product'][HomeScreen.tab][name]['Raw material'] == 'Corn':
                color = (3, 2, 1, 1)
            if data['product'][HomeScreen.tab][name]['Raw material'] == 'Potato':
                color = (1, 0, 0, 1)
            if data['product'][HomeScreen.tab][name]['Raw material'] == 'Pea':
                color = (3, 2, 1, 1)
            if data['product'][HomeScreen.tab][name]['Raw material'] == 'Corn/Potato':
                color = (1, 2, 2, 1)
            DetailedProductScreen.color_list[name] = color

        for name in data['product'][HomeScreen.tab]:
            btn = Button(text=str(name))
            btn.background_color = DetailedProductScreen.color_list[name]
            self.ids[name] = btn
            btn.bind(on_release=self.back_to_color)
            self.ids.grid.add_widget(btn)

    def back_to_color(self, instance):
        print(instance.text)
        # for name in DetailedProductScreen.color_list:
        #     print(name)
        # for id, widget in instance.ids.items():
        #     print(id)
        #     if widget.__self__ == instance:
        #         # instance.background_color = hi_cat()[id]
        #         print(id)
        #
        box = GridLayout(cols=1, rows=10, pos_hint={'top': .9, 'left': 1}, size_hint=(1, .7))
        for i in data['product'][HomeScreen.tab][instance.text]:
            type_label = Label(font_size=20, text=i.upper() + " :   " + data['product'][HomeScreen.tab][instance.text][i].upper(),
                               size_hint=(1, 1))
            box.add_widget(type_label)

        popupWindow = Popup(title=instance.text.upper(),  content=box, size_hint=(None, None), size=(400, 500))
        time.sleep(0.3)
        popupWindow.open()  # show the popup


        # self.add_widget(pr_grid)

    def on_leave(self):
        self.ids.grid.clear_widgets()
        print(HomeScreen.tab)

# name_color = {}


class HomeScreen(Screen):

    tab = 'Cboard'
    def product_name(self, name):
        self.manager.get_screen('product_screen').ids.name_label.text = name.upper()
        self.manager.get_screen('detailed_product_screen').ids.name_label.text = name.upper()
        self.manager.get_screen('calc_screen').ids.name_label.text = name.upper()
        product_label.append(name)
        HomeScreen.tab = name
        # DetailedProductScreen().build_grid()
        # print(HomeScreen.tab)
    #     # self.manager.get_screen('product_screen').ids.product_ico.name = name

    pass
    """
    HomeScreen class
    """



#
# class HiCatScreen(Screen):
#
#     pass


class ImageButton(ButtonBehavior, Image):
    """
    Class for buttons made from images
    """
    pass


# class ProductButtons(Screen):
#
#     pass


class PopUpWindow(FloatLayout):

    pass

class CalcScreen(Screen):


    def on_enter(self):
        print(self.ids.name_label.text)
        if self.ids.name_label.text == 'HI-CAT':
            self.ids.calc_screen_box.add_widget(HiCatCalc())
        if self.ids.name_label.text == 'CBOARD':
            self.ids.calc_screen_box.add_widget(CBoardCalc())
        if self.ids.name_label.text == 'VECTOR':
            self.ids.calc_screen_box.add_widget(VectorCalc())
        if self.ids.name_label.text == 'EVO':
            self.ids.calc_screen_box.add_widget(EvoCalc())
        if self.ids.name_label.text == 'ENZYME':
            self.ids.calc_screen_box.add_widget(EnzymeCalc())
    def on_leave(self):
        self.ids.calc_screen_box.clear_widgets()
        print('end')



class HiCatCalc(Screen):

    spinner = ObjectProperty()
    estimated_value = 0
    consum = 0
    cooker_range = ''
    loss_on_drying = 0
    slurry_concentration = 0
    final_concentration = 0

    def app_spinner(self, text):
        if text == 'WET-END':
            self.estimated_value = 4
        if text == "STRENGTH":
            self.estimated_value = 10
        self.ids.dosing.text=str(self.estimated_value) + ' KG/T'

    def starch_spinner(self, text):
        self.ids.starch_spinner.values = [str(x) for x in data['product']['Hi-Cat']]

    def starch_spinner_cooker_range(self, text):
        self.loss_on_drying = int(data['product']['Hi-Cat'][text]['Loss on drying'][0:2])

    def consumption(self, text):
        self.consum=int(text)

    def slurry_conc(self, text):
        self.slurry_concentration = int(text)

    def final_starch(self, text):
        self.final_concentration = int(text)

    def calculate_data(self):
        if self.slurry_concentration == 0 or self.final_concentration == 0:
            pass
        else:
            self.ids.consumption.text = str((int(self.consum) * int(self.estimated_value)*24*31)/1000) + ' t/month'

            cook_range_min = round(int(self.consum) * 0.85 * int(self.estimated_value) * (1 - (int(self.loss_on_drying))/100))
            cook_range_max = round(int(self.consum) * 1.5 * int(self.estimated_value) * (1 - (int(self.loss_on_drying))/100))
            HiCatCalc.cooker_range = str(cook_range_min) + ' - ' + str(cook_range_max)
            self.ids.cooker_range.text = self.cooker_range + ' kg/h d.s.s'

            water_range_min = round(((cook_range_min*100)/self.slurry_concentration)-cook_range_min)
            water_range_max = round(((cook_range_max*100)/self.slurry_concentration)-cook_range_max)
            self.ids.slurry_water.text = str(water_range_min) + 'l/h - ' + str(water_range_max) + 'l/h'

            dil_water_range_min = round(((cook_range_min * 100) / self.final_concentration) - cook_range_min - water_range_min)
            dil_water_range_max = round(((cook_range_max * 100) / self.final_concentration) - cook_range_max - water_range_max)
            self.ids.dilution_water.text = str(dil_water_range_min) + 'l/h - ' + str(dil_water_range_max) + 'l/h'

            water_cosnumption_min = round(((water_range_min + dil_water_range_min)*24*31)/1000)
            water_cosnumption_max = round(((water_range_max + dil_water_range_max)*24*31)/1000)
            self.ids.water_cons.text = str(water_cosnumption_min) + 'm3/m - ' + str(water_cosnumption_max) + 'm3/m'


class VectorCalc(Screen):

    dry_solid = 0
    vector_dosing = 0
    vector_production = 0
    vector_fnal = 0
    vector_commercial = 0
    vector_dilution = 0
    vector_volume = 0

    def vector_spinner(self, text):
        self.ids.vector_spinner.values = [str(x) for x in data['product']['Vector']]

    def vector_dry_solid(self, text):
        self.dry_solid = int(data['product']['Vector'][text]['Loss on drying'][0:2])
        self.ids.vector_dry_solid.text = str(self.dry_solid) + ' %'

    def vector_dosing(self, text):
        self.vector_dosing = int(text)

    def vector_production(self, text):
        self.vector_production = int(text)

    def vector_final(self, text):
        self.vector_fnal = int(text)

    def vector_calculations(self):

        self.vector_commercial = round(self.vector_dosing/int(self.dry_solid)*100*self.vector_production)
        self.ids.commercial_vector.text = str(self.vector_commercial) + ' l/h'

        self.vector_dilution = round(int(self.dry_solid)/self.vector_fnal*self.vector_commercial-self.vector_commercial)
        self.ids.vector_dilution.text = str(self.vector_dilution) + ' l/h'

        self.ids.vector_volume.text = str(self.vector_dilution+self.vector_commercial)
        self.ids.total_vector.text = str(self.vector_commercial*24*31/1000) + ' m3/mth'
        self.ids.total_water.text = str(self.vector_dilution*24*31/1000) + ' m3/mth'


class EvoCalc(Screen):

    def evo_spinner(self, text):
        self.ids.evo_spinner.values = [str(x) for x in data['product']['Evo']]

    pass

class CBoardCalc(Screen):

    def cboard_spinner(self, text):
        self.ids.cboard_spinner.values = [str(x) for x in data['product']['Cboard']]

    pass

class EnzymeCalc(Screen):



    pass

# GUI = Builder.load_file('main.kv')


screen_list = ['home_screen']  # list of visited screens for "BECK" button
button_pressed = {'products': 0, 'calc': 0}


class MainRoquetteApp(App):

    def build(self):
        GUI = Builder.load_file('main.kv')
        return GUI

    def change_screen(self, screen_name):

        """
        Function to change the screen
        :param screen_name: name of chosen screen
        """
        screen_manager = self.root.ids['screen_manager']
        screen_manager.current = screen_name
        if screen_name not in screen_list:
            screen_list.append(screen_name)

    def previous_screen(self):

        """
        Function to find previous screen from list of visited screens
        :return: last visited screen
        """
        screen_list.remove(screen_list[-1])
        return screen_list[-1]


    def zeroing_list(self):
        screen_list.clear()
        screen_list.append('home_screen')




    # def product_button(self):
    #     button_pressed['products'] = 1
    #     button_pressed['calc'] = 0
    #
    #
    # def calc_button(self):
    #     button_pressed['calc'] = 1
    #     button_pressed['products'] = 0

    def list_of_products(self, text):
        if text == 'hi-cat':
            return hi_cat()


if __name__ == '__main__':

    MainRoquetteApp().run()
