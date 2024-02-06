from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
from kivymd.app import MDApp
from kivymd.uix.datatables import MDDataTable
from kivy.metrics import dp
import zoo_data as zoo

check_indexes = []
columns_dict = {'animals': [
                ("[font=Comic][color=#cf1d02]N[/color][/font]", dp(17)),
                ("[font=Comic][color=#cf7d02]вид[/color][/font]", dp(18)),
                ("[font=Comic][color=#cbcf02]имя[/color][/font]", dp(18)),
                ("[font=Comic][color=#02cf5b]день рождения[/color][/font]", dp(26)),
                ("[font=Comic][color=#024dcf]пол[/color][/font]", dp(13)),
                ("[font=Comic][color=#8702cf]диета[/color][/font]", dp(13)),
                ("[font=Comic][color=#cb02cf]среда обитания[/color][/font]", dp(25)),
                ("[font=Comic][color=#cb02cf]надз.[/color][/font]", dp(12)),
                ("[font=Comic][color=#cb02cf]вет.[/color][/font]", dp(12))],
                'diets': [
                ("[font=Comic][color=#cf1d02]N[/color][/font]", dp(40)),
                ("[font=Comic][color=#cb02cf]название[/color][/font]", dp(60)),
                ("[font=Comic][color=#cb02cf]тип[/color][/font]", dp(60))],
                'birds': [
                ("[font=Comic][color=#cf1d02]N[/color][/font]", dp(17)),
                ("[font=Comic][color=#cf7d02]вид[/color][/font]", dp(22)),
                ("[font=Comic][color=#cbcf02]имя[/color][/font]", dp(22)),
                ("[font=Comic][color=#02cf5b]место зимовки[/color][/font]", dp(29)),
                ("[font=Comic][color=#024dcf]дата улета[/color][/font]", dp(36)),
                ("[font=Comic][color=#8702cf]дата прилета[/color][/font]", dp(36))],
                'reptiles': [
                ("[font=Comic][color=#cf1d02]N[/color][/font]", dp(21), None, "Custom tooltip"),
                ("[font=Comic][color=#cb02cf]вид[/color][/font]", dp(30), None, "Custom tooltip"),
                ("[font=Comic][color=#cb02cf]имя[/color][/font]", dp(30), None, "Custom tooltip"),
                ("[font=Comic][color=#cb02cf]температура[/color][/font]", dp(30), None, "Custom tooltip"),
                ("[font=Comic][color=#cb02cf]время спячки (дни)[/color][/font]", dp(35), None, "Custom tooltip")],
                'environments': [
                ("[font=Comic][color=#cb02cf]название[/color][/font]", dp(60), None, "Custom tooltip"),
                ("[font=Comic][color=#cb02cf]тип[/color][/font]", dp(120), None, "Custom tooltip")],
                'workers': [
                ("[font=Comic][color=#cf1d02]N[/color][/font]", dp(17), None, "Custom tooltip"),
                ("[font=Comic][color=#cf7d02]должность[/color][/font]", dp(22), None, "Custom tooltip"),
                ("[font=Comic][color=#cbcf02]имя[/color][/font]", dp(22), None, "Custom tooltip"),
                ("[font=Comic][color=#02cf5b]дата рождения[/color][/font]", dp(26), None, "Custom tooltip"),
                ("[font=Comic][color=#024dcf]номер телефона[/color][/font]", dp(25), None, "Custom tooltip"),
                ("[font=Comic][color=#8702cf]семейное положение[/color][/font]", dp(22), None, "Custom tooltip"),
                ("[font=Comic][color=#cb02cf]супруг[/color][/font]", dp(23), None, "Custom tooltip")],
                'couples': [
                ("[font=Comic][color=#cf1d02]N[/color][/font]", dp(19), None, "Custom tooltip"),
                ("[font=Comic][color=#cf7d02]должность[/color][/font]", dp(24), None, "Custom tooltip"),
                ("[font=Comic][color=#cbcf02]имя[/color][/font]", dp(22), None, "Custom tooltip"),
                ("[font=Comic][color=#02cf5b] [/color][/font]", dp(21), None, "Custom tooltip"),
                ("[font=Comic][color=#024dcf]N[/color][/font]", dp(19), None, "Custom tooltip"),
                ("[font=Comic][color=#8702cf]должность[/color][/font]", dp(24), None, "Custom tooltip"),
                ("[font=Comic][color=#cb02cf]имя[/color][/font]", dp(22), None, "Custom tooltip")]}

class AddAnimalPopup(Popup):
    def add_button(self):
        vet = self.ids.vet.text
        supervisor = self.ids.supervisor.text
        info = [str(zoo.get_last('animals')), f"'{self.ids.species.text}'", f"'{self.ids.name.text}'", f"'{self.ids.birth_date.text}'", f"'{self.ids.sex.text}'",
                 self.ids.diet.text, f"'{self.ids.environment.text}'", supervisor, vet]
        if not(zoo.exists('diets', 'n', self.ids.diet.text)):
            self.show_doesnt_exist('нет такой диеты')
        elif not(zoo.exists('environments', 'name', f"'{self.ids.environment.text}'")):
            self.show_doesnt_exist('нет такой среды')
        elif not(zoo.exists('workers', 'n', self.ids.vet.text)) or not(zoo.exists('workers', 'n', self.ids.supervisor.text)):
            self.show_doesnt_exist('вы ввели несуществующего сотрудника')
        elif zoo.get_checked('workers', 'n', self.ids.vet.text)[1] != 'в':
            self.show_doesnt_exist('мы не дадим вам назначить\nнадзирателя ветеринаром')
        elif zoo.get_checked('workers', 'n', self.ids.supervisor.text)[1]  != 'н':
            self.show_doesnt_exist('мы не дадим вам назначить\nветеринара надзирателем')
        else:
            zoo.add_row('animals', info)
            self.dismiss()
            

    def show_doesnt_exist(self, text):
        doesnt_exist = ErrorPopup()
        doesnt_exist.ids.error_text.text = text
        doesnt_exist.open()

class AddBirdPopup(Popup):
    def add_button(self):
        info = [f"{self.ids.n.text}", f"'{self.ids.winter.text}'", f"'{zoo.add_year(self.ids.departure.text)}'",
                 f"'{zoo.add_year(self.ids.arrival.text)}'"]
        for i in range(1, len(info)):
            if info[i] == f"''" or info[i] == f"'.2000'": info[i] = 'null'
        if not(zoo.exists('animals', 'n', self.ids.n.text)):
            self.show_doesnt_exist()
        else:
            zoo.add_row('birds', info)
            self.dismiss()

    def show_doesnt_exist(self):
        doesnt_exist = ErrorPopup()
        doesnt_exist.ids.error_text.text = 'нет такой птицы в зоопарке'
        doesnt_exist.open()

class AddReptilePopup(Popup):
    def add_button(self):
        info = [f"{self.ids.n.text}", f"'{self.ids.temperature.text}'", f"'{self.ids.hibernation_days.text}'"]
        if not(zoo.exists('animals', 'n', self.ids.n.text)):
            self.show_doesnt_exist()
        else:
            zoo.add_row('reptiles', info)
            self.dismiss()

    def show_doesnt_exist(self):
        doesnt_exist = ErrorPopup()
        doesnt_exist.ids.error_text.text = 'нет такой рептилии в зоопарке'
        doesnt_exist.open()

class AddEnvironmentPopup(Popup):
    def add_button(self):
        info = [f"'{self.ids.name.text}'", f"'{self.ids.description.text}'"]
        zoo.add_row('environments', info)
        self.dismiss()

class AddDietPopup(Popup):
    def add_button(self):
        info = [str(zoo.get_last('diets')), f"'{self.ids.name.text}'", f"'{self.ids.type.text}'"]
        zoo.add_row('diets', info)

class AddWorkerPopup(Popup):
    def add_button(self):
        marriage = self.ids.marriage.text
        if marriage == '': marriage = 'null'
        info = [str(zoo.get_last('workers')), f"'{self.ids.prof.text}'", f"'{self.ids.name.text}'", f"'{self.ids.birth_date.text}'",
                 f"'{self.ids.phone_number.text}'", f"'{self.ids.family_status.text}'", marriage]
        zoo.add_row('workers', info)
        self.dismiss()

class AddCouplePopup(Popup):
    def add_button(self):
        info = [f"'{self.ids.n_first.text}'", f"'{self.ids.n_second.text}'"]
        if not(zoo.exists('workers', 'n', self.ids.n_first.text)) or not(zoo.exists('workers', 'n', self.ids.n_second.text)):
            self.show_doesnt_exist()
        else:
            zoo.add_couple(self.ids.n_first.text, self.ids.n_second.text)
            self.dismiss()

    def show_doesnt_exist(self):
        doesnt_exist = ErrorPopup()
        doesnt_exist.ids.error_text.text = 'вы ввели несуществуещего рабочего'
        doesnt_exist.ids.button.text = 'а, ой'
        doesnt_exist.open()

class DeleteAnimalsPopup(Popup):
    def delete_button(self):
        global check_indexes
        if len(check_indexes) > 0:
            zoo.delete_rows('birds', 'N', check_indexes)
            zoo.delete_rows('reptiles', 'N', check_indexes)
            zoo.delete_rows('animals', 'N', check_indexes)
            check_indexes = []

class DeleteDietPopup(Popup):
    def delete_button(self):
        global check_indexes
        if len(check_indexes) > 0:
            eaters = zoo.get_eaters(check_indexes)
            if len(eaters) > 0:
                zoo.delete_rows('birds', 'N', [str(eater) for eater in eaters])
                zoo.delete_rows('reptiles', 'N', [str(eater) for eater in eaters])
                zoo.delete_rows('animals', 'n', [str(eater) for eater in eaters])
                zoo.delete_rows('diets', 'N', check_indexes)
            check_indexes = []

class DeleteBirdsPopup(Popup):
    def delete_button(self):
        global check_indexes
        if len(check_indexes) > 0:
            zoo.delete_rows('birds', 'N', check_indexes)
            check_indexes = []

class DeleteReptilesPopup(Popup):
    def delete_button(self):
        global check_indexes
        if len(check_indexes) > 0:
            zoo.delete_rows('reptiles', 'N', check_indexes)
            check_indexes = []

class DeleteEnvironmentsPopup(Popup):
    def delete_button(self):
        global check_indexes
        if len(check_indexes) > 0:
            indwellers = zoo.get_indwellers(check_indexes)
            if len(indwellers) > 0:
                zoo.delete_rows('birds', 'N', [str(indweller) for indweller in indwellers])
                zoo.delete_rows('reptiles', 'N', [str(indweller) for indweller in indwellers])
                zoo.delete_rows('animals', 'n', [str(indweller) for indweller in indwellers])
                zoo.delete_rows('environments', 'name', [f"'{index}'" for index in check_indexes])
            check_indexes = []

class DeleteWorkerPopup(Popup):
    def delete_button(self):
        global check_indexes
        if len(check_indexes) > 0:
            zoo.delete_rows('workers', 'N', check_indexes)
            check_indexes = []

class DivorceCouplePopup(Popup):
    def divorce_button(self):
        global check_indexes
        if len(check_indexes) > 0:
            for checked in check_indexes:
                row = zoo.get_checked_couple(checked)
                n_first, n_second = row[0], row[1]
                zoo.divorce_couple(n_first, n_second)
            check_indexes = []

class AlterAnimalPopup(Popup):
    def alter_button(self):
        global check_indexes
        if not(zoo.exists('diets', 'n', self.ids.diet.text)):
            self.show_doesnt_exist('нет такой диеты')
        elif not(zoo.exists('environments', 'name', f"'{self.ids.environment.text}'")):
            self.show_doesnt_exist('нет такой среды')
        elif not(zoo.exists('workers', 'n', self.ids.vet.text)) or not(zoo.exists('workers', 'n', self.ids.supervisor.text)):
            self.show_doesnt_exist('вы ввели несуществующего сотрудника')
        elif zoo.get_checked('workers', 'n', self.ids.vet.text)[1] != 'в':
            self.show_doesnt_exist('мы не дадим вам назначить\nнадзирателя внтеринаром')
        elif zoo.get_checked('workers', 'n', self.ids.supervisor.text)[1]  != 'н':
            self.show_doesnt_exist('мы не дадим вам назначить\nветеринара надзирателем')
        else:
            new_info = f"species = '{self.ids.species.text}', name = '{self.ids.name.text}', birth_date = '{self.ids.birth_date.text}',"
            new_info += f"sex = '{self.ids.sex.text}', diet = {self.ids.diet.text}, environment = '{self.ids.environment.text}',"
            new_info += f"superviser =  {self.ids.supervisor.text}, vet = {self.ids.vet.text}" 
            zoo.alter_row('animals', 'N', check_indexes[0], new_info)
            self.dismiss()
            check_indexes = []
        
    def show_doesnt_exist(self, text):
        doesnt_exist = ErrorPopup()
        doesnt_exist.ids.error_text.text = text
        doesnt_exist.open()
        
class AlterDietPopup(Popup):
    def alter_button(self):
        global check_indexes
        new_info = f"name = '{self.ids.name.text}', type = '{self.ids.type.text}'" 
        zoo.alter_row('diets', 'N', check_indexes[0], new_info)
        check_indexes = []

class AlterBirdPopup(Popup):
    def alter_button(self):
        global check_indexes
        departure = f"'{zoo.add_year(self.ids.departure.text)}'"
        if departure == f"'null'": departure = 'null'
        arrival = f"'{zoo.add_year(self.ids.arrival.text)}'"
        if arrival == f"'null'": arrival = 'null'
        new_info = f"wintering_place = '{self.ids.winter.text}', departure = {departure}, arrival = {arrival}" 
        zoo.alter_row('birds', 'N', check_indexes[0], new_info)
        check_indexes = []

class AlterReptilePopup(Popup):
    def alter_button(self):
        global check_indexes
        new_info = f"hibernation_days = '{self.ids.hibernation_days.text}', temperature = '{self.ids.temperature.text}'" 
        zoo.alter_row('reptiles', 'N', check_indexes[0], new_info)
        check_indexes = []

class AlterEnvironmentPopup(Popup):
    def alter_button(self):
        global check_indexes
        new_info = f"description = '{self.ids.description.text}'" 
        zoo.alter_row('environments', 'name', f"'{check_indexes[0]}'", new_info)
        check_indexes = []

class AlterWorkerPopup(Popup):
    def alter_button(self):
        global check_indexes
        marriage = self.ids.marriage.text
        if marriage == '' or marriage == 'None': marriage = 'null'
        new_info = f"prof = '{self.ids.prof.text}', name = '{self.ids.name.text}', birth_date = '{self.ids.birth_date.text}',"
        new_info += f"phone_number = '{self.ids.phone_number.text}', family_status = '{self.ids.family_status.text}',"
        new_info += f"marriage =  {marriage}" 
        zoo.alter_row('workers', 'N', check_indexes[0], new_info)
        check_indexes = []

class AlterCouplePopup(Popup):
    def alter_button(self):
        global check_indexes
        prev_first, prev_second = zoo.get_checked_couple(check_indexes[0])
        zoo.divorce_couple(prev_first, prev_second)
        new_first, new_second  = self.ids.n_first.text, self.ids.n_second.text 
        zoo.add_couple(new_first, new_second)
        check_indexes = []
        
class ErrorPopup(Popup):
    pass

class MainWidget(Screen):
    pass

class ColorfulLabel(Label):
    pass

class WindowManager(ScreenManager):
    pass

class MenuScreen(Screen):
    pass

class DietsScreen(Screen):
    def search(self):
        searched = self.ids.search.text.split()
        if len(searched) == 1 and searched[0].isdigit():
            found = zoo.search('diets', searched, ['N'])
        elif len(searched) > 0 and len(searched) < 3:
            found = zoo.search('diets', list(map(lambda x: f"'{x}'", searched)), ['name', 'type'])
        else:
            found = zoo.get_table('diets')
        return found
    
    def show_add_popup(self):
        add_popup = AddDietPopup()
        add_popup.open()

    def show_delete_popup(self):
        delete_popup = DeleteDietPopup()
        if len(zoo.get_eaters(check_indexes)) > 0:
            delete_popup.ids.label.text = '\nкто-то питается этой едой\nэти животные умрут с голода\n'
        delete_popup.open()
    
    def show_multiple_alter(self):
        multiple_alter = ErrorPopup()
        multiple_alter.open()

    def show_alter_popup(self):
        global check_indexes
        info = zoo.get_checked('diets', 'N', check_indexes[0])
        alter_popup = AlterDietPopup()
        alter_popup.ids.name.text = info[1]
        alter_popup.ids.type.text = info[2]
        alter_popup.open()

    def alter(self):
        global check_indexes
        if len(check_indexes) > 1:
            self.show_multiple_alter()
        elif len(check_indexes) == 1:
            self.show_alter_popup()

class AnimalsScreen(Screen):
    def show_animal_popup(self):
        add_popup = AddAnimalPopup()
        add_popup.open()

    def show_delete_popup(self):
        delete_popup = DeleteAnimalsPopup()
        delete_popup.open()
    
    def show_multiple_alter(self):
        multiple_alter = ErrorPopup()
        multiple_alter.open()

    def search(self):
        searched = self.ids.search.text.split()
        if len(searched) == 1 and searched[0].isdigit():
            found = zoo.search('animals', searched, ['N'])
        elif len(searched) > 0 and len(searched) < 3:
            found = zoo.search('animals', list(map(lambda x: f"'{x}'", searched)), ['species', 'name'])
        else:
            found = zoo.get_table('animals')
        return found

    def show_alter_popup(self):
        global check_indexes
        info = zoo.get_checked('animals', 'N', check_indexes[0])
        alter_popup = AlterAnimalPopup()
        alter_popup.ids.species.text = info[1]
        alter_popup.ids.name.text = info[2]
        alter_popup.ids.birth_date.text = info[3]
        alter_popup.ids.sex.text = info[4]
        alter_popup.ids.diet.text = str(info[5])
        alter_popup.ids.environment.text = info[6]
        alter_popup.ids.supervisor.text = str(info[7])
        alter_popup.ids.vet.text = str(info[8])
        alter_popup.open()

    def alter(self):
        global check_indexes
        if len(check_indexes) > 1:
            self.show_multiple_alter()
        elif len(check_indexes) == 1:
            self.show_alter_popup()

class BirdsScreen(Screen):
    def show_add_popup(self):
        add_popup = AddBirdPopup()
        add_popup.open()

    def show_delete_popup(self):
        delete_popup = DeleteBirdsPopup()
        delete_popup.open()
    
    def show_multiple_alter(self):
        multiple_alter = ErrorPopup()
        multiple_alter.open()

    def search(self):
        searched = self.ids.search.text.split()
        if len(searched) == 1 and searched[0].isdigit():
            found = zoo.search('birds', searched, ['N'])
        elif len(searched) > 0 and len(searched) < 3:
            found = zoo.search('birds', list(map(lambda x: f"'{x}'", searched)), ['species', 'name'])
        else:
            found = zoo.get_table('birds')
        return found

    def show_alter_popup(self):
        global check_indexes
        info = zoo.get_checked('birds', 'N', check_indexes[0])
        alter_popup = AlterBirdPopup()
        alter_popup.ids.winter.text = str(info[3])
        alter_popup.ids.departure.text = info[4]
        alter_popup.ids.arrival.text = info[5]
        alter_popup.open()

    def alter(self):
        global check_indexes
        if len(check_indexes) > 1:
            self.show_multiple_alter()
        elif len(check_indexes) == 1:
            self.show_alter_popup()

class ReptilesScreen(Screen):
    def show_add_popup(self):
        add_popup = AddReptilePopup()
        add_popup.open()

    def show_delete_popup(self):
        delete_popup = DeleteReptilesPopup()
        delete_popup.open()
    
    def show_multiple_alter(self):
        multiple_alter = ErrorPopup()
        multiple_alter.open()

    def search(self):
        searched = self.ids.search.text.split()
        if len(searched) == 1 and searched[0].isdigit():
            found = zoo.search('reptiles', searched, ['N'])
        elif len(searched) > 0 and len(searched) < 3:
            found = zoo.search('reptiles', list(map(lambda x: f"'{x}'", searched)), ['species', 'name'])
        else:
            found = zoo.get_table('reptiles')
        return found

    def show_alter_popup(self):
        global check_indexes
        info = zoo.get_checked('reptiles', 'N', check_indexes[0])
        alter_popup = AlterReptilePopup()
        alter_popup.ids.temperature.text = str(info[3])
        alter_popup.ids.hibernation_days.text = str(info[4])
        alter_popup.open()

    def alter(self):
        global check_indexes
        if len(check_indexes) > 1:
            self.show_multiple_alter()
        elif len(check_indexes) == 1:
            self.show_alter_popup()

class EnvironmentsScreen(Screen):
    def show_add_popup(self):
        add_popup = AddEnvironmentPopup()
        add_popup.open()

    def show_delete_popup(self):
        delete_popup = DeleteEnvironmentsPopup()
        if len(zoo.get_indwellers(check_indexes)) > 0:
            delete_popup.ids.label.text = 'тут кто-живет, при удалении этой\nсреды эти животные будут уничтожены'
        delete_popup.open()
    
    def show_multiple_alter(self):
        multiple_alter = ErrorPopup()
        multiple_alter.open()

    def search(self):
        searched = self.ids.search.text
        if searched != '':
            found = zoo.search('environments', [f"'{searched}'"], ['name'])
        else:
            found = zoo.get_table('environments')
        return found

    def show_alter_popup(self):
        global check_indexes
        info = zoo.get_checked('environments', 'name', f"'{check_indexes[0]}'")
        alter_popup = AlterEnvironmentPopup()
        alter_popup.ids.description.text = info[1]
        alter_popup.open()

    def alter(self):
        global check_indexes
        if len(check_indexes) > 1:
            self.show_multiple_alter()
        elif len(check_indexes) == 1:
            self.show_alter_popup()

class WorkersScreen(Screen):
    def show_add_popup(self):
        add_popup = AddWorkerPopup()
        add_popup.open()

    def show_delete_popup(self):
        delete_popup = DeleteWorkerPopup()
        delete_popup.open()
    
    def show_multiple_alter(self):
        multiple_alter = ErrorPopup()
        multiple_alter.open()

    def search(self):
        searched = self.ids.search.text.split()
        if len(searched) == 1 and searched[0].isdigit():
            found = zoo.search('workers', searched, ['N'])
        elif len(searched) > 0 and len(searched) < 3:
            found = zoo.search('workers', list(map(lambda x: f"'{x}'", searched)), ['prof', 'name'])
        else:
            found = zoo.get_table('workers')
        return found
    
    def show_alter_popup(self):
        global check_indexes
        info = zoo.get_checked('workers', 'N', check_indexes[0])
        alter_popup = AlterWorkerPopup()
        alter_popup.ids.prof.text = info[1]
        alter_popup.ids.name.text = info[2]
        alter_popup.ids.birth_date.text = str(info[3])
        alter_popup.ids.phone_number.text = info[4]
        alter_popup.ids.family_status.text = info[5]
        alter_popup.ids.marriage.text = str(info[6])
        alter_popup.open()
    
    def alter(self):
        global check_indexes
        if len(check_indexes) > 1:
            self.show_multiple_alter()
        elif len(check_indexes) == 1:
            self.show_alter_popup()

class CouplesScreen(Screen):
    def show_add_popup(self):
        add_popup = AddCouplePopup()
        add_popup.open()

    def show_divorce_popup(self):
        delete_popup = DivorceCouplePopup()
        delete_popup.open()
    
    def show_multiple_alter(self):
        multiple_alter = ErrorPopup()
        multiple_alter.open()

    def search(self):
        searched = self.ids.search.text.split()
        if len(searched) == 1 and searched[0].isdigit():
            found = zoo.search('couples', searched, ['f_n']) + zoo.search('couples', searched, ['s_n'])
        elif len(searched) > 0 and len(searched) < 3:
            found = zoo.search('couples', list(map(lambda x: f"'{x}'", searched)), ['s_prof', 's_name'])
            found += zoo.search('couples', list(map(lambda x: f"'{x}'", searched)), ['f_prof', 'f_name'])
        else:
            found = zoo.get_table('couples')
        return found

    def show_alter_popup(self):
        global check_indexes
        info = zoo.get_checked_couple(check_indexes[0])
        alter_popup = AlterCouplePopup()
        alter_popup.ids.n_first.text = str(info[0])
        alter_popup.ids.n_second.text = str(info[1])
        alter_popup.open()

    def alter(self):
        global check_indexes
        if len(check_indexes) > 1:
            self.show_multiple_alter()
        elif len(check_indexes) == 1:
            self.show_alter_popup()
    
class MainApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.table = None

    def build(self):
        super(MainApp,self).__init__()
        self.title = "MyApp"
        self.load_kv("struct.kv")
        return WindowManager()
    
    def change_screen(self, screen: str):
        self.root.current = screen

    def dismiss_table(self):
        self.table.close()

    def load_table(self, table_name, content = None):
        global check_indexes
        if check_indexes == []:
            if content == None: content = zoo.get_table(table_name)
            self.table = MDDataTable(
            use_pagination=True,
            
            rows_num = 200,
            elevation=7,
            check=True,
            column_data = columns_dict[table_name],
            row_data = content,)
            self.table.bind(on_check_press=self.checked)
            load_string = f'self.root.ids.{table_name}_screen.ids.data_layout.add_widget(self.table)'
            eval(load_string)

    def show_error(self, error_text):
        error_popup = ErrorPopup()
        error_popup.ids.error_text = error_text
        error_popup.open()


    def checked(self, instance_table, current_row):
        global check_indexes
        index = current_row[0]
        if index in check_indexes:
            i = 0
            while i < len(check_indexes):
                if check_indexes[i] == index: check_indexes.pop(i)
                else: i+=1
        else:
            check_indexes.append(index)


if __name__ == '__main__':
    MainApp().run() 