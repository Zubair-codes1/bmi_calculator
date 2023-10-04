import customtkinter as ctk
from settings import *
try:
    from ctypes import windll, byref, sizeof, c_int
except:
    pass

class App(ctk.CTk):
    def __init__(self):
        super().__init__(fg_color=GREEN)
        # window attributes
        self.title("BMI calculator")
        self.geometry("350x325")
        self.resizable(False, False)
        self.change_title_bar_colour()

        # overarching grid layout
        self.columnconfigure(0, weight=1)
        self.rowconfigure((0, 1, 2, 3), weight=1, uniform="a")

        # data
        self.height_int = ctk.DoubleVar(value=1.7)
        self.weight_float = ctk.DoubleVar(value=70)
        self.bmi_string = ctk.StringVar()
        self.update_bmi()

        # tracing when the height and weight are updated
        self.height_int.trace("w", self.update_bmi)
        self.weight_float.trace("w", self.update_bmi)

        # other classes - for making the app
        Output(self, self.bmi_string)
        Weight(self, self.weight_float)
        Height(self, self.height_int)

        self.mainloop()

    # changes title bar colour
    def change_title_bar_colour(self):
        try:
            HWND = windll.user32.GetParent(self.winfo_id())
            windll.dwmapi.DwmSetWindowAttribute(HWND, 35, byref(c_int(TITLE_HEX_COLOUR)), sizeof(c_int))
        except:
            pass

    # uses data to change the bmi accordingly
    def update_bmi(self, *args):
        height_meters = self.height_int.get()
        weight_kg = self.weight_float.get()
        bmi_result = round((weight_kg / (height_meters ** 2)), 2)
        self.bmi_string.set(bmi_result)

# Output label
class Output(ctk.CTkLabel):
    def __init__(self, parent, bmi_value):
        # font = ctk.CTkFont(family=FONT, size=MAIN_TEXT_SIZE)
        super().__init__(master=parent, font=(FONT, MAIN_TEXT_SIZE, "bold"), textvariable=bmi_value)
        self.grid(column=0, row=0, rowspan=2, sticky="nsew")

# Weight section - increase / decreasing weight
class Weight(ctk.CTkFrame):
    def __init__(self, parent, weight_float):
        COLOUR = WHITE
        super().__init__(master=parent, fg_color=COLOUR, corner_radius=10)
        self.weight_float = weight_float
        self.weight_float.set(70)
        # grid layout for weight section
        self.columnconfigure(0, weight=2, uniform="b")
        self.columnconfigure(1, weight=1, uniform="b")
        self.columnconfigure(2, weight=3, uniform="b")
        self.columnconfigure(3, weight=1, uniform="b")
        self.columnconfigure(4, weight=2, uniform="b")
        self.rowconfigure(0, weight=1, uniform="b")
        self.grid(column=0, row=2, rowspan=1, stick="nsew", padx=10, pady=10)

        # widgets
        self.weight = ctk.CTkLabel(master=self, text=f"{self.weight_float.get()}kg", text_color=BLACK,
                                   font=(FONT, INPUT_FONT_SIZE))
        self.weight.grid(row=0, column=2)

        # different buttons
        decrease_large = ctk.CTkButton(
            master=self, text="-", text_color=BLACK, font=(FONT, INPUT_FONT_SIZE),
            corner_radius=5, fg_color=LIGHT_GRAY, hover_color=GRAY,
            command=self.max_decrease
        )
        decrease_large.grid(column=0, row=0, padx=5)
        decrease_small = ctk.CTkButton(
            master=self, text="-", text_color=BLACK, font=(FONT, SWITCH_FONT_SIZE),
            corner_radius=5, hover_color=GRAY, fg_color=LIGHT_GRAY,
            command=self.min_decrease
        )
        decrease_small.grid(column=1, row=0, padx=5)
        increase_small = ctk.CTkButton(
            master=self, text="+", text_color=BLACK, font=(FONT, SWITCH_FONT_SIZE),
            corner_radius=5, fg_color=LIGHT_GRAY, hover_color=GRAY,
            command=self.min_increase
        )
        increase_small.grid(row=0, column=3, padx=5)
        increase_large = ctk.CTkButton(
            master=self, text="+", text_color=BLACK, font=(FONT, INPUT_FONT_SIZE),
            corner_radius=5, fg_color=LIGHT_GRAY, hover_color=GRAY,
            command=self.max_increase
        )
        increase_large.grid(row=0, column=4, padx=5)

    # functions for changing the weight
    def max_decrease(self):
        value = self.weight_float.get()
        value -= 1
        self.weight_float.set(value)
        self.weight.configure(text=f"{round(self.weight_float.get() * 10) / 10}kg")

    def min_decrease(self):
        value = self.weight_float.get()
        value -= 0.1
        self.weight_float.set(value)
        self.weight.configure(text=f"{round(self.weight_float.get() * 10) / 10}kg")

    def min_increase(self):
        value = self.weight_float.get()
        value += 0.1
        self.weight_float.set(value)
        self.weight.configure(text=f"{round(self.weight_float.get() * 10) / 10}kg")

    def max_increase(self):
        value = self.weight_float.get()
        value += 1
        self.weight_float.set(value)
        self.weight.configure(text=f"{round(self.weight_float.get() * 10) / 10}kg")

    def get_weight_value(self):
        return self.weight_float.get()

# height slider to input the person height
class Height(ctk.CTkFrame):
    def __init__(self, parent, height_value):
        super().__init__(master=parent)
        self.height_value = height_value
        self.height_value.set(1.7)
        # grid layout for height
        self.columnconfigure(0, weight=4, uniform="c")
        self.columnconfigure(1, weight=2, uniform="c")
        self.rowconfigure(0, weight=1, uniform="c")
        self.configure(fg_color=WHITE)
        self.grid(column=0, row=3, rowspan=1, stick="nsew", padx=10, pady=10)

        # min and max heights
        # widgets
        self.slider = ctk.CTkSlider(
            master=self, orientation="horizontal", progress_color=GREEN, fg_color=GRAY, button_color=GREEN,
            button_hover_color=GREEN, from_=1, to=2.5, command=self.get_slider_value, variable=self.height_value
        )
        self.slider.grid(row=0, column=0)
        self.height_label = ctk.CTkLabel(
            master=self, text=f"{self.slider.get()}m", fg_color=WHITE, text_color=BLACK,
            font=(FONT, INPUT_FONT_SIZE)
        )
        self.height_label.grid(row=0, column=1)

    def get_slider_value(self, value):
        self.height_label.configure(text=f"{round(self.slider.get() * 100)  / 100}m")

if __name__ == "__main__":
    App()
