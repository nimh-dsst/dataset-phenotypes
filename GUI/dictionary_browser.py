import PySimpleGUI as sg
import json
import pandas as pd

"""
    Database GUI Browser
    BrainHack 2022 NIH
    Author: Roberto Salamanca-Giron
    Github: RobertoFelipeSG
    e-mail: robertofelipe.sg@gmail.com
    V.1.0.
"""

with open('phenotype/dictionary.json') as f:
    js = json.load(f)
print(type(js))
len(js.keys())

use_custom_titlebar = True if sg.running_trinket() else False

def make_window(theme=None):

    NAME_SIZE = 23

    def name(name):
        dots = NAME_SIZE-len(name)-2
        return sg.Text(name + ' ' + '•'*dots, size=(NAME_SIZE,1), 
                       justification='c',pad=(0,0), font='Courier 10')

    sg.theme('DarkBlue3')    
    
    treedata = sg.TreeData()
    #Insert(parent_key, key, display_text, values)

    for k, val in enumerate(js.keys()) :
        # print(val)
        if 'Levels' in js[val]:            
            treedata.Insert('', val, val, js[val]['Levels'])
            for le in js[val]['Levels']:
                treedata.Insert(val, val, js[val]['Levels'], js[val]['Levels'])
        else:
            treedata.Insert('', val, val, '')
            
    def search(treedata, sub_string):
        return [key for key in js.keys()]#treedata.tree_dict if sub_string in key]


    layout = [[name('HCP'),
                
               sg.Tree(treedata, 
                headings=['Explanation'],#,'Levels'],
                auto_size_columns=False,
                select_mode=sg.TABLE_SELECT_MODE_EXTENDED,
                num_rows=len(js.keys()),
                # col0_width=40,
                key='-TREE-',
                show_expanded=True,
                enable_events=True,
                expand_x=True,
                expand_y=True,),
               
                [name('Listbox'),
                 sg.Listbox(['HCP', 'DB2', 'DB3', 'DB4'],
                            no_scrollbar=True,
                            s=(15,4))],

                
               [sg.Text('Search'), 
                sg.Input(size=(30,1), 
                key='-FILTER-',
                enable_events=True)],
                
               [sg.Button('Search')]
             ]]

    window = sg.Window('The PySimpleGUI Element List', layout, finalize=True, 
                       right_click_menu=sg.MENU_RIGHT_CLICK_EDITME_VER_EXIT, keep_on_top=True,
                       use_custom_titlebar=use_custom_titlebar, size=(1080, 720))

    return window


window = make_window()

while True:
    event, values = window.read()
    # sg.Print(event, values)
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
        
    if event == '-TREE-':
        selected_row = values['-TREE-'][0]
        print(selected_row)
              
    # elif event == '-LOAD-':
    #     key = where()
    #     node = treedata.tree_dict[key]
    #     parent_node = treedata.tree_dict[node.parent]
    #     index = parent_node.children.index(node)
    #     tree.update(values=treedata)
    #     print(node, parent_node, index)      

    elif event =='-FILTER-': 
        new_list = [i for i in js.keys() if values['-FILTER-'].lower() in i.lower()]
        print(new_list)

window.close()
