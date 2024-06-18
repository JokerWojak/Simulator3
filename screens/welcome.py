import os
import random
import json
import zipfile
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from screens.widgets.bargraph import BarGraphWidget
from persons.person import Person
from persons.save_main_character import save_main_character_to_json


class WelcomeScreen(Screen):
    def __init__(self, **kwargs):
        super(WelcomeScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        self.character_label = Label(text='', font_size='20sp', size_hint=(1, None), height=50)
        layout.add_widget(self.character_label)

        self.age_label = Label(text='Age: 0', font_size='20sp', size_hint=(1, None), height=50)
        layout.add_widget(self.age_label)

        self.bar_graph = BarGraphWidget(size_hint=(1, 0.6))
        layout.add_widget(self.bar_graph)

        button_layout = BoxLayout(size_hint=(1, None), height=50, orientation='horizontal', spacing=10)
        self.accept_button = Button(text="Accept", font_size='20sp')
        self.accept_button.bind(on_release=self.accept_pressed)
        button_layout.add_widget(self.accept_button)

        self.next_button = Button(text="Next", font_size='20sp')
        self.next_button.bind(on_release=self.next_pressed)
        button_layout.add_widget(self.next_button)

        load_button = Button(text="Load Game", font_size='20sp')
        load_button.bind(on_release=self.show_load_popup)
        button_layout.add_widget(load_button)

        layout.add_widget(button_layout)
        self.add_widget(layout)

        self.load_game()  # Load initial character data on screen creation

    def accept_pressed(self, *args):
        self.print_current_widget_data()
        self.update_graph_with_current_data()
        self.manager.current = 'game'

    def next_pressed(self, *args):
        new_character = Person()
        self.character_label.text = new_character.create_full_name()
        self.age_label.text = f"Age: {new_character.age}"

        new_values = {
            'Health': random.randint(0, 100),
            'Smarts': random.randint(0, 100),
            'Looks': random.randint(0, 100),
            'Happiness': random.randint(0, 100)
        }
        self.bar_graph.update_characteristics(new_values)
        self.save_game(new_character)

        self.print_current_widget_data()

    def save_game(self, main_character):
        save_main_character_to_json(main_character)

    def print_current_widget_data(self):
        print(f"Current Character: {self.character_label.text}")
        print(f"Current Age: {self.age_label.text}")
        current_traits = self.bar_graph.get_characteristics()
        print("Current Characteristics:")
        for trait, value in current_traits.items():
            print(f"{trait}: {value}")
        print("---")

    def update_graph_with_current_data(self):
        current_traits = self.bar_graph.get_characteristics()
        self.bar_graph.update_characteristics(current_traits)

    def show_load_popup(self, *args):
        popup_layout = BoxLayout(orientation='vertical')
        for game_name in self.find_saved_games():
            button = Button(text=game_name, size_hint_y=None, height=40)
            button.bind(on_release=lambda btn: self.load_game(btn.text))
            popup_layout.add_widget(button)

        popup = Popup(title='Load Game', content=popup_layout, size_hint=(0.8, 0.8))
        popup.open()

    def load_game(self, game_name=None):
        try:
            if game_name:
                game_state = load_game_data_from_zip(game_name)
                if game_state:
                    print(f"Loaded game state from {game_name}: {game_state}")
                    main_character_info = extract_main_character_info(game_state)
                    if main_character_info:
                        self.character_label.text = f"{main_character_info['first_name']} {main_character_info['last_name']}"
                        self.age_label.text = f"Age: {main_character_info['age']}"
                        self.bar_graph.update_characteristics(main_character_info['traits'])
                        print(f"Updated UI elements: character_label={self.character_label.text}, age_label={self.age_label.text}")
                        print("UI elements updated successfully.")
                    else:
                        print(f"No valid main character info extracted from {game_name}.")
                else:
                    print(f"Failed to load game state from {game_name}.")
            else:
                new_character = Person()
                print(f"Generated new character: {new_character.create_full_name()}, Age: {new_character.age}")
                new_values = {
                    'Health': random.randint(0, 100),
                    'Smarts': random.randint(0, 100),
                    'Looks': random.randint(0, 100),
                    'Happiness': random.randint(0, 100)
                }
                self.character_label.text = new_character.create_full_name()
                self.age_label.text = f"Age: {new_character.age}"
                self.bar_graph.update_characteristics(new_values)
                print(f"Updated UI elements: character_label={self.character_label.text}, age_label={self.age_label.text}")
                print("UI elements updated successfully.")
        except Exception as e:
            print(f"Error occurred while loading game: {str(e)}")

    def find_saved_games(self):
        saved_games_dir = os.path.join(os.getcwd(), 'run', 'saved_games')
        saved_games = [filename for filename in os.listdir(saved_games_dir) if filename.endswith(".zip")]
        return saved_games
