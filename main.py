import customtkinter
import phonenumbers
from phonenumbers import geocoder, carrier

customtkinter.set_appearance_mode("Dart")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("CallQ.py")
        self.geometry(f"{800}x{265}")

        # create main entry and button
        self.entry = customtkinter.CTkEntry(self, placeholder_text="Write phone number")
        self.entry.grid(row=3, column=1, padx=(20, 0), pady=(20, 20), sticky="nsew")

        self.main_button_1 = customtkinter.CTkButton(master=self, fg_color="transparent", border_width=2,
                                                     text_color=("gray10", "#DCE4EE"), text="Enter",
                                                     command=self.button_click_event)
        self.main_button_1.grid(row=3, column=2, padx=(20, 20), pady=(20, 20), sticky="nsew")

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="CallQ",
                                                 font=customtkinter.CTkFont(size=45, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionmenu = customtkinter.CTkOptionMenu(self.sidebar_frame,
                                                                      values=["Light", "Dark", "System"],
                                                                      command=self.change_appearance_mode_event)
        self.appearance_mode_optionmenu.grid(row=6, column=0, padx=20, pady=(10, 10))
        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.scaling_optionmenu = customtkinter.CTkOptionMenu(self.sidebar_frame,
                                                              values=["80%", "90%", "100%", "110%", "120%"],
                                                              command=self.change_scaling_event)
        self.scaling_optionmenu.grid(row=8, column=0, padx=20, pady=(10, 20))

        self.label = customtkinter.CTkLabel(self, font=("Times", 18, "bold"), text_color='#1f6aa5',
                                            text="""Hello! Enter the phone number and get information about it.
 The format of entering the number is not important. All variants are allowed,
 for example: +x xxx xxx xx xx, +x (xxx) xxx xx, +x-xxx-xx-xx-xxx, etc.
   The main thing is not to forget the "+" sign before the start of the number.""")
        self.label.grid(row=1, column=1, columnspan=2, pady=(20, 0), sticky="nsew")

        self.appearance_mode_optionmenu.set("Dark")
        self.scaling_optionmenu.set("100%")

        self.grid_columnconfigure(1, weight=4)
        self.grid_columnconfigure(2, weight=1)

    def button_click_event(self):
        input_number = self.entry.get()  # Get the input text from the entry
        try:
            number = phonenumbers.parse(input_number)
            if phonenumbers.is_valid_number(number):
                number_type = phonenumbers.number_type(number)
                country = geocoder.description_for_number(number, 'ru')
                country_name = geocoder.country_name_for_number(number, 'ru')
                carrier_name = carrier.name_for_number(number, 'ru')

                def type_phonenumber(number_type):
                    if number_type == 0:
                        return "Fixed line"
                    elif number_type == 1:
                        return "Mobile phone"
                    elif number_type == 2:
                        return "Fixed line or mobile phone (In some regions (e.g. the USA), " \
                               "it is impossible to distinguish between fixed-line and mobile numbers " \
                               "by looking at the phone number itself.)"
                    elif number_type == 3:
                        return "Toll free"
                    elif number_type == 4:
                        return "Premium rate"
                    elif number_type == 5:
                        return "Shared cost (The cost of this call is shared between the caller and the recipient, " \
                               "and is hence typically less than PREMIUM_RATE calls.)"
                    elif number_type == 6:
                        return "Voip (Voice over IP numbers. This includes TSoIP (Telephony Service over IP))"
                    elif number_type == 7:
                        return "Personal number (A personal number is associated with a particular person, and may be " \
                               "routed to either a MOBILE or FIXED_LINE number.)"
                    elif number_type == 8:
                        return "Pager"
                    elif number_type == 9:
                        return """UAN (Used for “Universal Access Numbers" or "Company Numbers".
                                 They may be further routed to specific offices, but allow one number to be used for a company.)"""

                if country == country_name:
                    result_text = f"Number type: {type_phonenumber(number_type)}\nCountry: {country}\nCarrier: {carrier_name}"
                else:
                    result_text = f"Number type: {type_phonenumber(number_type)}\nCountry: {country}\nCountry Name: {country_name}\nCarrier: {carrier_name}"
            else:
                result_text = """This is an invalid number.
            Check that the input is correct."""
            self.label.configure(text=result_text, font=("Times", 24, "bold"))
        except:
            self.label.configure(text="""An input error, or the "+" sign is missing,
        or the phone number length is incorrect
        or invalid characters are specified.""", font=("Times", 24, "bold"))

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)


if __name__ == "__main__":
    app = App()
    app.change_appearance_mode_event("Dart")
    app.mainloop()
