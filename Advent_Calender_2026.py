# RGB Xmas Tree Advent Calendar by Boughton-Shields Creations

import json
import os
import random
from time import sleep, strftime
from tree import RGBXmasTree

# Setup Tree
tree = RGBXmasTree()
tree.brightness = 0.1

STATE_FILE = "advent_state.json"
STAR_LED = 3  # LED index for the star at the top

# Available colours (R, G, B)
COLOURS = [
    (1, 0, 0),    # Red
    (0, 1, 0),    # Green
    (0, 0, 1),    # Blue
    (1, 1, 0),    # Yellow
    (0, 1, 1),    # Cyan / Turquoise
    (1, 0, 1),    # Magenta / Purple
    (1, 0.5, 0),  # Orange
]


def load_state():
    """Load saved LED states from a JSON file."""
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    return {}


def save_state(state):
    """Save current LED states to a JSON file."""
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=4)


def show_rainbow():
    """Display the rainbow pattern for Dec 26th-31st."""
    branches = [
        ([0, 1, 2], (1, 0, 0)),       # Red
        ([22, 23, 24], (1, 0.5, 0)),  # Orange
        ([19, 20, 21], (1, 1, 0)),    # Yellow
        ([4, 5, 6], (0, 1, 0)),       # Green
        ([10, 11, 12], (0, 1, 1)),    # Turquoise
        ([16, 17, 18], (0, 0, 1)),    # Blue
        ([13, 14, 15], (1, 0, 1)),    # Purple
        ([7, 8, 9], (1, 0, 0.25)),    # Light Purple
    ]
    for leds, colour in branches:
        for led in leds:
            tree[led].color = colour
    tree[STAR_LED].color = (1, 1, 1)  # White star


def advent(today_str):
    day = int(today_str)
    state = load_state()

    # Reset state if we are outside the 1-25 range or starting fresh
    if day < 1:
        return

    if day <= 25:
        if day == 25:
            print("Merry Christmas!")
        else:
            print(f"{today_str}-12")

        # Ensure every day up to 'today' has a randomly assigned LED and colour
        used_leds = {entry["led"] for entry in state.values()}
        available_leds = [
            i for i in range(25) if i != STAR_LED and i not in used_leds
        ]

        for d in range(1, day + 1):
            d_key = str(d)
            if d_key not in state and available_leds:
                chosen_led = random.choice(available_leds)
                available_leds.remove(chosen_led)
                chosen_colour = random.choice(COLOURS)
                state[d_key] = {"led": chosen_led, "colour": chosen_colour}
                save_state(state)

        # Light up all LEDs sequentially from Day 1 up to today
        for d in range(1, day + 1):
            d_key = str(d)
            if d_key in state:
                led_index = state[d_key]["led"]
                led_colour = tuple(state[d_key]["colour"])
                tree[led_index].color = led_colour
                sleep(0.5)

        # On Christmas Day (25th), turn on the white star last
        if day == 25:
            tree[STAR_LED].color = (1, 1, 1)

    # 26th - 31st Dec: Rainbow Tree
    elif day > 25:
        print(f"{today_str}-12")
        show_rainbow()


# Main Loop
try:
    while True:
        today = strftime("%d")
        month = strftime("%B")

        # Overrides for testing
        #today = "01"
        #month = "December"

        if month == "December":
            print("It's Christmas Time!")
            advent(today)
        else:
            print("It's not Christmas Time yet! Keep waiting!")
            # Clear saved state outside December so it's ready for next year
            if os.path.exists(STATE_FILE):
                os.remove(STATE_FILE)
            tree.color = (0, 0, 0)

        # Wait 1hr before re-checking date
        sleep(3600)

except KeyboardInterrupt:
    tree.color = (0, 0, 0)
    tree.close()
