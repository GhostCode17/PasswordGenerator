from customtkinter import *

import pyperclip
import requests
import random
import string

class PythonApp(CTk):
    
    def __init__(self):

        super().__init__()

        set_appearance_mode("dark")
        set_default_color_theme("green")

        self.wm_title("Password generator")
        self.wm_resizable(False, False)

        self.generated_password = "None"
        
        self.password_can_contain_uppercase_letters = BooleanVar(value= True)
        self.password_can_contain_lowercase_letters = BooleanVar(value= True)
        self.password_can_contain_numbers = BooleanVar(value= True)
        self.password_can_contain_symbols = BooleanVar(value= True)

        self.label_password_length = CTkLabel(self, text= "Length: 8")
        self.label_password_length.grid(row= 0, column= 0, padx= 5, pady= 5, sticky= W)

        self.slider_password_length = CTkSlider(self, from_= 8, to= 16, number_of_steps= 8, command= lambda slider_value: self.label_password_length.configure(text= f"Length: {str(int(slider_value))}"))
        self.slider_password_length.set(0.0)
        self.slider_password_length.grid(row= 1, column= 0, padx= 5, pady= 5, sticky= W)

        self.label_information = CTkLabel(self, text= "* The length is not considered to generate a special password *")
        self.label_information.grid(row= 2, column= 0, padx= 5, pady= 5, sticky= W)

        self.label_password_options = CTkLabel(self, text= "Can contain:")
        self.label_password_options.grid(row= 0, column= 1, padx= 5, pady= 5, sticky= W)
        
        self.checkbox_password_options_uppercase = CTkCheckBox(self, text= "Uppercase", command= self.validate_special_and_non_special_password_generation_options, variable= self.password_can_contain_uppercase_letters)
        self.checkbox_password_options_uppercase.grid(row= 1, column= 1, padx= 5, pady= 5, sticky= W)

        self.checkbox_password_options_lowercase = CTkCheckBox(self, text= "Lowercase", command= self.validate_special_and_non_special_password_generation_options, variable= self.password_can_contain_lowercase_letters)
        self.checkbox_password_options_lowercase.grid(row= 2, column= 1, padx= 5, pady= 5, sticky= W)

        self.checkbox_password_options_numbers = CTkCheckBox(self, text= "Numbers", command= self.validate_special_and_non_special_password_generation_options, variable= self.password_can_contain_numbers)
        self.checkbox_password_options_numbers.grid(row= 3, column= 1, padx= 5, pady= 5, sticky= W)

        self.checkbox_password_options_symbols = CTkCheckBox(self, text= "Symbols", command= self.validate_special_and_non_special_password_generation_options, variable= self.password_can_contain_symbols)
        self.checkbox_password_options_symbols.grid(row= 4, column= 1, padx= 5, pady= 5, sticky= W)

        self.label_actions = CTkLabel(self, text= "Actions")
        self.label_actions.grid(row= 0, column= 2, padx= 5, pady= 5, sticky= W)

        self.button_generate_non_special_password = CTkButton(self, text= "Generate", command= self.generate_and_write_non_special_password)
        self.button_generate_non_special_password.grid(row= 1, column= 2, padx= 5, pady= 5, sticky= W)

        self.button_generate_special_password = CTkButton(self, text= "Generate a special", command= self.generate_and_write_special_password)
        self.button_generate_special_password.grid(row= 2, column= 2, padx= 5, pady= 5, sticky= W)
        
        self.button_copy_password = CTkButton(self, text= "Copy", command= lambda: pyperclip.copy(self.generated_password))
        self.button_copy_password.grid(row= 3, column= 2, padx= 5, pady= 5, sticky= W)

        self.label_generated_password = CTkLabel(self, text= f"Your password: {self.generated_password}")
        self.label_generated_password.grid(row= 4, column= 2, padx= 5, pady= 5, sticky= W)

    def validate_special_and_non_special_password_generation_options(self):

        enable_button_generate_non_special_password = False
        enable_button_generate_non_special_password = enable_button_generate_non_special_password or self.password_can_contain_uppercase_letters.get() 
        enable_button_generate_non_special_password = enable_button_generate_non_special_password or self.password_can_contain_lowercase_letters.get() 
        enable_button_generate_non_special_password = enable_button_generate_non_special_password or self.password_can_contain_numbers.get() 
        enable_button_generate_non_special_password = enable_button_generate_non_special_password or self.password_can_contain_symbols.get()

        enable_button_generate_special_password = True

        if not (self.password_can_contain_uppercase_letters.get() or self.password_can_contain_lowercase_letters.get()):
            enable_button_generate_special_password = False

        if not(self.password_can_contain_numbers.get() or self.password_can_contain_symbols.get()):
            enable_button_generate_special_password = False

        map_of_button_states = { True : NORMAL, False : DISABLED }
        
        self.button_generate_non_special_password.configure(state = map_of_button_states.get(enable_button_generate_non_special_password))
        self.button_generate_special_password.configure(state = map_of_button_states.get(enable_button_generate_special_password))

    def generate_and_write_special_password(self):

        response = None

        string_of_numbers = ""
        string_of_symbols = ""

        for _ in range(1, random.randint(1, 3) + 1):
            string_of_numbers += random.choice(string.digits)

        for _ in range(1, random.randint(1, 2) + 1):
            string_of_symbols += random.choice(string.punctuation)

        try:
            response = requests.get("https://random-word-api.herokuapp.com/word", timeout= 2)
        except:
            pass

        self.generated_password = response.json()[0] if response else "httperror"

        if self.password_can_contain_uppercase_letters.get() and self.password_can_contain_lowercase_letters.get():
            self.generated_password = self.generated_password.capitalize()

        elif self.password_can_contain_uppercase_letters.get():
            self.generated_password = self.generated_password.upper()

        elif self.password_can_contain_lowercase_letters.get():
            self.generated_password = self.generated_password.lower()

        if self.password_can_contain_numbers.get() and self.password_can_contain_symbols.get():
            self.generated_password += (string_of_numbers + string_of_symbols) if random.choice([0, 1]) == 0 else (string_of_symbols + string_of_numbers)

        elif self.password_can_contain_numbers.get():
            self.generated_password += string_of_numbers

        elif self.password_can_contain_symbols.get():
            self.generated_password += string_of_symbols

        self.label_generated_password.configure(text= f"Your password: {self.generated_password}")

    def generate_and_write_non_special_password(self):

        characters_to_generate_the_password = []

        if self.checkbox_password_options_uppercase.get():
            characters_to_generate_the_password.append(string.ascii_uppercase)

        if self.checkbox_password_options_lowercase.get():
            characters_to_generate_the_password.append(string.ascii_lowercase)

        if self.checkbox_password_options_numbers.get():
            characters_to_generate_the_password.append(string.digits)

        if self.checkbox_password_options_symbols.get():
            characters_to_generate_the_password.append(string.punctuation)

        self.generated_password = ""

        for _ in range(1, int(self.slider_password_length.get()) + 1):
            self.generated_password += random.choice(random.choice(characters_to_generate_the_password))

        self.label_generated_password.configure(text= f"Your password: {self.generated_password}")

if __name__ == "__main__":
    PythonApp().mainloop()