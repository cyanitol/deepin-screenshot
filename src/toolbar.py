#!/usr/bin/python
#-*- coding:utf-8 -*-

# Copyright (C) 2011 ~ 2012 Deepin, Inc.
#               2011 ~ 2012 Long Changjin
# 
# Author:     Long Changjin <admin@longchangjin.cn>
# Maintainer: Long Changjin <admin@longchangjin.cn>
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from theme import app_theme
from dtk.ui.button import ImageButton, ToggleButton
from dtk.ui.window import Window
#from dtk.ui.line import VSeparator
from dtk.ui.label import Label
#from dtk.ui.box import EventBox
from dtk.ui.color_selection import ColorSelectDialog
#from dtk.ui.dialog import SaveFileDialog
from dtk.ui.spin import SpinBox
import dtk.ui.constant
from lang import _
import utils
import gtk
from constant import *
from _share.config import OperateConfig


class Toolbar():
    ''' Toolbar window'''
    def __init__(self, parent=None, screenshot=None):
        self.screenshot = screenshot
        self.win = screenshot.window
        self.__config = OperateConfig()

        toolbar_padding_x = 15
        toolbar_padding_y = 5
        toolbar_icon_width = toolbar_icon_height = 28
        toolbar_icon_num = 10
        #self.widht = 290
        self.height = toolbar_icon_height + toolbar_padding_y * 2
        self.window = Window(window_type=gtk.WINDOW_POPUP, shadow_visible=False)
        self.window.set_keep_above(True)
        self.window.set_decorated(False)
        self.window.set_transient_for(parent)
        #self.window.connect("size-allocate", lambda w, a: updateShape(w, a, 2))
        #self.window.connect("expose-event", lambda w, e: exposeBackground(w, e, appTheme.getDynamicPixbuf("bg.png")))

        vbox = gtk.VBox(False, 0)
        self.toolbox = gtk.HBox(False, 2)
        #self.window.window_frame.pack_start(self.toolbox)
        self.window.window_shadow.remove(self.window.window_frame)
        self.window.window_shadow.add(self.toolbox)
        self.window.remove(self.window.window_shadow)
        vbox.pack_start(self.window.window_shadow)
        self.window.add(vbox)
        self.window.window_shadow.set(0.5, 0.5, 0, 0)
        self.window.window_shadow.set_padding(toolbar_padding_y, toolbar_padding_y, toolbar_padding_x, toolbar_padding_x)

        self._toggle_buton_list = []
        self.create_toggle_button("rect", ACTION_RECTANGLE, _("Tip draw rectangle"))
        self.create_toggle_button("ellipse", ACTION_ELLIPSE, _("Tip draw ellipse"))
        self.create_toggle_button("arrow",ACTION_ARROW, _("Tip draw arrow"))
        self.create_toggle_button("line",ACTION_LINE, _("Tip draw line"))
        self.create_toggle_button("text",ACTION_TEXT, _("Tip draw Text"))

        button = ImageButton(
            app_theme.get_pixbuf("action/sep.png"),
            app_theme.get_pixbuf("action/sep.png"),
            app_theme.get_pixbuf("action/sep.png"))
        self.toolbox.pack_start(button)
        #self.toolbox.pack_start(VSeparator())

        self.create_button("undo", _("Tip undo"))
        self.create_button("save", _("Tip save"))
        
        button = ImageButton(
            app_theme.get_pixbuf("action/sep.png"),
            app_theme.get_pixbuf("action/sep.png"),
            app_theme.get_pixbuf("action/sep.png"))
        self.toolbox.pack_start(button)
        #self.toolbox.pack_start(VSeparator())

        self.create_button("cancel", _("Tip cancel"))
        self.create_button("finish", _("Tip finish"))
        self.create_button("share", _("Tip share"))

        if self.screenshot:
            self._button_clicked_cb = {
                'undo': self.screenshot.undo,
                'save': self.save_to_file,
                'cancel': self.win.quit,
                'finish': self.screenshot.save_snapshot,
                'share': self.share_picture}

    def create_toggle_button(self, name, action, text=''):
        ''' make a togglebutton '''
        button = ToggleButton(
            app_theme.get_pixbuf("action/" + name + "_normal.png"),
            app_theme.get_pixbuf("action/" + name + "_hover.png"),
            app_theme.get_pixbuf("action/" + name + "_press.png"))
        button.connect("pressed", self._toggle_button_pressed)
        button.connect("toggled", self._toggle_button_toggled, action)
        button.connect("released", self._toggle_button_released)
        button.connect("enter-notify-event", self._show_tooltip, text)
        button.set_name(name)
        button.set_size_request(28, 28)
        self.toolbox.pack_start(button)
        self._toggle_buton_list.append(button)

    def create_button(self, name, text=''):
        ''' make a button '''
        button = ImageButton(
            app_theme.get_pixbuf("action/" + name + "_normal.png"),
            app_theme.get_pixbuf("action/" + name + "_hover.png"),
            app_theme.get_pixbuf("action/" + name + "_press.png"))
        button.connect("enter-notify-event", self._show_tooltip, text)
        button.connect("clicked", self._button_clicked, name)
        button.set_name(name)
        button.set_size_request(28, 28)
        self.toolbox.pack_start(button)

    def _show_tooltip(self, widget, event, text):
        '''Create help tooltip.'''
        widget.set_has_tooltip(True)
        widget.set_tooltip_text(text)
        widget.trigger_tooltip_query()

    def _button_clicked(self, widget, name):
        ''' button clicked '''
        if self.screenshot is None:
            return
        # save current input text
        if self.screenshot.show_text_window_flag:
            self.win.save_text_window()
        self._button_clicked_cb[name](widget)

    def _toggle_button_released(self, widget):
        ''' toggle button pressed '''
        if self.screenshot is None:
            return
        self.screenshot.isToggled = False
        for each in self._toggle_buton_list:
            if each.get_active():
                self.screenshot.isToggled = True

    def _toggle_button_pressed(self, widget):
        ''' toggle button pressed '''
        for each in self._toggle_buton_list:
            if each == widget:
                continue
            each.set_active(False)
        # save current input text
        if self.screenshot.show_text_window_flag:
            self.win.save_text_window()

    def _toggle_button_toggled(self, widget, action):
        ''' toggle button toggled'''
        if self.screenshot is None:
            return
        if widget.get_active():
            self.screenshot.set_action_type(action)
            self.win.set_cursor(action)
            self.win.show_colorbar()
            self.win.adjust_colorbar()
        else:
            self.win.set_cursor(None)
            self.win.hide_colorbar()
            if not self.screenshot.action_list and not self.screenshot.text_action_list and self.screenshot.show_toolbar_flag and not self.screenshot.window_flag:
                self.screenshot.set_action_type(ACTION_SELECT)
            elif self.screenshot.action_list and self.screenshot.isToggled or self.screenshot.text_action_list:
                self.screenshot.set_action_type(None)
    
    def set_button_active(self, name, state):
        '''set button active'''
        for each in self._toggle_buton_list:
            if name == each.get_name():
                each.set_active(state)
                break
    
    def share_picture(self, widget):
        '''share picture'''
        self.screenshot.share_to_flag = True
        self.save_to_file()

    def save_to_file(self, widget=None):
        ''' save to file '''
        self.win.hide_colorbar()
        self.win.hide_toolbar()
        #dialog = SaveFileDialog('', self.screenshot.window.window,
            #ok_callback=self._save_to_file_cb, cancel_callback=self._save_to_file_cancel)
        dialog = gtk.FileChooserDialog(
            "Save..",
            self.win.window,
            gtk.FILE_CHOOSER_ACTION_SAVE,
            (gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT,
             gtk.STOCK_SAVE, gtk.RESPONSE_ACCEPT))
        dialog.set_action(gtk.FILE_CHOOSER_ACTION_SAVE)
        dialog.set_default_response(gtk.RESPONSE_ACCEPT)
        dialog.set_position(gtk.WIN_POS_MOUSE)
        dialog.set_local_only(True)
        last_folder = self.__config.get("save", "folder")
        if last_folder:
            dialog.set_current_folder(last_folder)
        else:
            dialog.set_current_folder(utils.get_pictures_dir())
        dialog.set_current_name("%s%s.%s" % (__(DEFAULT_FILENAME), utils.get_format_time(), "png"))
        response = dialog.run()
        filename = dialog.get_filename()
        if response == gtk.RESPONSE_ACCEPT:
            self.__config.set("save", folder=dialog.get_current_folder())
            self._save_to_file_cb(filename)
        else:
            self._save_to_file_cancel(filename)
        dialog.destroy()

    def _save_to_file_cancel(self, filename):
        ''' save file dialog cancel_callback'''
        self.screenshot.share_to_flag = False
        self.win.adjust_toolbar()
        self.win.show_toolbar()
        #self.win.show_colorbar()
        
    def _save_to_file_cb(self, filename):
        ''' save file dialog ok_callback'''
        print "save", filename
        self.screenshot.save_snapshot(filename=filename)
    
    def set_all_inactive(self):
        '''set all button inactive'''
        for each in self._toggle_buton_list:
            each.set_active(False)
    
    def show(self):
        ''' show the toolbar '''
        if not self.window.get_visible():
            self.window.show_window()

    def hide(self):
        '''hide the toolbar'''
        if self.window.get_visible():
            self.window.hide_all()

class Colorbar():
    ''' Colorbar window '''
    def __init__(self, parent=None, screenshot=None):
        self.screenshot = screenshot
        self.win = self.screenshot.window
        
        padding_x = 5
        padding_y = 3
        icon_width = icon_height = 28
        self.width = 280
        self.height = icon_height + padding_y * 2
        #color_num = 9
        
        self.window = Window(window_type=gtk.WINDOW_POPUP, shadow_visible=False)
        self.window.set_type_hint(gtk.gdk.WINDOW_TYPE_HINT_DIALOG)
        self.window.set_keep_above(True)
        self.window.set_transient_for(parent)
        self.window.set_decorated(False)
        #self.window.set_size_request(-1, self.height)

        vbox = gtk.VBox(False, 0)
        self.box = gtk.HBox(False, 1)
        self.size_box = gtk.HBox()
        self.dynamic_box = gtk.HBox()

        self.window.window_shadow.set(0.5, 0.5, 0, 0)
        self.window.window_shadow.set_padding(padding_y, padding_y, padding_x, padding_x)
        self.window.remove(self.window.window_shadow)
        self.window.add(vbox)
        self.window.window_shadow.remove(self.window.window_frame)
        self.window.window_shadow.add(self.box)
        vbox.pack_start(self.window.window_shadow)
        #self.window.window_frame.add(self.box)

        self.__size_button_dict = {}
        self.create_size_button("small", ACTION_SIZE_SMALL)
        self.create_size_button("normal", ACTION_SIZE_NORMAL)
        self.create_size_button("big", ACTION_SIZE_BIG)
        self.create_size_button("fill", ACTION_SIZE_RECTANGLE_ELLIPSE_FILL)
        self._set_size_button_state("small", True)

        self.size_align = gtk.Alignment()
        self.size_align.set(0.5,0.5,0,0)
        self.size_align.set_padding(2, 1, 0, 0)
        self.size_align.add(self.size_box)
        #self.dynamic_box.pack_start(self.size_align)
        self.box.pack_start(self.dynamic_box)
        
        # font select
        self.font_box = gtk.HBox()
        self.font_label = Label("Sans",enable_select=False, text_x_align=dtk.ui.constant.ALIGN_MIDDLE, label_width=20)
        self.font_label.set_size_request(20, 28)
        self.font_spin = SpinBox(10, 8, 72, 1)
        self.font_spin.connect("value-changed", self._font_size_changed)
        self.font_box.pack_start(self.font_label)
        self.font_box.pack_start(self.font_spin)
        #self.font_label.connect("button-press-event", self._select_font_event) 
        #self.font_label.connect("enter-notify-event", lambda w, e: utils.set_cursor(w, gtk.gdk.Cursor(gtk.gdk.HAND2)))
        #self.font_label.connect("leave-notify-event", lambda w, e: utils.set_default_cursor(w))
        #self.dynamic_box.pack_start(self.font_label)

        button = ImageButton(
            app_theme.get_pixbuf("action/color_sep.png"),
            app_theme.get_pixbuf("action/color_sep.png"),
            app_theme.get_pixbuf("action/color_sep.png"))
        self.box.pack_start(button)

        # color select
        self.color_select = gtk.EventBox()
        #self.color_select = ColorButton()

        self.box.pack_start(self.color_select, False, False)
        #self.color_select.set_border_width(2)
        self.color_select.set_events(gtk.gdk.BUTTON_PRESS_MASK)
        self.color_select.set_size_request(28,28)
        self.color_select.set_app_paintable(True)
        self.color_select.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse("#FF0000"))
        self.color_select.connect('expose-event', self._color_select_expose)
        #self.color_select.connect('button-press-event', self._select_color_event)
        #self.color_select.connect("enter-notify-event", lambda w, e: utils.set_cursor(w, gtk.gdk.Cursor(gtk.gdk.HAND2)))
        #self.color_select.connect("leave-notify-event", lambda w, e: utils.set_default_cursor(w))
        
        # color button
        self.vbox = gtk.VBox(False, 0)
        self.above_hbox = gtk.HBox(False, 2)
        self.below_hbox = gtk.HBox(False, 2)
        self.color_map = {
            'black'       : "#000000",
            'gray_dark'   : "#808080",
            'red_dark'    : "#800000",
            'yellow_dark' : "#808000",
            'green_dark'  : "#008000",
            'blue_dark'   : "#000080",
            'pink_dark'   : "#800080",
            'wathet_dark' : "#008080",
            'white'       : "#FFFFFF",
            'gray'        : "#C0C0C0",
            'red'         : "#FF0000",
            'yellow'      : "#FFFF00",
            'green'       : "#00FF00",
            'blue'        : "#0000FF",
            'pink'        : "#FF00FF",
            'wathet'      : "#00FFFF"}
        i = 0
        keys = self.color_map.keys()
        for name in keys:
            if i < len(keys)/2:
                self.create_color_button(self.above_hbox, name)
            else:
                self.create_color_button(self.below_hbox, name)
            i += 1
        self.vbox.pack_start(self.above_hbox)
        self.vbox.pack_start(self.below_hbox)
        self.box.pack_start(self.vbox)

    def create_color_button(self, box, name):
        ''' create color button'''
        button = ImageButton(
            app_theme.get_pixbuf("color/" + name + ".png"),
            app_theme.get_pixbuf("color/" + name + "_hover.png"),
            app_theme.get_pixbuf("color/" + name + "_hover.png"))
        button.connect('pressed', self._color_button_pressed, name) 
        button.set_size_request(14, 14)
        box.pack_start(button)

    def create_toggle_button(self, name):
        ''' make a togglebutton '''
        button = ToggleButton(
            app_theme.get_pixbuf("action/" + name + ".png"),
            app_theme.get_pixbuf("action/" + name + "_hover.png"),
            app_theme.get_pixbuf("action/" + name + "_press.png"))
        button.set_name(name)
        return button

    def create_image_button(self, name):
        '''create ImageButton'''
        button = ImageButton(
            app_theme.get_pixbuf("action/" + name + ".png"),
            app_theme.get_pixbuf("action/" + name + "_hover.png"),
            app_theme.get_pixbuf("action/" + name + "_press.png"))
        button.set_name(name)
        return button

    def create_size_button(self, name, index):
        ''' create size button '''
        #button = self.create_image_button(name)
        button = self.create_toggle_button(name)
        button.set_size_request(28, 28)
        button.connect("pressed", self._size_button_pressed, index)
        #button.connect("toggled", self._size_button_toggled, name)
        button.connect("released", self._size_button_released)
        self.size_box.pack_start(button)
        self.__size_button_dict[name] = button

    def _select_font_event(self, widget, event, data=None):
        ''' select font '''
        if self.screenshot is None:
            return
        self.win.hide_toolbar()
        self.win.hide_colorbar()
        font_dialog = gtk.FontSelectionDialog("font select")
        #font_dialog.set_skip_taskbar_hint(True)
        if self.screenshot.show_text_window_flag:
            font_dialog.set_transient_for(self.screenshot.text_window.window)
        else:
            font_dialog.set_transient_for(self.win.window)
        font_dialog.set_font_name(widget.text)
        font_dialog.connect("response", self._font_dialog_response)
        font_dialog.set_modal(True)
        font_dialog.show_all()

    def _font_dialog_response(self, widget, response):
        if response == gtk.RESPONSE_OK or response == gtk.RESPONSE_APPLY:
            self.screenshot.font_name = widget.get_font_name()
            print self.screenshot.font_name
            self.font_label.set_text(self.screenshot.font_name)
        self.win.adjust_toolbar()
        self.win.show_toolbar()
        self.win.show_colorbar()
        widget.destroy()

    def _font_size_changed(self, widget, value):
        '''font size changed'''
        self.screenshot.font_size = value
        if self.screenshot.show_text_window_flag:
            if not self.screenshot.text_window.set_font_size(value):
                #print value, self.screenshot.text_window.get_font_size()
                widget.set_value(self.screenshot.text_window.get_font_size())
            self.win.refresh()

    def _color_select_expose(self, widget, event, data=None):
        '''set colorBox border '''
        (x, y, width, height, depth) = widget.window.get_geometry() 
        cr = widget.window.cairo_create()
        cr.set_line_width(2)
        cr.rectangle(0,0,width, height)
        cr.set_source_rgb(0, 0, 0)
        cr.stroke()
        cr.rectangle(2,2,width-4, height-4)
        cr.set_line_width(1)
        cr.set_source_rgb(0xff, 0xff, 0xff)
        cr.stroke()

    def _select_color_event(self, widget, event, data=None):
        ''' select color '''
        self.win.hide_toolbar()
        self.win.hide_colorbar()
        color = ColorSelectDialog(confirm_callback=self._select_color, cancel_callback=self._select_color_cancel)
        color.set_transient_for(self.win.window)
        #color.set_keep_above(True)
        color.show_all()

    def _select_color(self, color_hex):
        ''' confirm select color '''
        self.color_select.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse(color_hex))
        if self.screenshot is None:
            return
        self.screenshot.action_color = color_hex
        self.win.adjust_toolbar()
        self.win.show_toolbar()
        self.win.show_colorbar()

    def _select_color_cancel(self):
        ''' cancel slect color'''
        self.win.adjust_toolbar()
        self.win.show_toolbar()
        self.win.show_colorbar()

    def _color_button_pressed(self, widget, name):
        ''' color button pressed'''
        self.color_select.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse(self.color_map[name]))
        if self.screenshot is None:
            return
        self.screenshot.action_color = self.color_map[name]
        if self.screenshot.show_text_window_flag:
            self.screenshot.text_window.set_text_color(self.screenshot.action_color)
            self.win.refresh()

    def _size_button_pressed(self, widget, index):
        ''' size button pressed'''
        if self.screenshot is None:
            return
        #self.screenshot.iconIndex = index
        self.screenshot.action_size = index
        for each in self.size_box.get_children():
            if each == widget:
                continue
            else:
                each.set_active(False)

    def _size_button_released(self, widget):
        ''' size button release '''
        if not widget.get_active():
            widget.set_active(True)

    def _set_size_button_state(self, name, state):
        '''set size button state'''
        for each in self.__size_button_dict.keys():
            if each == name:
                #each.set_active(state)
                self.__size_button_dict[name].set_active(state)
        
    def show(self):
        ''' show the colorbar'''
        # action is text, show font size set
        if self.screenshot.action == ACTION_TEXT:
            if self.size_align in self.dynamic_box.get_children():
                self.dynamic_box.remove(self.size_align)
            if self.font_box not in self.dynamic_box.get_children():
                self.dynamic_box.add(self.font_box)
        # show draw size
        else:
            if self.font_box in self.dynamic_box.get_children():
                self.dynamic_box.remove(self.font_box)
            if self.size_align not in self.dynamic_box.get_children():
                self.dynamic_box.add(self.size_align)
            # actin is rectangle or ellispe, show fill button
            if self.screenshot.action in [ACTION_RECTANGLE, ACTION_ELLIPSE]:
                if self.__size_button_dict['fill'] not in self.size_box.get_children():
                    self.size_box.pack_start(self.__size_button_dict['fill'])
            else:
                if self.__size_button_dict['fill'] in self.size_box.get_children():
                    if self.__size_button_dict['fill'].get_active():
                        self.__size_button_dict['small'].pressed()
                        self.__size_button_dict['small'].released()
                    self.size_box.remove(self.__size_button_dict['fill'])
        if not self.window.get_visible():
            self.window.show_window()

    def hide(self):
        '''hide the toolbar'''
        if self.window.get_visible():
            self.window.hide_all()

if __name__ == '__main__':
    #Toolbar().show()
    Colorbar().show()
    gtk.main()