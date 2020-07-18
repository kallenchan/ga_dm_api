import webbrowser
import pandas as pd
import json
import requests
import numpy as np

def get_all_lobbies():
    response=requests.get("https://aoe2.net/api/lobbies?game=aoe2hd&language=en")
    lobbies=pd.json_normalize(response.json())
    ga_dm_lobbies=lobbies[['lobby_id','name','game_type','num_players','players','num_slots']]
    return ga_dm_lobbies

# Return All Lobbies
all_lobbies=get_all_lobbies()
lobby_ids=all_lobbies.loc[1:3,'lobby_id']

# #Accept Input
# selected_game=input("Choose a game to join")
# steam_protocol="steam://joinlobby/221380/{}".format(lobby_ids.to_dict()[float(selected_game)])
# webbrowser.open_new(steam_protocol)
# print("Joining Game")

# print(all_lobbies)

# for index,row in all_lobbies.iterrows():
#     # print(index)
#     # print(row)
#     print(row['num_players'])


import wx

class game_Panel(wx.Panel):
    def __init__(self,parent):
        wx.Panel.__init__(self,parent)

        main_sizer=wx.BoxSizer(wx.VERTICAL)
        self.row_obj_dict={}
        self.list_ctrl=wx.ListCtrl(
            self,size=(1000,100),
            style=wx.LC_REPORT | wx.BORDER_SUNKEN
        )

        #Add Columns
        self.list_ctrl.InsertColumn(0,'Name',width=150)
        self.list_ctrl.InsertColumn(1,'Slots',width=50)
        self.list_ctrl.InsertColumn(2,'Host',width=200)
        self.list_ctrl.InsertColumn(3,'Players',width=100)

        self.on_press_refresh()

        # Buttons 
        grid=wx.GridSizer(2,2,5)

        refresh_button=wx.Button(self,label="Refresh",pos=(20,150),size=(80,40))
        join_button=wx.Button(self,label="Join",pos=(175,150),size=(80,40))
        
        self.Bind(wx.EVT_BUTTON,self.on_press_refresh,refresh_button)
        self.Bind(wx.EVT_BUTTON,self.on_press_join,join_button)

        self.SetSizer(main_sizer)
        self.Fit()
        self.Show()

    def on_press_refresh(self,event=None):

        #Delete All Items
        self.list_ctrl.DeleteAllItems()

        #Add Items
        for index,lobby in all_lobbies.iterrows():
            #Name
            self.list_ctrl.InsertItem(index,lobby['name'])

            #Slots
            self.list_ctrl.SetItem(index,1,"{}/{}".format(
                str(lobby['num_players']),
                str(lobby['num_slots'])
            ))

            #Players
            df_players=pd.DataFrame(lobby.players)
            try:
                self.list_ctrl.SetItem(index,2,'{} ({})'.format(
                    df_players.loc[0]['name'],
                    str(int(df_players.loc[0]['rating']))
                ))
            except (TypeError,ValueError):
                self.list_ctrl.SetItem(index,2,
                    df_players.loc[0]['name']
                )

    def on_press_join(self,event):
        print("Joining Lobby")

class game_Frame(wx.Frame):
    def __init__(self):
        super().__init__(parent=None,
                        title='GA DM')
        self.panel=game_Panel(self)
        self.Show()

app = wx.App(False)
frame = game_Frame()
panel = game_Panel(frame)
frame.Show()
app.MainLoop()

# class ExamplePanel(wx.Panel):
#     def __init__(self, parent):
#         wx.Panel.__init__(self, parent)

#         # create some sizers
#         mainSizer = wx.BoxSizer(wx.VERTICAL)
#         grid = wx.GridBagSizer(hgap=5, vgap=5)
#         hSizer = wx.BoxSizer(wx.HORIZONTAL)

#         self.quote = wx.StaticText(self, label="Your quote: ")
#         grid.Add(self.quote, pos=(0,0))

#         # A multiline TextCtrl - This is here to show how the events work in this program, don't pay too much attention to it
#         self.logger = wx.TextCtrl(self, size=(200,300), style=wx.TE_MULTILINE | wx.TE_READONLY)

#         # A button
#         self.button =wx.Button(self, label="Save")
#         self.Bind(wx.EVT_BUTTON, self.OnClick,self.button)

#         # the edit control - one line version.
#         self.lblname = wx.StaticText(self, label="Your name :")
#         grid.Add(self.lblname, pos=(1,0))
#         self.editname = wx.TextCtrl(self, value="Enter here your name", size=(140,-1))
#         grid.Add(self.editname, pos=(1,1))
#         self.Bind(wx.EVT_TEXT, self.EvtText, self.editname)
#         self.Bind(wx.EVT_CHAR, self.EvtChar, self.editname)

#         # the combobox Control
#         self.sampleList = ['friends', 'advertising', 'web search', 'Yellow Pages']
#         self.lblhear = wx.StaticText(self, label="How did you hear from us ?")
#         grid.Add(self.lblhear, pos=(3,0))
#         self.edithear = wx.ComboBox(self, size=(95, -1), choices=self.sampleList, style=wx.CB_DROPDOWN)
#         grid.Add(self.edithear, pos=(3,1))
#         self.Bind(wx.EVT_COMBOBOX, self.EvtComboBox, self.edithear)
#         self.Bind(wx.EVT_TEXT, self.EvtText,self.edithear)

#         # add a spacer to the sizer
#         grid.Add((10, 40), pos=(2,0))

#         # Checkbox
#         self.insure = wx.CheckBox(self, label="Do you want Insured Shipment ?")
#         grid.Add(self.insure, pos=(4,0), span=(1,2), flag=wx.BOTTOM, border=5)
#         self.Bind(wx.EVT_CHECKBOX, self.EvtCheckBox, self.insure)

#         # Radio Boxes
#         radioList = ['blue', 'red', 'yellow', 'orange', 'green', 'purple', 'navy blue', 'black', 'gray']
#         rb = wx.RadioBox(self, label="What color would you like ?", pos=(20, 210), choices=radioList,  majorDimension=3,
#                          style=wx.RA_SPECIFY_COLS)
#         grid.Add(rb, pos=(5,0), span=(1,2))
#         self.Bind(wx.EVT_RADIOBOX, self.EvtRadioBox, rb)

#         hSizer.Add(grid, 0, wx.ALL, 5)
#         hSizer.Add(self.logger)
#         mainSizer.Add(hSizer, 0, wx.ALL, 5)
#         mainSizer.Add(self.button, 0, wx.CENTER)
#         self.SetSizerAndFit(mainSizer)

#     def EvtRadioBox(self, event):
#         self.logger.AppendText('EvtRadioBox: %d\n' % event.GetInt())
#     def EvtComboBox(self, event):
#         self.logger.AppendText('EvtComboBox: %s\n' % event.GetString())
#     def OnClick(self,event):
#         self.logger.AppendText(" Click on object with Id %d\n" %event.GetId())
#     def EvtText(self, event):
#         self.logger.AppendText('EvtText: %s\n' % event.GetString())
#     def EvtChar(self, event):
#         self.logger.AppendText('EvtChar: %d\n' % event.GetKeyCode())
#         event.Skip()
#     def EvtCheckBox(self, event):
#         self.logger.AppendText('EvtCheckBox: %d\n' % event.Checked())       

# app = wx.App(False)
# frame = wx.Frame(None)
# panel = ExamplePanel(frame)
# frame.Show()
# app.MainLoop()