import customtkinter as ctk
from settings import *
try:
    from ctypes import windll, byref, sizeof, c_int
except:
    pass

class App(ctk.CTk):
    def __init__(self):
        super().__init__(fg_color=GREEN)
        self.title("BMI calculator")
        self.geometry("350x350")
        self.resizable(False, False)
        self.change_title_bar_colour()

        self.columnconfigure(0, weight=1)
        self.rowconfigure((0, 1, 2, 3), weight=1, uniform="a")

        self.output = Output(self)
        self.weight = Weight(self)

        self.mainloop()

    def change_title_bar_colour(self):
        try:
            HWND = windll.user32.GetParent(self.winfo_id())
            windll.dwmapi.DwmSetWindowAttribute(HWND, 35, byref(c_int(TITLE_HEX_COLOUR)), sizeof(c_int))
        except:
            pass

class Output(ctk.CTkLabel):
    def __init__(self, parent):
        font = ctk.CTkFont(family=FONT, size=MAIN_TEXT_SIZE)
        output_text = 22.5
        super().__init__(master=parent, font=font, text=output_text)
        self.grid(column=0, row=0, rowspan=2, sticky="nsew")

class Weight(ctk.CTkFrame):
    def __init__(self, parent):
        COLOUR = WHITE
        super().__init__(master=parent, fg_color=COLOUR, corner_radius=10)
        self.columnconfigure(0, weight=2, uniform="b")
        self.columnconfigure(1, weight=1, uniform="b")
        self.columnconfigure(2, weight=3, uniform="b")
        self.columnconfigure(3, weight=1, uniform="b")
        self.columnconfigure(4, weight=2, uniform="b")
        self.rowconfigure(0, weight=1, uniform="b")
        self.configure(corner_radius=8)
        self.grid(column=0, row=2, rowspan=1, stick="nsew", padx=10, pady=10)

        # widgets
        self.weight_value = 70
        self.weight = ctk.CTkLabel(master=self, text=f"{self.weight_value}kg", text_color=BLACK, font=(FONT,
                                                                                                  INPUT_FONT_SIZE))
        self.weight.grid(row=0, column=2)
        decrease_large = ctk.CTkButton(master=self, text="-", text_color=BLACK, font=(FONT, INPUT_FONT_SIZE),
                                       corner_radius=5, fg_color=LIGHT_GRAY, hover_color=GRAY,
                                       command=self.max_decrease)
        decrease_large.grid(column=0, row=0, padx=5)
        decrease_small = ctk.CTkButton(master=self, text="-", text_color=BLACK, font=(FONT, SWITCH_FONT_SIZE),
                                       corner_radius=5, hover_color=GRAY, fg_color=LIGHT_GRAY,
                                       command=self.min_decrease)
        decrease_small.grid(column=1, row=0, padx=5)
        increase_small = ctk.CTkButton(master=self, text="+", text_color=BLACK, font=(FONT, SWITCH_FONT_SIZE),
                                       corner_radius=5, fg_color=LIGHT_GRAY, hover_color=GRAY,
                                       command=self.min_increase)
        increase_small.grid(row=0, column=3, padx=5)
        increase_large = ctk.CTkButton(master=self, text="+", text_color=BLACK, font=(FONT, INPUT_FONT_SIZE),
                                       corner_radius=5, fg_color=LIGHT_GRAY, hover_color=GRAY,
                                       command=self.max_increase)
        increase_large.grid(row=0, column=4, padx=5)

    def max_decrease(self):
        self.weight_value -= 1
        self.weight.configure(text=f"{round(self.weight_value * 10) / 10}kg")
    def min_decrease(self):
        self.weight_value -= 0.1
        self.weight.configure(text=f"{round(self.weight_value * 10) / 10}kg")
    def min_increase(self):
        self.weight_value += 0.1
        self.weight.configure(text=f"{round(self.weight_value * 10) / 10}kg")
    def max_increase(self):
        self.weight_value += 1
        self.weight.configure(text=f"{round(self.weight_value * 10) / 10}kg")

if __name__ == "__main__":
    App()
