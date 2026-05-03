# keyword_patterns.py
# Expanded fuzzy patterns for diet, dieting, calories, protein, meal prep, and resets.

CHANGE_WORDS = [
    "change", "switch", "replace", "update", "adjust", "set",
    "target", "begin", "start", "stop", "quit", "end",
    "no longer", "not", "instead", "no more", "drop", "done with"
]

RESET_PHRASES = [
    "reset my keywords",
    "reset everything",
    "clear my preferences",
    "wipe my preferences",
    "delete all my preferences",
    "start over",
    "reset all",
    "reset it all",
    "reset settings"
]

# Diet start patterns
DIET_START_PATTERNS = {
    "vegan": [
        "i want to start a vegan diet",
        "i want to begin a vegan diet",
        "i want to go vegan",
        "i want to be vegan",
        "i want to switch to a vegan diet",
        "i want to change to a vegan diet",
        "i want to follow a vegan diet",
        "i want to adopt a vegan diet",
        "i want to try being vegan",
        "im starting a vegan diet",
        "im going vegan",
        "im becoming vegan",
        "im switching to vegan",
        "im changing my diet to vegan",
        "im transitioning to vegan",
        "make me vegan",
        "switch me to vegan",
        "set my diet to vegan"
    ],
    "vegetarian": [
        "i want to start a vegetarian diet",
        "i want to go vegetarian",
        "i want to be vegetarian",
        "im becoming vegetarian",
        "im switching to vegetarian",
        "make me vegetarian",
        "set my diet to vegetarian"
    ],
    "pescatarian": [
        "i want to start a pescatarian diet",
        "i want to go pescatarian",
        "i want to be pescatarian",
        "im becoming pescatarian",
        "im switching to pescatarian",
        "make me pescatarian",
        "set my diet to pescatarian"
    ]
}

# Diet stop patterns
DIET_STOP_PATTERNS = [
    "i am no longer vegan",
    "im no longer vegan",
    "im not vegan anymore",
    "i am not vegan anymore",
    "i want to stop being vegan",
    "i want to quit being vegan",
    "i want to change my diet so im not vegan",
    "i want to switch away from vegan",
    "i want to stop following a vegan diet",
    "i want to end my vegan diet",
    "i want to drop the vegan diet",
    "im done being vegan",
    "im stopping vegan",
    "im quitting vegan",
    "im transitioning off vegan",
    "i quit vegan",
    "im done with vegan",
    "i stopped being vegan"
]

DIETING_YES = [
    "i am dieting",
    "im dieting",
    "i want to start dieting",
    "i want to begin dieting",
    "i want to go on a diet",
    "i want to be on a diet",
    "im starting a diet",
    "im going on a diet",
    "im beginning a diet",
    "im trying to diet",
    "im trying to lose weight",
    "im trying to cut calories",
    "im trying to slim down"
]

DIETING_NO = [
    "i am not dieting",
    "im not dieting",
    "im no longer dieting",
    "i want to stop dieting",
    "i want to quit dieting",
    "i want to end my diet",
    "im done dieting",
    "im taking a break from dieting",
    "im not on a diet anymore"
]

MEAL_PREP_YES = [
    "i want to start meal prepping",
    "i want to begin meal prepping",
    "i want to meal prep",
    "i want to prep my meals",
    "im starting meal prep",
    "im going to meal prep",
    "im beginning meal prep",
    "im prepping meals this week",
    "i want to get into meal prepping"
]

MEAL_PREP_NO = [
    "i want to stop meal prepping",
    "im not meal prepping anymore",
    "im done meal prepping",
    "i want to quit meal prepping",
    "i want to end meal prepping"
]

CALORIE_PATTERNS = [
    "set my calorie goal to",
    "i want to set my calorie goal to",
    "my calorie target should be",
    "make my calories",
    "change my calories to",
    "i want",
    "i want to eat",
    "my new calorie goal is",
    "i no longer want a calorie goal of",
    "instead",
    "calories",
    "calorie target",
    "set calories to",
    "set my calories to"
]

PROTEIN_PATTERNS = [
    "i want",
    "set my protein goal to",
    "change my protein goal to",
    "update my protein to",
    "adjust my protein to",
    "i want high protein",
    "i want normal protein",
    "i want no protein",
    "i want zero protein",
    "i want to target",
    "i want to aim for",
    "protein goal",
    "set protein to"
]
