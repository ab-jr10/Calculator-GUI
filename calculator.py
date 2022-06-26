import tkinter as tk


LARGE_FONT = ("Arial", 40, "bold")
SMALL_FONT = ("Arial", 16)
DIGITS_FONT = ("Arial", 24, "bold")
DEFAULT_FONT = ("Arial", 20)

BUTTON_BG = "#0f3e62"  # "#154792"
BUTTON_FG = "#FFFFFF"
SPL_BUTTON_BG = "#3d6581"  # "#3186D8"
LABEL_BG = "#b6e0ea"  # "#3186D8"
LABEL_FG = "#0e265e"


class Calculator:
    def __init__(self):
        self.window = tk.Tk()
        self.window.geometry("375x667")
        self.window.resizable(0, 0)
        self.window.title("Calculator")
        self.window.attributes('-alpha', 0.9599)
        self.window.wm_iconbitmap("calc.ico")

        self.total_expression = ""
        self.current_expression = ""
        self.display_frame = self.create_display_frame()

        self.total_label, self.current_label = self.create_display_labels()
        
        self.digit = {
            7: (1, 1), 8: (1, 2), 9: (1, 3),
            4: (2, 1), 5: (2, 2), 6: (2, 3),
            1: (3, 1), 2: (3, 2), 3: (3, 3),   
            '.': (4, 1), 0: (4, 2)   
        }
        
        self.operations = {"/": "\u00F7", "*": "\u00D7", "-": "-", "+": "+"}
        
        
        self.buttons_frame = self.create_buttons_frame()
        
        self.buttons_frame.rowconfigure(0, weight=1)
        
        for x in range(1, 5):
            self.buttons_frame.rowconfigure(x, weight=1)
            self.buttons_frame.columnconfigure(x, weight=1)
            
                     
        self.create_digit_button()
        self.create_operator_button()
        self.create_special_button()
        self.bind_keys()
        
        
    def bind_keys(self):
        self.window.bind("<Return>", lambda event: self.evaluate())
        for key in self.digit:
            self.window.bind(str(key), lambda event,
                             digit=key: self.add_to_equation(digit))

        for key in self.operations:
            self.window.bind(key, lambda event,
                             operator=key: self.append_operator(operator))
        
        
    def create_special_button(self):
        self.clear_button()
        self.equals_to_button()
        self.square_button()
        self.sqrt_button()

        

    def create_display_labels(self):
        total_label = tk.Label(self.display_frame, text=self.total_expression, anchor=tk.E, bg=LABEL_BG, fg=LABEL_FG, padx=24, font=SMALL_FONT)
        total_label.pack(expand=True, fill='both')

        current_label = tk.Label(self.display_frame, text=self.current_expression, anchor=tk.E, bg=LABEL_BG, fg=LABEL_FG, padx=24, font=LARGE_FONT)
        current_label.pack(expand=True, fill='both')

        return total_label, current_label
    
    
    def add_to_equation(self, value):
        self.current_expression += str(value)
        self.update_current_label()


    def create_display_frame(self):
        frame = tk.Frame(self.window, height=221, bg=LABEL_BG)
        frame.pack(expand=True, fill="both")
        return frame

        
    def create_digit_button(self):
        for digit, grid_value in self.digit.items():
            button = tk.Button(self.buttons_frame, text= str(digit), bg= BUTTON_BG, fg=BUTTON_FG, font=DIGITS_FONT, borderwidth=0, command= lambda x=digit: self.add_to_equation(x))
            button.grid(row=grid_value[0], column= grid_value[1], sticky=tk.NSEW)
            
            
    def append_operator(self, operator):
        self.current_expression += operator
        self.total_expression += self.current_expression
        self.current_expression = ""
        self.update_current_label()
        self.update_total_label()
            
    def create_operator_button(self):
        i = 0
        for operator, symbol in self.operations.items():
            button = tk.Button(self.buttons_frame, text= symbol, bg= SPL_BUTTON_BG, fg=BUTTON_FG, font=DEFAULT_FONT, borderwidth=0, command= lambda  x=operator: self.append_operator(x))
            button.grid(row=i, column=4, sticky=tk.NSEW)
            i+=1
            
            
    def clear(self):
        self.current_expression = ""
        self.total_expression = ""
        self.update_current_label()
        self.update_total_label()
            
            
    def clear_button(self):
        button = tk.Button(self.buttons_frame, text="C", bg=SPL_BUTTON_BG, fg=BUTTON_FG, font=DEFAULT_FONT, borderwidth=0, command= self.clear)
        button.grid(row=0, column=1, sticky=tk.NSEW)
        
    
    def square(self):
        self.current_expression = str(eval(f"{self.current_expression}**2"))
        self.update_current_label()
        
        
    def square_button(self):
        button = tk.Button(self.buttons_frame, text="x\u00b2", bg=SPL_BUTTON_BG, fg=BUTTON_FG, font=DEFAULT_FONT, borderwidth=0, command=self.square)
        button.grid(row=0, column=2, sticky=tk.NSEW)
        
        
    def sqrt(self):
        self.current_expression = str(eval(f"{self.current_expression}**0.5"))
        self.update_current_label()

    def sqrt_button(self):
        button = tk.Button(self.buttons_frame, text="\u221ax", bg=SPL_BUTTON_BG, fg=BUTTON_FG, font=DEFAULT_FONT, borderwidth=0, command=self.sqrt)
        button.grid(row=0, column=3, sticky=tk.NSEW)

        
    def evaluate(self):
        self.total_expression += self.current_expression
        self.update_total_label()
        
        try:
            self.current_expression = str(eval(self.total_expression))
            
            self.total_expression = ""
        except Exception as e:
            self.current_expression = "Error"      
        finally:
            self.update_current_label()
        
     
        
    def equals_to_button(self):
        button = tk.Button(self.buttons_frame, text="=", bg=SPL_BUTTON_BG, fg=BUTTON_FG, font=DEFAULT_FONT, borderwidth=0, command= self.evaluate)
        button.grid(row=4, column=3, columnspan=2, sticky=tk.NSEW)

            
    def create_buttons_frame(self):
        frame = tk.Frame(self.window)
        frame.pack(expand=True, fill="both")
        return frame
    
    
    def update_total_label(self):
        expression = self.total_expression
        for operator, symbol in self.operations.items():
            expression = expression.replace(operator, f" {symbol} ")
        self.total_label.config(text=expression)
        
        
    def update_current_label(self):
        self.current_label.config(text=self.current_expression[:11])


    
   

    def run(self):
        self.window.mainloop()


if __name__ == "__main__":
    calc = Calculator()
    calc.run()
