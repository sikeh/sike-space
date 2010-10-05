#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#    screenrec is a screen recorder inspired by Zaheer Abbas Merali's istanbul
#    Copyright (C) 2006  Michael Urman
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of version 2 of the GNU General Public License as
#    published by the Free Software Foundation.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#

import os, time
try: import pygtk; pygtk.require('2.0'); del pygtk
except ImportError: pass
import gtk, gobject
if gtk.gtk_version < (2, 6, 0):
    raise ImportError("GTK+ version 2.6.0 not found")
try: import pygst; pygst.require('0.10'); del pygst
except ImportError: pass
import gst
if gst.gst_version < (0, 10, 0):
    raise ImportError("GStreamer version 0.10.0 not found")
from egg import trayicon
_ = str

__NAME__ = "Cankiri"
__VERSION__ = "0.2"

class AreaIndicator(gtk.Window):
    edge = {
        (-1, -1): gtk.gdk.WINDOW_EDGE_NORTH_WEST,
        ( 0, -1): gtk.gdk.WINDOW_EDGE_NORTH,
        ( 1, -1): gtk.gdk.WINDOW_EDGE_NORTH_EAST,
        (-1,  0): gtk.gdk.WINDOW_EDGE_WEST,
        ( 0,  0): gtk.gdk.WINDOW_EDGE_NORTH,
        ( 1,  0): gtk.gdk.WINDOW_EDGE_EAST,
        (-1,  1): gtk.gdk.WINDOW_EDGE_SOUTH_WEST,
        ( 0,  1): gtk.gdk.WINDOW_EDGE_SOUTH,
        ( 1,  1): gtk.gdk.WINDOW_EDGE_SOUTH_EAST,
    }
    cursor = {
        (-1, -1): gtk.gdk.TOP_LEFT_CORNER,
        ( 0, -1): gtk.gdk.FLEUR,
        ( 1, -1): gtk.gdk.TOP_RIGHT_CORNER,
        (-1,  0): gtk.gdk.LEFT_SIDE,
        ( 0,  0): gtk.gdk.X_CURSOR,
        ( 1,  0): gtk.gdk.RIGHT_SIDE,
        (-1,  1): gtk.gdk.BOTTOM_LEFT_CORNER,
        ( 0,  1): gtk.gdk.BOTTOM_SIDE,
        ( 1,  1): gtk.gdk.BOTTOM_RIGHT_CORNER,
    }
    def __init__(self):
        gtk.Window.__init__(self, gtk.WINDOW_POPUP)
        self.border = 5
        self.da = da = gtk.DrawingArea()
        self.add(da)
        da.connect('configure-event', self.configure_event)
        da.connect('expose-event', self.expose_event)
        da.connect('button-press-event', self.button_press_event)
        da.connect('motion-notify-event', self.motion_notify_event)
        da.add_events(gtk.gdk.POINTER_MOTION_MASK
                | gtk.gdk.BUTTON_PRESS_MASK
                | gtk.gdk.BUTTON_RELEASE_MASK)
        da.show()
        self.frozen = False

    def get_position(self, x, y):
        width, height = self.window.get_size()
        if 0 <= x < 20: xpos = -1
        elif width - 20 <= x < width: xpos = 1
        else: xpos = 0
        if 0 <= y < 20: ypos = -1
        elif height - 20 <= y < height: ypos = 1
        else: ypos = 0
        return xpos, ypos

    def button_press_event(self, da, event):
        if self.frozen:
            return

        if event.button == 1 and event.type == gtk.gdk.BUTTON_PRESS:
            edge = self.edge[self.get_position(event.x, event.y)]
            if edge == gtk.gdk.WINDOW_EDGE_NORTH:
                self.begin_move_drag(event.button,
                        int(event.x_root), int(event.y_root), event.time)
            else:
                self.begin_resize_drag(edge, event.button,
                        int(event.x_root), int(event.y_root), event.time)

    def motion_notify_event(self, da, event):
        if self.frozen:
            da.window.set_cursor(None)
            return
        cursor = self.cursor[self.get_position(event.x, event.y)]
        da.window.set_cursor(gtk.gdk.Cursor(cursor))

    def expose_event(self, da, event):
        width, height = da.window.get_size()
        cr = da.window.cairo_create()
        cr.rectangle(event.area.x, event.area.y,
                event.area.width, event.area.height)
        cr.clip()

        bw = self.border / 2.0 + 1
        cr.set_line_width(bw)
        cr.rectangle(bw - 0.5, bw - 0.5,
                width - self.border - 1, height - self.border - 1)
        if self.frozen: cr.set_source_rgb(0.75, 0.75, 0.75)
        else: cr.set_source_rgb(1, 1, 0.5)
        cr.stroke()

        cr.set_line_width(1)
        cr.set_source_rgb(0, 0, 0)
        cr.rectangle(0.5, 0.5, width - 1, height - 1)
        cr.rectangle(self.border - 0.5, self.border - 0.5,
                width - 2 * self.border + 1, height - 2 * self.border + 1)
        cr.stroke()

    def configure_event(self, da, event):
        width, height = da.window.get_size()
        shape = gtk.gdk.Pixmap(None, width, height, 1)
        gc = gtk.gdk.GC(shape)
        gc.set_foreground(gtk.gdk.Color(pixel=0))
        shape.draw_rectangle(gc, True, 0, 0, width, height)
        gc.set_foreground(gtk.gdk.Color(pixel=1))
        for n in range(self.border):
            shape.draw_rectangle(gc, False, n, n, width - 2 * n - 1, height - 2 * n - 1)
        self.window.shape_combine_mask(None, 0, 0)
        self.window.shape_combine_mask(shape, 0, 0)

    def set_area(self, area):
        self.move(area[0] - self.border, area[1] - self.border)
        self.resize(area[2] + 2 * self.border, area[3] + 2 * self.border)

    def get_area(self):
        left, top = self.window.get_origin()
        width, height = self.window.get_size()
        return (left + self.border, top + self.border,
                width - 2 * self.border, height - 2 * self.border)

    def set_frozen(self, frozen):
        self.frozen = frozen
        if self.da.window:
            self.da.queue_draw_area(0, 0, *self.da.window.get_size())

class Recorder(object):
    def __init__(self):
        self.__map = False
        self.image = image = gtk.Image()
        self.icon = icon = trayicon.TrayIcon(__NAME__)
        ebox = gtk.EventBox()
        ebox.add(image)
        icon.add(ebox)

        ebox.connect('button-press-event', self.__button)
        icon.connect('map-event', self.__map_icon, True)
        icon.connect('unmap-event', self.__map_icon, False)

        self.set_state('idle')
        icon.show_all()

        self.last_folder = os.path.abspath('.')
        self.capture_filename = ''
        self.capture_audio = False
        self.capture_framerate = 10
        self.capture_pointer = True
        self.capture_fullscreen = True
        width, height = gtk.gdk.screen_width(), gtk.gdk.screen_height()
        self.capture_area = (width / 4, height / 4, width / 2, height / 2)

        self.area = AreaIndicator()
        self.area.set_area(self.capture_area)
        gobject.idle_add(self.start_recording)

        self.save = gtk.FileChooserDialog(__NAME__,
            action=gtk.FILE_CHOOSER_ACTION_SAVE,
            buttons=(gtk.STOCK_OK, gtk.RESPONSE_OK,
                gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL))
        self.save.connect('map-event', self.__icon_fallback)

        self.about = gobject.new(gtk.AboutDialog,
                name=__NAME__, version=__VERSION__,
                authors=["Michael Urman", "Zaheer Abbas Merali"],
                copyright="Copyright © 2006 Michael Urman",
                comments="Cankiri Screen Recorder\n\n"
                    "This file may be distributed and/or modified under the "
                    "terms of the GNU General Public License version 2 as "
                    "published by the Free Software Foundation",
                website="http://www.tortall.net/mu/wiki/Cankiri")

    def __map_icon(self, container, event, mapping):
        self.__map = mapping
        if not mapping: self.__icon_fallback()

    def __icon_fallback(self, *args):
        if not self.__map:
            window = gobject.new(gtk.Window, resizable=False,
                    skip_pager_hint=True, skip_taskbar_hint=True)
            window.set_keep_above(True)
            window.move(0, 0)
            ebox = self.icon.get_children()[0]
            self.icon.remove(ebox)
            window.add(ebox)
            window.show_all()

    def __button(self, widget, event):
        if event.button == 1:
            self.toggle_recording()
        elif event.button == 3:
            menu = gtk.Menu()
            if self.state == 'idle':
                item = gtk.ImageMenuItem(gtk.STOCK_MEDIA_RECORD)
                item.connect('activate', self.start_recording)
                menu.append(item)

            if self.state == 'record':
                item = gtk.ImageMenuItem(gtk.STOCK_MEDIA_STOP)
                item.connect('activate', self.end_recording)
                menu.append(item)

            item = gtk.ImageMenuItem(gtk.STOCK_ABOUT)
            item.connect('activate', self.__about)
            menu.append(item)

            item = gtk.ImageMenuItem(gtk.STOCK_QUIT)
            item.connect('activate', self.__quit)
            menu.append(item)

            for item in menu: item.show()
            menu.popup(None, None, None, event.button, event.time)

    def __about(self, activator):
        self.about.run()
        self.about.hide()

    def __quit(self, activator):
        if self.state == 'record':
            self.end_recording()
        self.save.response(gtk.RESPONSE_CANCEL)
        self.about.destroy()
        gtk.main_quit()

    def set_state(self, state, name=__NAME__, tips=gtk.Tooltips()):
        self.state = state
        image = dict(idle=gtk.STOCK_MEDIA_STOP, record=gtk.STOCK_MEDIA_RECORD,
                configure=gtk.STOCK_PREFERENCES)[state]
        state = dict(idle=_("Idle"), record=_("Recording"),
                configure=_("Configuring"))[state]
        self.image.set_from_stock(image, gtk.ICON_SIZE_MENU)
        tips.set_tip(self.icon, _("%(name)s: %(state)s") % locals())

    def toggle_recording(self):
        if self.state == 'idle':
            self.start_recording()
        elif self.state == 'record':
            self.end_recording()

    def query_save_options(self):
        if self.state == 'configure': return gtk.RESPONSE_CANCEL
        self.set_state('configure')

        ogg = gtk.FileFilter()
        ogg.set_name(_("Ogg Theora Video (*.ogg)"))
        ogg.add_pattern("*.ogg")

        self.save.add_filter(ogg)
        self.save.set_current_folder(self.last_folder)
        self.save.set_current_name(_("screencast-%s-%s.ogg") %
                (os.environ.get('USER'), time.strftime("%Y-%m-%d-%H-%M")))
        self.save.set_do_overwrite_confirmation(True)
        self.save.set_default_response(gtk.RESPONSE_OK)

        table = gtk.Table(2, 2)
        self.save.set_extra_widget(table)

        audio = gtk.CheckButton(_("Record _sound"))
        if self.capture_audio: audio.set_active(True)
        table.attach(audio, 0, 1, 0, 1)

        pointer = gtk.CheckButton(_("Record _mouse pointer"))
        if self.capture_pointer: pointer.set_active(True)
        table.attach(pointer, 0, 1, 1, 2)

        fullscreen = gtk.RadioButton(None, _("Capture _entire screen"))
        table.attach(fullscreen, 1, 2, 0, 1)

        partial = gtk.RadioButton(fullscreen, _("Capture _partial screen"))
        table.attach(partial, 1, 2, 1, 2)
        table.show_all()

        fullscreen.set_active(self.capture_fullscreen)
        partial.set_active(not self.capture_fullscreen)

        self.area.set_area(self.capture_area)
        self.area.set_frozen(False)
        if self.capture_fullscreen: self.area.hide()
        else: self.area.show()

        def toggle_shown(toggle, widget):
            if toggle.get_active(): widget.show()
            else: widget.hide()
        partial.connect('toggled', toggle_shown, self.area)

        done = []
        self.save.connect_object('response', list.append, done)
        self.save.show()
        while not done:
            gtk.main_iteration()
        resp = done[0]
        if resp == gtk.RESPONSE_OK:
            self.last_folder = self.save.get_current_folder()
            self.capture_filename = self.save.get_filename()
            self.capture_audio = audio.get_active()
            self.capture_pointer = pointer.get_active()
            self.capture_fullscreen = fullscreen.get_active()
            try: self.capture_area = self.area.get_area()
            except AttributeError: pass
            self.area.set_frozen(True)
        else:
            self.area.hide()
            self.area.set_area(self.capture_area)
            self.image.set_from_stock(gtk.STOCK_MEDIA_STOP, gtk.ICON_SIZE_MENU)
            self.set_state('idle')

        if self.capture_fullscreen: self.area.hide()
        else: self.area.show()
        
        self.save.hide()
        return resp

    def start_recording(self, activator=None):
        if self.query_save_options() != gtk.RESPONSE_OK:
            return

        def elm(element, *args, **kwargs):
            return (element, args and args[0] or ' ', kwargs)

        def make_pipeline(*elements):
            return ' ! '.join([joiner.join([element] +
                map('%s=%s'.__mod__, options.items()))
                for element, joiner, options in elements])

        fps = "%d/1" % int(self.capture_framerate)
        pointer = str(self.capture_pointer).lower()

        if self.capture_fullscreen:
            left = top = right = bottom = 0
            width = gtk.gdk.screen_width()
            height = gtk.gdk.screen_height()
        else:
            left, top, width, height = self.capture_area
            right = gtk.gdk.screen_width() - width - left
            bottom = gtk.gdk.screen_height() - height - top

        output = self.capture_filename
        if not os.path.splitext(output)[1]:
            output = os.path.extsep.join([self.capture_filename, 'ogg'])

        video = make_pipeline(
            elm('ximagesrc', name='video', **{'show-pointer': pointer}),
            elm('ffmpegcolorspace'),
            elm('videobox', left=left, top=top, right=right, bottom=bottom),
            elm('video/x-raw-yuv',',', width=width, height=height, framerate=fps),
            elm('theoraenc', quality="32"),
            elm('mux.'),
        )
        audio = make_pipeline(
            elm(gst.registry_get_default().find_plugin('gconfelements')
                and 'gconfaudiosrc' or 'alsasrc', name='audio'),
            elm('audioconvert'),
            elm('vorbisenc', quality="0.1"),
            elm('mux.'),
        )
        mux = make_pipeline(
            elm('oggmux', name='mux'),
            elm('filesink', name='sink'),
        )

        if not self.capture_audio: pipeline = ' '.join([mux, video])
        else: pipeline = ' '.join([mux, video, audio])

        print pipeline

        self.pipeline = gst.parse_launch(pipeline)
        self.pipeline.get_by_name('sink').set_property('location', output)
        bus = self.pipeline.get_bus()
        bus.add_signal_watch()
        bus.connect("message", self.bus_message)

        self.pipeline.set_state(gst.STATE_PLAYING)

        self.set_state('record')

    def end_recording(self, activator=None):
        for name in ("video", "audio"):
            source = self.pipeline.get_by_name(name)
            if source:
                source.set_state(gst.STATE_NULL)
                source.set_locked_state(True)

    def bus_message(self, bus, message):
        if message.type == gst.MESSAGE_ERROR:
            print message.parse_error()
        elif message.type == gst.MESSAGE_EOS:
            self.pipeline.set_state(gst.STATE_NULL)
            self.set_state('idle')
            self.area.hide()

if __name__ == '__main__':
    recorder = Recorder()
    try: gtk.main()
    except KeyboardInterrupt: pass
