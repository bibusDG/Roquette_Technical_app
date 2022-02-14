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

warning_popup = Popup(title = 'Warning', content = Label(text='Please insert number'), size_hint_x=.6, size_hint_y=.6)
zero_division_popup = Popup(title = 'Warning', content = Label(text='Please insert right values'), size_hint_x=.6, size_hint_y=.6)
no_product_warning = Popup(title = 'Warning', content = Label(text='No products'), size_hint_x=.6, size_hint_y=.6)

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

        try:

            for name in data['product'][HomeScreen.tab]:
                if data['product'][HomeScreen.tab][name]['Raw material'] == 'Wheat':
                    color = (1, 1, 1, 1)
                if data['product'][HomeScreen.tab][name]['Raw material'] == 'Corn':
                    color = (3, 2, 1, 1)
                if data['product'][HomeScreen.tab][name]['Raw material'] == 'Potato':
                    color = (1, 0, 0, 1)
                if data['product'][HomeScreen.tab][name]['Raw material'] == 'Pea':
                    color = (1, 2, 1, 1)
                if data['product'][HomeScreen.tab][name]['Raw material'] == 'Mix':
                    color = (1, 2, 2, 1)
                self.color_list[name] = color

            for name in data['product'][HomeScreen.tab]:
                btn = Button(text=str(name), color=(0,0,0,1), bold=True)
                btn.background_color = self.color_list[name]
                self.ids[name] = btn
                btn.bind(on_release=self.back_to_color)
                self.ids.grid.add_widget(btn)

        except KeyError:
            no_product_warning.open()

    def back_to_color(self, instance):
        # print(instance.text)
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
            type_label = Label(font_size=15, text=i.upper() + " :   " + data['product'][HomeScreen.tab][instance.text][i].upper(),
                               size_hint=(1, 1))
            box.add_widget(type_label)

        popupWindow = Popup(title=instance.text.upper(),  content=box, size_hint=(None, None), size_hint_x=.8, size_hint_y=.8)
        time.sleep(0.3)
        popupWindow.open()  # show the popup


        # self.add_widget(pr_grid)

    def on_leave(self):
        self.ids.grid.clear_widgets()
        # print(HomeScreen.tab)

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
        # print(self.ids.name_label.text)
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
        # print('end')



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
        if len(text) == 0 or text == '0':
            warning_popup.open()
            pass
        else:
            self.consum=int(text)

    def slurry_conc(self, text):
        if len(text) == 0 or text == '0':
            warning_popup.open()
            pass
        else:
            self.slurry_concentration = int(text)

    def final_starch(self, text):
        if len(text) == 0 or text == '0':
            warning_popup.open()
            pass
        else:
            self.final_concentration = int(text)

    def calculate_data(self):

        try:

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

        except ZeroDivisionError:
            zero_division_popup.open()

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
        self.dry_solid = int(data['product']['Vector'][text]['Dry substance'][0:2])
        self.ids.vector_dry_solid.text = str(self.dry_solid) + ' %'

    def vector_dosings(self, text):
        if len(text) == 0 or text == '0':
            warning_popup.open()
            pass
        else:
            self.vector_dosing = int(text)

    def vector_productions(self, text):
        if len(text) == 0 or text == '0':
            warning_popup.open()
            pass
        else:
            self.vector_production = int(text)

    def vector_final(self, text):
        if len(text) == 0 or text == '0':
            warning_popup.open()
            pass
        else:
            self.vector_fnal = int(text)

    def vector_calculations(self):

        try:

            self.vector_commercial = round(self.vector_dosing/int(self.dry_solid)*100*self.vector_production)
            self.ids.commercial_vector.text = str(self.vector_commercial) + ' l/h'

            self.vector_dilution = round(int(self.dry_solid)/self.vector_fnal*self.vector_commercial-self.vector_commercial)
            self.ids.vector_dilution.text = str(self.vector_dilution) + ' l/h'

            self.ids.vector_volume.text = str(self.vector_dilution+self.vector_commercial)
            self.ids.total_vector.text = str(self.vector_commercial*24*31/1000) + ' m3/mth'
            self.ids.total_water.text = str(self.vector_dilution*24*31/1000) + ' m3/mth'

        except ZeroDivisionError:
            zero_division_popup.open()



class EvoCalc(Screen):

    variables = {'batches': 0, 'prod_day': 0, 'latex_price': 0, 'evo_price': 0, 'latex_dry': 0, 'ds_latex': 0,
                 'ds_evo': 0, 'latex_part': 0, 'evo_part': 0, 'st_latex': 0, 'st_evo': 0, 'tr_latex': 0, 'tr_evo': 0,
                 'button_pressed': 0}

    prices = {}

    prod_rate = 0
    evo_dry = 0
    latex_dry_euro = 0
    evo_dry_euro = 0
    latex_part_dry = 0
    evo_part_dry = 0

    def button_pressed(self):
        self.variables['button_pressed'] = 1

    def evo_spinner(self, text):
        self.ids.evo_spinner.values = [str(x) for x in data['product']['Evo']]

    def spinner_on_text(self, text):
        self.evo_dry = int(data['product']['Evo'][text]['Loss on drying'][0:2])
        self.ids.evo_dry.text = str(100 - self.evo_dry) + ' %'

    def variable_input(self, text, name):
        if len(text) == 0:
            warning_popup.open()
            pass
        else:
            self.variables[name] = int(text)

    def add_cost_popup_button(self):
        if self.variables['button_pressed'] == 0:
            pop_btn = Button(text='SHOW COSTS')
            self.ids.bottom_line.add_widget(pop_btn)
            pop_btn.bind(on_release=self.cost_popup)
            print(self.variables['button_pressed'])
        else:
            pass

    def cost_popup(self, *args):

        self.prices['STD.COST/BATCH'] = round((self.variables['st_evo']*self.evo_part_dry*self.evo_dry_euro)/1000 + \
                                        (self.variables['st_latex'] * self.latex_part_dry*self.latex_dry_euro/1000), 2)
        self.prices['STD.COST/DAY'] = round(self.prices['STD.COST/BATCH'] * self.variables['batches'],2)
        self.prices['STD.COST/YEAR'] = round(self.prices['STD.COST/DAY'] * self.variables['prod_day'],2)

        self.prices['EVO.COST/BATCH'] = round(
            (self.variables['tr_evo'] * self.evo_part_dry * self.evo_dry_euro) / 1000 + \
            (self.variables['tr_latex'] * self.latex_part_dry * self.latex_dry_euro / 1000), 2)
        self.prices['EVO.COST/DAY'] = round(self.prices['EVO.COST/BATCH'] * self.variables['batches'], 2)
        self.prices['EVO.COST/YEAR'] = round(self.prices['EVO.COST/DAY'] * self.variables['prod_day'], 2)
        self.prices['SAVING/YEAR'] = round(self.prices['STD.COST/YEAR'] - self.prices['EVO.COST/YEAR'], 2)

        pricing_box = GridLayout(cols=1, rows=10, spacing=10, pos_hint={'top': .9, 'left': 1}, size_hint=(1, .7))
        for data in self.prices:
            type_label = Label(font_size=15,
                               text=data + " :   " + str(self.prices[data]) + '€',
                               size_hint=(1, 1))
            pricing_box.add_widget(type_label)


        calc_popup = Popup(title='SUMMARY COSTS', content=pricing_box, size_hint=(None, None), size=(380, 500))
        time.sleep(0.3)
        calc_popup.open()

    def evo_calculations(self):

        try:

            self.prod_rate = round(self.variables['prod_day']*100/365, 2)
            self.ids.prod_rate.text = str(self.prod_rate) + ' %'

            self.latex_dry_euro = round(self.variables['latex_price'] * 100/ self.variables['latex_dry'], 2)
            self.ids.latex_dry_euro.text = str(self.latex_dry_euro) + ' €/T'

            self.evo_dry_euro = round(self.variables['evo_price'] * 100 / (100-self.evo_dry), 2)
            self.ids.evo_dry_euro.text = str(self.evo_dry_euro) + ' €/T'

            self.latex_part_dry = round(self.variables['latex_part'] *self.variables['ds_latex'] / 100, 2)
            self.ids.latex_part_dry.text = str(self.latex_part_dry) + ' kg dry'

            self.evo_part_dry = round(self.variables['evo_part'] * self.variables['ds_evo'] / 100, 2)
            self.ids.evo_part_dry.text = str(self.evo_part_dry) + ' kg dry'

        except ZeroDivisionError:
            zero_division_popup.open()



        pass


    pass

class CBoardCalc(Screen):

    variables = {'b_coef': 1, 'c_coef': 1, 'e_coef': 1, 'be_coef': 2, 'bc_coef': 2, 'ce_coef': 2, 'tot_starch': 0, 'b_total': 0,
                 'c_total': 0, 'e_total': 0, 'be_total': 0, 'bc_total': 0, 'ce_total': 0, 'sode_kg': 0, 'sode_conc': 0, 'new_sode_conc': 0}

    calculation = 0
    sode_calc = 0

    def cboard_spinner(self, text):
        self.ids.cboard_spinner.values = [str(x) for x in data['product']['Cboard']]

    def cboard_spinner_starch(self, text):
        pass

    def total_starch(self, text, name):
        if len(text) == 0:
            warning_popup.open()
        else:
            self.variables[name] = int(text)

    def amount(self, text, name):
        if len(text) == 0:
            warning_popup.open()
        else:
            self.variables[name] = int(text)

    def coeficient(self, text, name):
        if len(text) == 0:
            warning_popup.open()
        else:
            self.variables[name] = float(text)


    def calculate(self):

        try:

            self.calculation = round(self.variables['tot_starch']/((self.variables['b_coef']*self.variables['b_total']) +
                                    (self.variables['e_coef']*self.variables['e_total']) + (self.variables['c_coef']*self.variables['c_total'])
                                    + (self.variables['be_coef']*self.variables['be_total'])+
                                    (self.variables['bc_coef']*self.variables['bc_total']) + (self.variables['ce_coef']*self.variables['ce_total']))*1000, 2)
            self.ids.result.text = str(self.calculation) + ' g/m2'

        except ZeroDivisionError:
            zero_division_popup.open()

    def sode_calculation(self):

        try:

            self.sode_calc = round((self.variables['sode_kg'] * self.variables['sode_conc']) / self.variables['new_sode_conc'], 1)
            self.ids.new_sode_kg.text = str(self.sode_calc) + ' kg'

        except ZeroDivisionError:
            zero_division_popup.open()
    pass

class EnzymeCalc(Screen):

    moisture = 0
    starch_dose = 0
    production = 0
    slurry_conc = 0
    final_conc = 0
    slurry_water = 0
    dilution_water = 0
    enzyme_flow = 0
    total_water = 0
    total_enzyme = 0

    def starch_spinner(self, text):
        self.ids.enzyme_spinner.values = [str(x) for x in data['product']['Enzyme']]

    def enzyme_spinner(self, text):
        self.moisture = int(data['product']['Enzyme'][text]['Loss on drying'][0:2])

    def starch_dosing(self, text):
        if len(text) == 0 or text == '0':
            warning_popup.open()
            pass
        else:
            self.starch_dose = int(text)

    def productions(self, text):
        if len(text) == 0 or text == '0':
            warning_popup.open()
            pass
        else:
            self.production = int(text)

    def slurry_concent(self, text):
        if len(text) == 0 or text == '0':
            warning_popup.open()
            pass
        else:
            self.slurry_conc = int(text)

    def final_concent(self, text):
        if len(text) == 0 or text == '0':
            warning_popup.open()
            pass
        else:
            self.final_conc = int(text)

    def enzyme_calculation(self):

        try:

            self.ids.consumption.text = str((self.starch_dose * self.production*24*31)/1000) + ' t/month'
            self.slurry_water = round(((self.starch_dose * self.production)*100*(1-(self.moisture/100))/
                                                    (self.slurry_conc))-self.starch_dose * self.production)
            self.ids.slurry_water.text = str(self.slurry_water) + ' l/h'

            self.dilution_water = round(((self.slurry_water * self.slurry_conc) / self.final_conc)-self.slurry_water)
            self.ids.dilution_water.text = str(self.dilution_water) + ' l/h'

            self.enzyme_flow = round((((self.slurry_water * self.slurry_conc)/100)**2)*0.002 / ((self.slurry_water * self.slurry_conc)/100), 2)
            self.ids.enzyme_flow.text = str(self.enzyme_flow) + ' l/h'

            self.total_water = round((self.dilution_water*24*31)/1000 + (self.slurry_water*24*31)/1000, 2)
            self.ids.water_cons.text = str(self.total_water) + ' m3/m'

            self.total_enzyme = round((self.enzyme_flow*24*31)/1000, 2)
            self.ids.enzyme_cons.text = str(self.total_enzyme) + ' m3/m'

        except ZeroDivisionError:
            zero_division_popup.open()




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
