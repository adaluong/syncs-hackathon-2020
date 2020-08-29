'''
Requires Python 3.6 because of f-strings
'''

import kivy
kivy.require('1.11.1')
from kivy.config import Config
Config.set('graphics', 'width', '400')
Config.set('graphics', 'height', '800')
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.graphics import *

## This is the setup for each screen of our app (just sets background colour and
## screen ids)
Builder.load_string("""
<MenuScreen>:
    canvas.before:
        Color:
            rgba: 50/255, 65/255, 228/255, 1
        Rectangle:
            pos: self.pos
            size: self.size
    name: "menu_screen"
<TopicScreen>:
    canvas.before:
        Color:
            rgba: 50/255, 65/255, 228/255, 1
        Rectangle:
            pos: self.pos
            size: self.size
    name: "topic_screen"
<AttributesScreen>:
    canvas.before:
        Color:
            rgba: 50/255, 65/255, 228/255, 1
        Rectangle:
            pos: self.pos
            size: self.size
    name: "attribute_screen"
<OptionScreen>:
    canvas.before:
        Color:
            rgba: 50/255, 65/255, 228/255, 1
        Rectangle:
            pos: self.pos
            size: self.size
    name: "option_screen"
<FinalScreen>:
    canvas.before:
        Color:
            rgba: 50/255, 65/255, 228/255, 1
        Rectangle:
            pos: self.pos
            size: self.size
    name: "final_screen"
""")

## Dodgy af global values to keep track of everything
topic = ""
attributes = []
options = {}

'''
Algorithm that makes the decision - simply gives each attribute score a
weighting based on the priority of that attribute. The weightings are a linear
scale between 1 and 2, so for example if their are 3 attributes the weightings
(from highest to lowest) are [2, 1.5, 1] whereas if there are 5 attributes the
weightings are [2, 1.75, 1.5, 1.25, 1].

Take for example the following scenario where the topic is "Cafe" and the three
priorities from highest to lowest are "Prettiness", "Distance" and "Price".
Firstly the max score is:

10 * 2 + 10 * 1.5 + 10 * 1 = 45

We then grab each option and attribute scores and calculate a percentage
score relative to the max score.

<Cafe> : (<Prettiness>, <Distance>, <Price>) : <Equation> : <Score As %>

McCafe : (2, 10, 8) : 2 * 2 + 10 * 1.5 + 8 * 1 : 60%
The Grounds : (10, 2, 2) : 10 * 2 + 2 * 1.5 + 2 * 1 : 55.56%
Paper Boy : (8, 6, 6) : 8 * 2 + 6 * 1.5 + 6 * 1 : 68.89%

So the decision is to go to Paper Boy :)
'''

def calc_scores():
    # Distance between weights
    delta = 1.0 / (len(attributes) - 1)

    # Find max score
    max = sum([10 * (2 - delta * i) for i in range(len(attributes))])
    scores = {}

    # Calculate each score
    for opt in options:
        scores[opt] = sum([round(options[opt][i] * (2 - delta * i) * 100 / max, 2) for i in range(len(attributes))])

    # Return a dictionary of scores from highest to lowest
    return {k: v for k, v in sorted(scores.items(), key=lambda item: item[1], reverse=True)}

## The screen that first opens
class MenuScreen(Screen):
    def __init__(self, **kwargs):
        # Idk what this does but we need it? lmao
        super(MenuScreen, self).__init__(**kwargs)

        # Display the logo
        img = Image(source='logo.png')
        self.add_widget(img)

    # Switch to next screen when clicked
    def on_touch_down(self, touch):
        sm.switch_to(TopicScreen())

## The screen to enter what needs to be decided on
class TopicScreen(Screen):
    def __init__(self, **kwargs):
        # Idk what this does but we need it? lmao
        super(TopicScreen, self).__init__(**kwargs)

        # Create the textinput
        textinput = TextInput(background_color=[0.925, 0.949, 0.996, 1],
                              size=(360, 50),
                              size_hint=(None, None),
                              halign="center",
                              pos=(20, 375),
                              font_size=30,
                              font_name="aileron/Aileron-Bold.otf")
        textinput.bind(text=self.change_state)

        # Add textinput to screen
        self.add_widget(textinput)

        # Create the label (dodgy formatting)
        layout = FloatLayout(size=(300, 300))
        label = Label(text="Enter the topic you're\nundecided on:",
                      halign="center",
                      font_size=30,
                      pos_hint={'x':0, 'y':0.1},
                      font_name="aileron/Aileron-Bold.otf")

        # Add label to screen
        layout.add_widget(label)
        self.add_widget(layout)

    # Switch to next screen when user presses enter
    def change_state(self, instance, value):
        # Save the topic of the decision
        global topic

        if value and value[-1] == "\n":
            topic = value[:-1]
            sm.switch_to(AttributesScreen())

## The screen to enter the priorities
class AttributesScreen(Screen):
    def create_text_input():
        return TextInput(background_color=[0.925, 0.949, 0.996, 1],
                         size=(360, 50),
                         size_hint=(None, None),
                         halign="center",
                         font_size=30,
                         font_name="aileron/Aileron-Bold.otf")

    def __init__(self, **kwargs):
        # Idk what this does but we need it? lmao
        super(AttributesScreen, self).__init__(**kwargs)

        # Setup dodgy formatting
        self.layout = StackLayout(orientation='lr-tb', spacing=10, pos=(20, -10))

        # Create label
        label = Label(text="Enter your priorities for\nthe decision in order\nof importance:",
                      font_size=30,
                      halign="center",
                      size=(360, 150),
                      size_hint=(None, None),
                      font_name="aileron/Aileron-Bold.otf")

        # Create the textinputs
        self.textinputs = [AttributesScreen.create_text_input()]

        # Create the add button to add more priorities
        self.add_btn = Button(text="+",
                     halign="center",
                     valign="center",
                     font_size=40,
                     size=(50, 50),
                     size_hint=(None, None),
                     font_name="aileron/Aileron-Bold.otf")
        self.add_btn.bind(on_press=self.button_press)

        # Create dummy button for spacing
        self.dummy_btn = Button(halign="center",
                                valign="center",
                                background_color=[0, 0, 0, 0],
                                font_size=40,
                                size=(240, 50),
                                size_hint=(None, None),
                                font_name="aileron/Aileron-Bold.otf")

        # Create the submit button to move to next screen
        self.submit_btn = Button(text=">",
                                 halign="center",
                                 valign="center",
                                 font_size=40,
                                 size=(50, 50),
                                 size_hint=(None, None),
                                 font_name="aileron/Aileron-Bold.otf")
        self.submit_btn.bind(on_press=self.change_state)

        # Add all of above to the screen
        self.layout.add_widget(label)
        self.layout.add_widget(self.textinputs[0])
        self.layout.add_widget(self.add_btn)
        self.layout.add_widget(self.dummy_btn)
        self.layout.add_widget(self.submit_btn)
        self.add_widget(self.layout)

    # Add new priority when add button is pressed
    def button_press(self, instance):
        # Max 3 priorities
        if len(self.textinputs) < 3:
            # Create the new text box
            self.textinputs.append(AttributesScreen.create_text_input())

            # Remove the buttons
            self.layout.remove_widget(self.add_btn)
            self.layout.remove_widget(self.dummy_btn)
            self.layout.remove_widget(self.submit_btn)

            # Add the new text box underneath and add back the buttons
            self.layout.add_widget(self.textinputs[-1])
            self.layout.add_widget(self.add_btn)
            self.layout.add_widget(self.dummy_btn)
            self.layout.add_widget(self.submit_btn)

    # Switch to next screen when submit button is pressed
    def change_state(self, instance):
        # Save the priorities
        global attributes
        attributes = [i.text for i in self.textinputs]

        sm.switch_to(OptionScreen())

## The screen to enter the options and scores
class OptionScreen(Screen):
    def create_label_one():
        return Label(text=f"{topic}:",
                     size=(100, 50),
                     size_hint=(None, None),
                     font_size=32,
                     font_name="aileron/Aileron-Bold.otf")

    def create_label_two(attr):
        return Label(text=f"{attr}:",
                     size=(100, 30),
                     size_hint=(None, None),
                     font_size=17,
                     font_name="aileron/Aileron-Bold.otf")

    def create_text_input_one():
        return TextInput(background_color=[0.925, 0.949, 0.996, 1],
                         size=(255, 50),
                         size_hint=(None, None),
                         halign="center",
                         font_size=30,
                         font_name="aileron/Aileron-Bold.otf")

    def create_text_input_two(attr):
        return TextInput(background_color=[0.925, 0.949, 0.996, 1],
                         size=(255, 30),
                         size_hint=(None, None),
                         halign="center",
                         font_size=15,
                         font_name="aileron/Aileron-Bold.otf")

    def create_gap():
        return Button(halign="center",
                      valign="center",
                      background_color=[0, 0, 0, 0],
                      font_size=40,
                      size=(380, 20),
                      size_hint=(None, None),
                      font_name="aileron/Aileron-Bold.otf")

    def __init__(self, **kwargs):
        # Idk what this does but we need it? lmao
        super(OptionScreen, self).__init__(**kwargs)

        # Setup dodgy formatting
        self.layout = StackLayout(orientation='lr-tb', spacing=10, pos=(20, -10))

        # Create the labels
        label = Label(text=f"Enter {topic} options and\nscores for each priority\nout of 10:",
                      halign="center",
                      font_size=25,
                      size=(360, 100),
                      size_hint=(None, None),
                      font_name="aileron/Aileron-Bold.otf")

        self.option_label = OptionScreen.create_label_one()

        self.attribute_labels = []
        for attr in attributes:
            self.attribute_labels.append(OptionScreen.create_label_two(attr))

        # Create the textinputs
        self.option_textinputs = [OptionScreen.create_text_input_one()]
        self.attribute_textinputs = []
        for attr in attributes:
            self.attribute_textinputs.append([OptionScreen.create_text_input_two(attr)])

        # Create the add button
        self.add_btn = Button(text="+",
                              halign="center",
                              valign="center",
                              font_size=40,
                              size=(50, 50),
                              size_hint=(None, None),
                              font_name="aileron/Aileron-Bold.otf")
        self.add_btn.bind(on_press=self.button_press)

        # Create dummy button
        self.dummy_btn = Button(halign="center",
                                valign="center",
                                background_color=[0, 0, 0, 0],
                                font_size=40,
                                size=(240, 50),
                                size_hint=(None, None),
                                font_name="aileron/Aileron-Bold.otf")

        # Create the submit button
        self.submit_btn = Button(text=">",
                                 halign="center",
                                 valign="center",
                                 font_size=40,
                                 size=(50, 50),
                                 size_hint=(None, None),
                                 font_name="aileron/Aileron-Bold.otf")
        self.submit_btn.bind(on_press=self.change_state)

        # Create the gap
        self.gap_btn = OptionScreen.create_gap()

        # Add everything to the screen
        self.layout.add_widget(label)
        self.layout.add_widget(self.option_label)
        self.layout.add_widget(self.option_textinputs[0])

        for i in range(len(attributes)):
            self.layout.add_widget(self.attribute_labels[i])
            self.layout.add_widget(self.attribute_textinputs[i][0])

        self.layout.add_widget(self.add_btn)
        self.layout.add_widget(self.dummy_btn)
        self.layout.add_widget(self.submit_btn)
        self.add_widget(self.layout)

    def button_press(self, instance):
        if len(self.option_textinputs) < 3:
            # Recreate Labels and gap
            self.option_label = OptionScreen.create_label_one()

            self.attribute_labels = []
            for attr in attributes:
                self.attribute_labels.append(OptionScreen.create_label_two(attr))

            self.gap_btn = OptionScreen.create_gap()

            self.option_textinputs.append(OptionScreen.create_text_input_one())

            for i in range(len(attributes)):
                self.attribute_textinputs[i].append(OptionScreen.create_text_input_two(attr))

            # Remove buttons
            self.layout.remove_widget(self.add_btn)
            self.layout.remove_widget(self.dummy_btn)
            self.layout.remove_widget(self.submit_btn)

            # Add a gap
            self.layout.add_widget(self.gap_btn)

            # Add the labels and textinputs
            self.layout.add_widget(self.option_label)
            self.layout.add_widget(self.option_textinputs[-1])

            for i in range(len(attributes)):
                self.layout.add_widget(self.attribute_labels[i])
                self.layout.add_widget(self.attribute_textinputs[i][-1])

            # Add back the buttons
            self.layout.add_widget(self.add_btn)
            self.layout.add_widget(self.dummy_btn)
            self.layout.add_widget(self.submit_btn)

    # Switch to next screen when submit button is pressed
    def change_state(self, instance):
        # Save the options and scores
        global options

        options = {}
        for i in range(len(self.option_textinputs)):
            opt = self.option_textinputs[i].text
            options[opt] = [int(attr[i].text) for attr in self.attribute_textinputs]

        sm.switch_to(FinalScreen())

## The screen that tells you the decision
class FinalScreen(Screen):
    def __init__(self, **kwargs):
        # Idk what this does but we need it? lmao
        super(FinalScreen, self).__init__(**kwargs)

        # Calculate Scores
        scores = calc_scores()

        # Create a label that prints the decision
        label = Label(text="\n\n".join([f"The {topic} you\nshould choose is:\n"] + [i + ": " + str(scores[i]) + "%" for i in scores]),
                      halign="center",
                      font_size=35,
                      font_name="aileron/Aileron-Bold.otf")

        # Add to the screen
        self.add_widget(label)

    # Switch to next screen when clicked
    def on_touch_down(self, touch):
        # Change screen when button is pressed
        sm.switch_to(MenuScreen())

sm = ScreenManager()
sm.add_widget(MenuScreen())


class EddyApp(App):

    def build(self):
        return sm


if __name__ == "__main__":
    EddyApp().run()
