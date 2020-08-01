#!/usr/bin/env python
# encoding: utf-8
import curses
import npyscreen
from packaging import version


class ClustersGrid(npyscreen.GridColTitles):
    additional_x_offset = 2

    def when_cursor_moved(self):
        pass

    def custom_print_cell(self, actual_cell, cell_display_value):
        if cell_display_value =='1.0.1':
            actual_cell.color = 'DANGER'
        elif cell_display_value == '3.7.86':
            actual_cell.color = 'GOOD'
        else:
            actual_cell.color = 'DEFAULT'


class VersionSelectForm(npyscreen.Popup):
    def create(self):
        self.name = 'VersionSelectFormbla'
        # pop_x = self.grid.relx + self.grid.width//2 - pop_width//2
        # self.show_atx = 200
        # self.nextrelx = 40


class KubeApp(npyscreen.NPSAppManaged): #StandardApp):   # NPSApp):
    def do_stuff(self, pop):
        # self.version_form.display()
        # self.pop.hidden = False
        # self.pop.display()
        self.version_form.edit()

    def main(self):
        main_form = npyscreen.Form(name="Clusters Overview v0.1.0",)
        main_form.add(npyscreen.BoxTitle,
                      name="Namespace",
                      relx=2,
                      rely=2,
                      max_width=20,
                      values=[
                          'airflow-ml',
                          'analytics',
                          'cdp',
                          'datafeeds',
                          'devops',
                          'frontend',
                          'kube-system',
                          'mcd',
                          'mcd-spark',
                          'noc',
                          'recs',
                          'ssapi',
                      ],
                    )

        self.grid = main_form.add(ClustersGrid,
                                  rely=2,
                                  relx=25,
                                  # max_width=150,
                                  max_height=10,
                                  columns=6,
                                  )
        self.grid.add_handlers({curses.ascii.NL: self.do_stuff})
        self.grid.col_titles = ['Service', 'Container', 'Dev', 'Staging', 'Prod EUC', 'Prod USE']
        self.grid.values = []
        self.grid.values = [
            ['rcom-server', 'rcom-server', 'latest', '3.7.86', '3.7.86', '3.7.86'],
            ['', 'cache-updater', 'latest', '3.7.86', '3.7.86', '3.7.86'],
            ['', 'redis', '5.0.1', '5.0.1', '5.0.1', '5.0.1'],
            ['', 'lfu-redis', '5.0.1', '5.0.1', '5.0.1', '5.0.1'],
            ['user-affinity', 'user-affinity', 'latest', '3.7.86', '3.7.86', '3.7.86'],
            ['es-graphite', 'es-graphite', 'latest', '1.0.1', '1.0.1', '1.0.1'],
        ]
        pop_width = 30
        pop_x = self.grid.relx + self.grid.width//2 - pop_width//2
        pop_y = self.grid.rely + self.grid.height//2
        self.version_form = self.addForm("select-version-form", VersionSelectForm, )
        self.version_form.show_atx = self.grid.relx + self.grid.width//2 - self.version_form.columns//2
        self.version_form.show_aty = self.grid.rely + self.grid.height//2 
        self.ms = self.version_form.add(npyscreen.TitleSelectOne,
                                        max_height=4,
                                        value=[1,],
                                        name="Pick One",
                                        values=["3.7.86", "3.7.87", "3.7.88"],
                                        scroll_exit=True
                                        )

        main_form.edit()


if __name__ == "__main__":
    App = KubeApp()
    App.run()
