from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.colorpicker import ColorPicker
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.popup import Popup
from kivy.uix.widget import Widget
from kivy.graphics import Color, Ellipse, Line
from kivy.core.window import Window

import os
from PIL import Image

class PaintWidget(Widget):
    def __init__(self, **kwargs):
        super(PaintWidget, self).__init__(**kwargs)
        self.line_width = 2
        self.brush_color = (0, 0, 0, 1)
        self.shape = 'line'
        self.points = []

    def on_touch_down(self, touch):
        with self.canvas:
            Color(*self.brush_color)
            if self.shape == 'line':
                touch.ud['line'] = Line(points=(touch.x, touch.y), width=self.line_width)
            elif self.shape == 'circle':
                d = 30
                Ellipse(pos=(touch.x - d / 2, touch.y - d / 2), size=(d, d))
            elif self.shape == 'square':
                d = 30
                touch.ud['rect'] = Line(rectangle=(touch.x - d / 2, touch.y - d / 2, d, d), width=self.line_width)

    def on_touch_move(self, touch):
        if self.shape == 'line':
            touch.ud['line'].points += [touch.x, touch.y]
        elif self.shape == 'square':
            self.canvas.remove(touch.ud['rect'])
            d = 30
            with self.canvas:
                Color(*self.brush_color)
                touch.ud['rect'] = Line(rectangle=(touch.x - d / 2, touch.y - d / 2, d, d), width=self.line_width)

    def set_brush_color(self, color):
        self.brush_color = color

    def set_line_width(self, width):
        self.line_width = width

    def set_shape(self, shape):
        self.shape = shape

class DrawingApp(App):
    def build(self):
        self.paint_widget = PaintWidget()
        
        main_layout = BoxLayout(orientation='vertical')
        buttons_layout = BoxLayout(size_hint=(1, 0.1))
        
        clear_button = Button(text='Clear')
        clear_button.bind(on_press=self.clear_canvas)
        buttons_layout.add_widget(clear_button)
        
        color_picker_button = Button(text='Color')
        color_picker_button.bind(on_press=self.open_color_picker)
        buttons_layout.add_widget(color_picker_button)
        
        save_button = Button(text='Save')
        save_button.bind(on_press=self.save_drawing)
        buttons_layout.add_widget(save_button)
        
        load_button = Button(text='Load')
        load_button.bind(on_press=self.open_load_dialog)
        buttons_layout.add_widget(load_button)
        
        brush_button = Button(text='Brush')
        brush_button.bind(on_press=self.set_brush)
        buttons_layout.add_widget(brush_button)
        
        circle_button = Button(text='Circle')
        circle_button.bind(on_press=self.set_circle)
        buttons_layout.add_widget(circle_button)
        
        square_button = Button(text='Square')
        square_button.bind(on_press=self.set_square)
        buttons_layout.add_widget(square_button)
        
        main_layout.add_widget(buttons_layout)
        main_layout.add_widget(self.paint_widget)
        
        return main_layout

    def clear_canvas(self, instance):
        self.paint_widget.canvas.clear()

    def open_color_picker(self, instance):
        color_picker = ColorPicker()
        popup = Popup(title='Pick a Color', content=color_picker, size_hint=(0.8, 0.8))
        color_picker.bind(color=self.on_color)
        popup.open()

    def on_color(self, instance, value):
        self.paint_widget.set_brush_color(value)

    def save_drawing(self, instance):
        self.save_dialog = FileChooserIconView()
        save_button = Button(text="Save", size_hint=(1, 0.1))
        save_button.bind(on_press=self.save_canvas)
        save_layout = BoxLayout(orientation="vertical")
        save_layout.add_widget(self.save_dialog)
        save_layout.add_widget(save_button)
        self.save_popup = Popup(title="Save Drawing", content=save_layout, size_hint=(0.8, 0.8))
        self.save_popup.open()

    def save_canvas(self, instance):
        if not self.save_dialog.selection:
            return
        path = self.save_dialog.selection[0]
        if os.path.splitext(path)[1] == '':
            path += '.png'
        self.export_to_png(path)
        self.save_popup.dismiss()

    def open_load_dialog(self, instance):
        self.load_dialog = FileChooserIconView()
        load_button = Button(text="Load", size_hint=(1, 0.1))
        load_button.bind(on_press=self.load_canvas)
        load_layout = BoxLayout(orientation="vertical")
        load_layout.add_widget(self.load_dialog)
        load_layout.add_widget(load_button)
        self.load_popup = Popup(title="Load Drawing", content=load_layout, size_hint=(0.8, 0.8))
        self.load_popup.open()

    def load_canvas(self, instance):
        if not self.load_dialog.selection:
            return
        path = self.load_dialog.selection[0]
        self.paint_widget.canvas.clear()
        with self.paint_widget.canvas:
            Image.open(path).show()
        self.load_popup.dismiss()

    def set_brush(self, instance):
        self.paint_widget.set_shape('line')

    def set_circle(self, instance):
        self.paint_widget.set_shape('circle')

    def set_square(self, instance):
        self.paint_widget.set_shape('square')

if __name__ == '__main__':
    DrawingApp().run()

