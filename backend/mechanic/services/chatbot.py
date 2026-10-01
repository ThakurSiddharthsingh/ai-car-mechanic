"""
AI Car Mechanic - Conversation Engine

This file handles the conversational part of the mechanic assistant.

It:
- understands common car problems
- remembers previous user answers
- handles short answers such as:
    yes
    no
    yesterday
    continuously
    sometimes
    hard
    soft
    normal
- asks one useful question at a time
- supports multiple vehicle systems
- avoids repeatedly asking the same generic question
"""

import re


# =========================================================
# CAR KEYWORDS
# =========================================================

CAR_KEYWORDS = [
    # General
    "car",
    "vehicle",
    "automobile",
    "my car",
    "my vehicle",

    # Engine
    "engine",
    "motor",
    "overheat",
    "overheating",
    "overheated",
    "coolant",
    "radiator",
    "thermostat",
    "water pump",

    # Brakes
    "brake",
    "brakes",
    "braking",
    "brake pedal",
    "brake pad",
    "brake pads",
    "rotor",
    "disc brake",

    # Tyres / wheels
    "tyre",
    "tyres",
    "tire",
    "tires",
    "puncture",
    "flat tyre",
    "flat tire",
    "wheel",
    "wheels",
    "rim",
    "rims",
    "wheel alignment",
    "wheel balancing",

    # Steering / suspension
    "steering",
    "steering wheel",
    "suspension",
    "shock absorber",
    "shocks",
    "strut",
    "struts",
    "alignment",

    # Battery / electrical
    "battery",
    "alternator",
    "starter",
    "starting",
    "won't start",
    "wont start",
    "doesn't start",
    "doesnt start",
    "electrical",
    "electric",
    "fuse",
    "fuses",
    "wiring",

    # Transmission
    "clutch",
    "gear",
    "gears",
    "gearbox",
    "transmission",
    "manual transmission",
    "automatic transmission",

    # Fluids
    "oil",
    "engine oil",
    "oil leak",
    "coolant",
    "brake fluid",
    "transmission fluid",
    "fluid leak",
    "leaking fluid",

    # Fuel
    "fuel",
    "petrol",
    "gasoline",
    "diesel",
    "fuel pump",
    "fuel injector",
    "injector",

    # AC / heating
    "ac",
    "a/c",
    "air conditioner",
    "air conditioning",
    "heater",
    "heating",
    "cooling",

    # Exhaust / smoke
    "smoke",
    "exhaust",
    "exhaust smoke",
    "muffler",
    "catalytic converter",

    # Lights / electrical accessories
    "headlight",
    "headlights",
    "tail light",
    "tail lights",
    "indicator",
    "indicators",
    "turn signal",
    "turn signals",
    "fog light",
    "dashboard light",
    "warning light",
    "check engine",
    "abs light",

    # Other
    "horn",
    "noise",
    "sound",
    "vibration",
    "shaking",
    "rattling",
    "clicking",
    "warning",
]


# =========================================================
# NORMALIZATION
# =========================================================

def normalize_text(text):
    """Normalize user text for reliable keyword matching."""

    if text is None:
        return ""

    text = str(text).lower().strip()

    # Common spelling variations
    replacements = {
        "tires": "tyres",
        "tire": "tyre",
        "brakes": "brake",
        "gears": "gear",
        "wont": "won't",
        "doesnt": "doesn't",
        "cant": "can't",
        "isnt": "isn't",
        "dont": "don't",
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    # Normalize whitespace
    text = re.sub(r"\s+", " ", text)

    return text


# =========================================================
# CAR RELATED CHECK
# =========================================================

def is_car_related(message: str) -> bool:
    """Check whether text contains a vehicle/mechanical topic."""

    text = normalize_text(message)

    return any(
        keyword in text
        for keyword in CAR_KEYWORDS
    )


# =========================================================
# CATEGORY DETECTION
# =========================================================

def detect_category(text):
    """
    Detect the main vehicle system involved.

    Returns:
        string category or None
    """

    text = normalize_text(text)

    # Order matters.

    if any(
        word in text
        for word in [
            "brake",
            "braking",
            "brake pedal",
            "brake pad",
            "brake pads",
            "rotor",
        ]
    ):
        return "brake"

    if any(
        word in text
        for word in [
            "tyre",
            "puncture",
            "flat tyre",
            "wheel",
            "rim",
            "alignment",
            "balancing",
        ]
    ):
        return "tyre"

    if any(
        word in text
        for word in [
            "steering",
            "suspension",
            "shock absorber",
            "strut",
        ]
    ):
        return "steering"

    if any(
        word in text
        for word in [
            "clutch",
            "gearbox",
            "transmission",
            "gear",
        ]
    ):
        return "transmission"

    if any(
        word in text
        for word in [
            "battery",
            "alternator",
            "starter",
            "electrical",
            "fuse",
            "wiring",
        ]
    ):
        return "electrical"

    if any(
        word in text
        for word in [
            "overheat",
            "overheating",
            "coolant",
            "radiator",
            "thermostat",
            "water pump",
        ]
    ):
        return "cooling"

    if any(
        word in text
        for word in [
            "engine",
            "motor",
            "knocking",
            "ticking",
            "stalling",
            "stall",
            "losing power",
            "loss of power",
        ]
    ):
        return "engine"

    if any(
        word in text
        for word in [
            "oil",
            "engine oil",
            "oil leak",
        ]
    ):
        return "oil"

    if any(
        word in text
        for word in [
            "fuel",
            "petrol",
            "gasoline",
            "diesel",
            "fuel pump",
            "injector",
        ]
    ):
        return "fuel"

    if any(
        word in text
        for word in [
            "ac",
            "a/c",
            "air conditioner",
            "air conditioning",
            "heater",
        ]
    ):
        return "ac"

    if any(
        word in text
        for word in [
            "smoke",
            "exhaust",
            "muffler",
            "catalytic",
        ]
    ):
        return "exhaust"

    if any(
        word in text
        for word in [
            "headlight",
            "headlights",
            "tail light",
            "tail lights",
            "indicator",
            "turn signal",
            "fog light",
            "warning light",
            "check engine",
            "abs light",
        ]
    ):
        return "lights"

    if "horn" in text:
        return "horn"

    return None


# =========================================================
# GENERAL INFORMATION DETECTION
# =========================================================

def detect_frequency(text):
    text = normalize_text(text)

    if any(
        phrase in text
        for phrase in [
            "continuously",
            "continuous",
            "constantly",
            "all the time",
            "every time",
            "always",
            "non stop",
            "nonstop",
        ]
    ):
        return "continuous"

    if any(
        phrase in text
        for phrase in [
            "sometimes",
            "occasionally",
            "once in a while",
            "intermittent",
            "intermittently",
        ]
    ):
        return "intermittent"

    return None


def detect_onset(text):
    text = normalize_text(text)

    if "today" in text:
        return "today"

    if "yesterday" in text:
        return "yesterday"

    if "last night" in text:
        return "last night"

    if "last week" in text:
        return "last week"

    if "last month" in text:
        return "last month"

    if "recently" in text:
        return "recently"

    if "few days" in text:
        return "a few days ago"

    if "few weeks" in text:
        return "a few weeks ago"

    if "for months" in text:
        return "for several months"

    if "for years" in text:
        return "for a long time"

    return None


def detect_yes_no(text):
    text = normalize_text(text)

    yes_words = [
        "yes",
        "yeah",
        "yep",
        "yup",
        "correct",
        "right",
        "true",
        "it does",
        "it is",
        "that's right",
    ]

    no_words = [
        "no",
        "nope",
        "not",
        "it doesn't",
        "it does not",
        "it isn't",
        "it is not",
    ]

    if text in yes_words:
        return "yes"

    if text in no_words:
        return "no"

    return None


# =========================================================
# SYMPTOM DETECTION
# =========================================================

def detect_common_symptoms(text):
    text = normalize_text(text)

    symptoms = []

    symptom_map = {
        "noise": [
            "noise",
            "sound",
            "squeaking",
            "squeak",
            "squealing",
            "squeal",
            "grinding",
            "scraping",
            "rattling",
            "humming",
            "thumping",
            "clicking",
            "click",
            "knocking",
            "ticking",
        ],
        "vibration": [
            "vibration",
            "vibrating",
            "shaking",
            "shake",
            "judder",
            "juddering",
        ],
        "leak": [
            "leak",
            "leaking",
            "leaked",
            "fluid under",
            "liquid under",
            "puddle",
        ],
        "smoke": [
            "smoke",
            "smoking",
        ],
        "overheating": [
            "overheat",
            "overheating",
            "hot",
            "temperature high",
            "temperature rising",
            "temperature gauge high",
        ],
        "starting": [
            "won't start",
            "doesn't start",
            "not starting",
            "cannot start",
            "can't start",
            "car won't start",
            "car does not start",
        ],
        "power_loss": [
            "losing power",
            "loss of power",
            "low power",
            "poor acceleration",
            "not accelerating",
            "slow acceleration",
        ],
        "pulling": [
            "pulling",
            "pulls left",
            "pulls right",
            "pull to the left",
            "pull to the right",
            "car pulls",
            "vehicle pulls",
        ],
        "pressure": [
            "low pressure",
            "tyre pressure",
            "tire pressure",
            "underinflated",
            "under inflated",
        ],
        "puncture": [
            "puncture",
            "flat tyre",
            "flat tire",
            "nail in tyre",
            "nail in tire",
        ],
        "wear": [
            "uneven wear",
            "tyre wear",
            "tire wear",
            "worn tyre",
            "worn tire",
            "worn out tyre",
        ],
    }

    for symptom, phrases in symptom_map.items():
        if any(
            phrase in text
            for phrase in phrases
        ):
            symptoms.append(symptom)

    return symptoms


# =========================================================
# BRAKE HELPERS
# =========================================================

def detect_brake_pedal_condition(text):
    text = normalize_text(text)

    if "spongy" in text:
        return "spongy"

    if "soft pedal" in text or "pedal is soft" in text:
        return "soft"

    if "hard pedal" in text or "pedal is hard" in text:
        return "hard"

    if "normal pedal" in text or "pedal is normal" in text:
        return "normal"

    return None


def detect_brake_timing(text):
    text = normalize_text(text)

    braking = any(
        phrase in text
        for phrase in [
            "when i brake",
            "when i press the brake",
            "press the brake",
            "while braking",
            "during braking",
            "when braking",
            "every time i brake",
            "braking",
        ]
    )

    driving = any(
        phrase in text
        for phrase in [
            "while driving",
            "when driving",
            "during driving",
            "at high speed",
            "at low speed",
        ]
    )

    if braking and driving:
        return "both"

    if braking:
        return "braking"

    if driving:
        return "driving"

    return None


# =========================================================
# CONVERSATION HISTORY HELPERS
# =========================================================

def build_text_from_history(conversation_history, current_message):
    """
    Supports both:
        ["tyres", "yesterday"]

    and:

        [
            {"sender": "user", "message": "tyres"},
            {"sender": "bot", "message": "..."},
        ]
    """

    parts = []

    for item in conversation_history or []:

        if isinstance(item, dict):
            if item.get("sender") == "user":
                parts.append(
                    str(item.get("message", ""))
                )

        else:
            parts.append(str(item))

    parts.append(str(current_message))

    return normalize_text(" ".join(parts))


def get_last_bot_question(conversation_history):
    """
    Find the latest question asked by the bot.
    """

    for item in reversed(conversation_history or []):

        if isinstance(item, dict):

            if item.get("sender") == "bot":

                message = str(
                    item.get("message", "")
                ).strip()

                if "?" in message:
                    return message

    return ""


# =========================================================
# RESPONSE BUILDER
# =========================================================

def response(
    text,
    question=None,
    needs_follow_up=False,
):
    result = {
        "is_car_related": True,
        "response": text,
        "needs_follow_up": needs_follow_up,
    }

    if question:
        result["follow_up_question"] = question

    return result


# =========================================================
# MAIN CHATBOT
# =========================================================

def generate_basic_response(
    message: str,
    conversation_history=None
):
    """
    Generate a rule-based mechanic conversation.

    The chatbot intentionally asks one major question at a time.
    """

    if conversation_history is None:
        conversation_history = []

    current = normalize_text(message)

    full_history = build_text_from_history(
        conversation_history,
        message,
    )

    # =====================================================
    # GREETING
    # =====================================================

    greetings = [
        "hello",
        "hi",
        "hey",
        "hii",
        "good morning",
        "good afternoon",
        "good evening",
    ]

    if current in greetings:

        return {
            "is_car_related": True,
            "response": (
                "Hello! I'm your AI Car Mechanic. "
                "Tell me what's wrong with your car."
            ),
            "needs_follow_up": False,
        }

    # =====================================================
    # NON-CAR MESSAGE
    # =====================================================

    if not is_car_related(full_history):

        return {
            "is_car_related": False,
            "response": (
                "I'm an AI car mechanic assistant. "
                "I can help with car and mechanical issues "
                "such as engine problems, brakes, tyres, "
                "battery, overheating, steering, suspension, "
                "transmission, AC, and other vehicle problems."
            ),
            "needs_follow_up": False,
        }

    category = detect_category(full_history)

    frequency = detect_frequency(full_history)

    onset = detect_onset(full_history)

    symptoms = detect_common_symptoms(full_history)

    # =====================================================
    # BRAKES
    # =====================================================

    if category == "brake":

        pedal = detect_brake_pedal_condition(full_history)

        timing = detect_brake_timing(full_history)

        brake_symptom = any(
            item in symptoms
            for item in [
                "noise",
                "vibration",
                "pulling",
            ]
        )

        # User only says "brakes"
        if not brake_symptom and pedal is None:

            return response(
                "I can help investigate the brake problem.",
                (
                    "What are you noticing with the brakes — "
                    "noise, grinding, vibration, pulling, "
                    "a soft pedal, a hard pedal, or something else?"
                ),
                True,
            )

        # Brake symptom known, timing unknown
        if brake_symptom and timing is None:

            return response(
                "Thanks. I understand the brake symptom.",
                (
                    "Does it happen mainly when you press "
                    "the brake, while driving, or in both situations?"
                ),
                True,
            )

        # Timing known, pedal unknown
        if timing in ["braking", "both"] and pedal is None:

            return response(
                "Thanks. I understand that the problem "
                "happens during braking.",
                (
                    "How does the brake pedal feel — "
                    "soft, hard, spongy, or normal?"
                ),
                True,
            )

        # No onset information
        if onset is None:

            return response(
                "Thanks. I have the main brake symptoms.",
                (
                    "When did you first notice this problem?"
                ),
                True,
            )

        return response(
            "Thanks. I have enough information about "
            "the brake symptoms to proceed with the diagnosis.",
            None,
            False,
        )

    # =====================================================
    # TYRES / WHEELS
    # =====================================================

    if category == "tyre":

        tyre_symptom = any(
            item in symptoms
            for item in [
                "noise",
                "vibration",
                "pressure",
                "puncture",
                "wear",
                "pulling",
            ]
        )

        # Only "tyres"
        if not tyre_symptom:

            return response(
                "I can help investigate the tyre problem.",
                (
                    "What exactly are you noticing — "
                    "low tyre pressure, a flat tyre or puncture, "
                    "vibration, unusual noise, uneven wear, "
                    "or the car pulling to one side?"
                ),
                True,
            )

        # Need frequency
        if frequency is None:

            return response(
                "Thanks. I understand the tyre symptom.",
                (
                    "Does the problem happen continuously, "
                    "or only under certain conditions such as "
                    "at a particular speed, while braking, "
                    "or while turning?"
                ),
                True,
            )

        # Need onset
        if onset is None:

            return response(
                "Thanks. I understand when the tyre problem occurs.",
                (
                    "When did you first notice the problem?"
                ),
                True,
            )

        return response(
            "Thanks. I have enough information about "
            "the tyre problem to proceed with the diagnosis.",
            None,
            False,
        )

    # =====================================================
    # ENGINE
    # =====================================================

    if category == "engine":

        engine_symptoms = any(
            item in symptoms
            for item in [
                "noise",
                "smoke",
                "overheating",
                "starting",
                "power_loss",
            ]
        )

        if not engine_symptoms:

            return response(
                "I can help investigate the engine problem.",
                (
                    "What are you noticing — the engine won't start, "
                    "loss of power, overheating, unusual noise, "
                    "smoke, stalling, or something else?"
                ),
                True,
            )

        # Serious overheating
        if "overheating" in symptoms:

            if not any(
                phrase in full_history
                for phrase in [
                    "steam",
                    "coolant",
                    "temperature gauge",
                    "red zone",
                    "leaking",
                ]
            ):

                return response(
                    "An overheating engine should be handled carefully.",
                    (
                        "Is there steam, coolant leaking, or is "
                        "the temperature gauge reaching the red zone?"
                    ),
                    True,
                )

        if onset is None:

            return response(
                "Thanks. I understand the main engine symptom.",
                "When did you first notice this problem?",
                True,
            )

        return response(
            "Thanks. I have enough information about "
            "the engine problem to proceed with the diagnosis.",
            None,
            False,
        )

    # =====================================================
    # COOLING / OVERHEATING
    # =====================================================

    if category == "cooling":

        if "overheating" not in symptoms:

            return response(
                "I can help investigate the cooling system.",
                (
                    "Is the engine overheating, losing coolant, "
                    "leaking coolant, or is the temperature gauge "
                    "behaving unusually?"
                ),
                True,
            )

        if not any(
            phrase in full_history
            for phrase in [
                "steam",
                "coolant",
                "leak",
                "temperature gauge",
                "red zone",
            ]
        ):

            return response(
                "I understand that the engine is overheating.",
                (
                    "Is there any steam or coolant leaking, "
                    "or is the temperature gauge simply "
                    "rising above normal?"
                ),
                True,
            )

        return response(
            "Thanks. I have enough information about "
            "the cooling problem to proceed with the diagnosis.",
            None,
            False,
        )

    # =====================================================
    # BATTERY / ELECTRICAL
    # =====================================================

    if category == "electrical":

        electrical_symptom = any(
            item in symptoms
            for item in [
                "starting",
            ]
        ) or any(
            phrase in full_history
            for phrase in [
                "clicking",
                "click",
                "dim lights",
                "dashboard lights dim",
                "battery dead",
                "battery weak",
                "electrical problem",
            ]
        )

        if not electrical_symptom:

            return response(
                "I can help investigate the electrical system.",
                (
                    "Is the car failing to start, making clicking "
                    "sounds, showing dim dashboard lights, losing "
                    "electrical power, or showing a warning light?"
                ),
                True,
            )

        if onset is None:

            return response(
                "Thanks. I understand the electrical symptom.",
                "When did you first notice the problem?",
                True,
            )

        return response(
            "Thanks. I have enough information about "
            "the electrical problem to proceed with the diagnosis.",
            None,
            False,
        )

    # =====================================================
    # STEERING / SUSPENSION
    # =====================================================

    if category == "steering":

        steering_symptom = any(
            item in symptoms
            for item in [
                "vibration",
                "noise",
                "pulling",
            ]
        )

        if not steering_symptom:

            return response(
                "I can help investigate the steering or suspension.",
                (
                    "What are you noticing — steering vibration, "
                    "the car pulling to one side, unusual suspension "
                    "noise, a hard steering wheel, or something else?"
                ),
                True,
            )

        if frequency is None:

            return response(
                "Thanks. I understand the steering or suspension symptom.",
                (
                    "Does it happen continuously, while turning, "
                    "while driving over bumps, while braking, "
                    "or mainly at a particular speed?"
                ),
                True,
            )

        if onset is None:

            return response(
                "Thanks. I have the main steering or suspension details.",
                "When did you first notice the problem?",
                True,
            )

        return response(
            "Thanks. I have enough information about "
            "the steering or suspension problem to proceed "
            "with the diagnosis.",
            None,
            False,
        )

    # =====================================================
    # TRANSMISSION / CLUTCH / GEARBOX
    # =====================================================

    if category == "transmission":

        transmission_symptom = any(
            phrase in full_history
            for phrase in [
                "gear not",
                "gear won't",
                "gear wont",
                "hard to shift",
                "difficulty shifting",
                "gear slipping",
                "slipping gear",
                "clutch slipping",
                "clutch pedal",
                "grinding gear",
                "gear grinding",
                "jerking",
                "jerk",
                "automatic transmission",
                "manual transmission",
            ]
        )

        if not transmission_symptom:

            return response(
                "I can help investigate the clutch, gearbox, "
                "or transmission.",
                (
                    "What are you noticing — difficulty changing gears, "
                    "gear slipping, clutch slipping, grinding, jerking, "
                    "or something else?"
                ),
                True,
            )

        if onset is None:

            return response(
                "Thanks. I understand the transmission symptom.",
                "When did you first notice the problem?",
                True,
            )

        return response(
            "Thanks. I have enough information about "
            "the transmission problem to proceed with the diagnosis.",
            None,
            False,
        )

    # =====================================================
    # OIL
    # =====================================================

    if category == "oil":

        if not any(
            phrase in full_history
            for phrase in [
                "oil leak",
                "oil leaking",
                "low oil",
                "oil pressure",
                "oil light",
                "oil warning",
                "oil consumption",
                "burning oil",
            ]
        ):

            return response(
                "I can help investigate the engine-oil issue.",
                (
                    "Are you seeing an oil leak, low oil level, "
                    "an oil warning light, or noticing that "
                    "the engine is consuming oil?"
                ),
                True,
            )

        if onset is None:

            return response(
                "Thanks. I understand the oil-related symptom.",
                "When did you first notice it?",
                True,
            )

        return response(
            "Thanks. I have enough information about "
            "the oil problem to proceed with the diagnosis.",
            None,
            False,
        )

    # =====================================================
    # FUEL
    # =====================================================

    if category == "fuel":

        fuel_symptom = any(
            phrase in full_history
            for phrase in [
                "poor mileage",
                "low mileage",
                "bad mileage",
                "fuel consumption",
                "fuel leak",
                "not starting",
                "won't start",
                "loss of power",
                "poor acceleration",
                "jerking",
                "stalling",
            ]
        )

        if not fuel_symptom:

            return response(
                "I can help investigate the fuel system.",
                (
                    "Are you noticing poor fuel economy, "
                    "difficulty starting, loss of power, "
                    "jerking, a fuel smell, or a possible fuel leak?"
                ),
                True,
            )

        if onset is None:

            return response(
                "Thanks. I understand the fuel-related symptom.",
                "When did you first notice the problem?",
                True,
            )

        return response(
            "Thanks. I have enough information about "
            "the fuel-system problem to proceed with the diagnosis.",
            None,
            False,
        )

    # =====================================================
    # AC / HEATING
    # =====================================================

    if category == "ac":

        ac_symptom = any(
            phrase in full_history
            for phrase in [
                "not cooling",
                "not cold",
                "warm air",
                "hot air",
                "weak airflow",
                "no airflow",
                "bad smell",
                "strange smell",
                "ac noise",
                "ac making noise",
                "heater not working",
            ]
        )

        if not ac_symptom:

            return response(
                "I can help investigate the AC or heating system.",
                (
                    "Is the AC not cooling, blowing warm air, "
                    "having weak airflow, making unusual noise, "
                    "producing a bad smell, or is the heater "
                    "not working?"
                ),
                True,
            )

        if onset is None:

            return response(
                "Thanks. I understand the AC/heating symptom.",
                "When did you first notice the problem?",
                True,
            )

        return response(
            "Thanks. I have enough information about "
            "the AC/heating problem to proceed with the diagnosis.",
            None,
            False,
        )

    # =====================================================
    # EXHAUST / SMOKE
    # =====================================================

    if category == "exhaust":

        smoke_type = any(
            phrase in full_history
            for phrase in [
                "white smoke",
                "blue smoke",
                "black smoke",
                "grey smoke",
                "gray smoke",
            ]
        )

        if not smoke_type:

            return response(
                "I can help investigate the exhaust problem.",
                (
                    "What color is the smoke — white, blue, black, "
                    "grey, or is it mainly an unusual exhaust smell "
                    "or noise?"
                ),
                True,
            )

        if onset is None:

            return response(
                "Thanks. I understand the exhaust symptom.",
                "When did you first notice the smoke?",
                True,
            )

        return response(
            "Thanks. I have enough information about "
            "the exhaust problem to proceed with the diagnosis.",
            None,
            False,
        )

    # =====================================================
    # LIGHTS
    # =====================================================

    if category == "lights":

        if not any(
            phrase in full_history
            for phrase in [
                "not working",
                "doesn't work",
                "doesnt work",
                "not turning on",
                "not coming on",
                "flickering",
                "dim",
                "warning light",
                "check engine",
                "abs light",
            ]
        ):

            return response(
                "I can help investigate the vehicle lighting "
                "or warning-light problem.",
                (
                    "Which light is affected, and what is happening — "
                    "not turning on, flickering, dim, or showing "
                    "a warning on the dashboard?"
                ),
                True,
            )

        if onset is None:

            return response(
                "Thanks. I understand the lighting or warning-light issue.",
                "When did you first notice it?",
                True,
            )

        return response(
            "Thanks. I have enough information about "
            "the lighting/electrical issue to proceed with "
            "the diagnosis.",
            None,
            False,
        )

    # =====================================================
    # HORN
    # =====================================================

    if category == "horn":

        if not any(
            phrase in full_history
            for phrase in [
                "not working",
                "doesn't work",
                "doesnt work",
                "weak",
                "silent",
                "no sound",
            ]
        ):

            return response(
                "I can help investigate the horn.",
                (
                    "Is the horn completely silent, weak, "
                    "intermittent, or does it work sometimes?"
                ),
                True,
            )

        return response(
            "Thanks. I have enough information about "
            "the horn problem to proceed with the diagnosis.",
            None,
            False,
        )

    # =====================================================
    # GENERIC VEHICLE PROBLEM
    # =====================================================

    return response(
        "I can help troubleshoot that vehicle problem.",
        (
            "What is the main symptom — unusual noise, vibration, "
            "warning light, starting problem, fluid leak, loss of power, "
            "or something else?"
        ),
        True,
    )