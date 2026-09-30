
CAR_KEYWORDS = [
    "car",
    "vehicle",
    "engine",
    "brake",
    "brakes",
    "tyre",
    "tire",
    "wheel",
    "steering",
    "clutch",
    "gear",
    "gearbox",
    "battery",
    "oil",
    "coolant",
    "radiator",
    "ac",
    "air conditioner",
    "air conditioning",
    "headlight",
    "light",
    "horn",
    "starter",
    "alternator",
    "suspension",
    "shock absorber",
    "fuel",
    "petrol",
    "diesel",
    "smoke",
    "noise",
    "vibration",
    "overheating",
    "puncture",
    "dashboard",
    "warning light",
    "check engine",
]


def is_car_related(message: str) -> bool:
    """
    Check whether a message is related to cars
    or mechanical issues.
    """

    message = message.lower()

    return any(
        keyword in message
        for keyword in CAR_KEYWORDS
    )


def detect_brake_pedal_condition(text: str):
    """
    Detect the brake pedal condition from the user's message.

    Returns:
        "soft"
        "hard"
        "spongy"
        "normal"
        None
    """

    text = text.lower().strip()

    # Soft pedal
    if (
        "soft" in text
        or "pedal feels soft" in text
        or "pedal is soft" in text
        or "brake pedal feels soft" in text
        or "brake pedal is soft" in text
    ):
        return "soft"

    # Spongy pedal
    if (
        "spongy" in text
        or "pedal feels spongy" in text
        or "pedal is spongy" in text
    ):
        return "spongy"

    # Hard pedal
    if (
        "hard" in text
        or "pedal feels hard" in text
        or "pedal is hard" in text
        or "brake pedal feels hard" in text
        or "brake pedal is hard" in text
    ):
        return "hard"

    # Normal pedal
    if (
        "normal" in text
        or "pedal feels normal" in text
        or "pedal is normal" in text
        or "brake pedal feels normal" in text
        or "brake pedal is normal" in text
    ):
        return "normal"

    return None


def detect_brake_timing(text: str):
    """
    Detect when the brake problem happens.

    Returns:
        "braking"
        "driving"
        "both"
        None
    """

    text = text.lower()

    braking = any(
        phrase in text
        for phrase in [
            "when i brake",
            "when i press the brake",
            "when i press brake",
            "while braking",
            "during braking",
            "when braking",
            "every time i brake",
            "every time i press the brake",
            "pressing the brake",
            "press the brake",
            "press brake",
            "braking",
        ]
    )

    driving = any(
        phrase in text
        for phrase in [
            "while driving",
            "when driving",
            "driving without braking",
            "also while driving",
            "even when i'm driving",
            "even when driving",
        ]
    )

    if braking and driving:
        return "both"

    if braking:
        return "braking"

    if driving:
        return "driving"

    return None


def generate_basic_response(
    message: str,
    conversation_history=None
):
    """
    Generate a rule-based mechanic response.

    Parameters:
        message:
            Current user message.

        conversation_history:
            Previous USER messages from the same conversation.

    Returns:
        Dictionary containing:
            response
            is_car_related
            needs_follow_up
            follow_up_question (when required)
    """

    if conversation_history is None:
        conversation_history = []

    current_message = message.lower().strip()

    # Combine previous messages with current message.
    full_history = " ".join(
        conversation_history + [message]
    ).lower()

    # =========================================================
    # 1. NON-CAR QUESTIONS
    # =========================================================

    if not is_car_related(full_history):

        return {
            "is_car_related": False,
            "response": (
                "I'm an AI car mechanic assistant. I can help with "
                "car and mechanical issues such as engine problems, "
                "brakes, tyres, battery, overheating, steering, "
                "and other vehicle-related concerns."
            ),
            "needs_follow_up": False,
        }

    # =========================================================
    # 2. BRAKE CONVERSATION
    # =========================================================

    if "brake" in full_history:

        # -----------------------------------------------------
        # Detect brake information from entire conversation
        # -----------------------------------------------------

        pedal_condition = detect_brake_pedal_condition(
            full_history
        )

        brake_timing = detect_brake_timing(
            full_history
        )

        # -----------------------------------------------------
        # Detect brake symptoms
        # -----------------------------------------------------

        has_brake_noise = any(
            word in full_history
            for word in [
                "noise",
                "sound",
                "squeal",
                "squealing",
                "squeak",
                "squeaking",
                "screech",
                "grinding",
                "scraping",
                "clicking",
                "click",
            ]
        )

        has_brake_vibration = any(
            word in full_history
            for word in [
                "vibration",
                "vibrating",
                "shaking",
                "shake",
                "judder",
            ]
        )

        has_brake_pulling = any(
            phrase in full_history
            for phrase in [
                "pulling",
                "pulls to the left",
                "pulls to the right",
                "pull left",
                "pull right",
            ]
        )

        # =====================================================
        # SPECIAL CASE:
        # User may answer the previous question with only:
        #
        # "hard"
        # "soft"
        # "normal"
        # "spongy"
        #
        # We already detect these from full_history.
        # =====================================================

        if pedal_condition is not None:

            # If we already know the brake problem happens
            # during braking and know the pedal condition,
            # we have enough information.
            if brake_timing in ["braking", "both"]:

                return {
                    "is_car_related": True,
                    "response": (
                        "Thanks. I have enough information about "
                        "the brake symptoms to proceed with a "
                        "diagnosis."
                    ),
                    "needs_follow_up": False,
                }

        # =====================================================
        # If user has described a brake symptom
        # =====================================================

        if (
            has_brake_noise
            or has_brake_vibration
            or has_brake_pulling
        ):

            # -------------------------------------------------
            # We have symptom but don't know WHEN it happens.
            # -------------------------------------------------

            if brake_timing is None:

                return {
                    "is_car_related": True,
                    "response": (
                        "I can help investigate that brake issue."
                    ),
                    "follow_up_question": (
                        "Does the problem happen only when you "
                        "press the brake, or also while driving "
                        "without braking?"
                    ),
                    "needs_follow_up": True,
                }

            # -------------------------------------------------
            # We know it happens while braking, but pedal
            # condition is unknown.
            # -------------------------------------------------

            if (
                brake_timing in ["braking", "both"]
                and pedal_condition is None
            ):

                return {
                    "is_car_related": True,
                    "response": (
                        "Thanks. I understand that the problem "
                        "happens while braking."
                    ),
                    "follow_up_question": (
                        "How does the brake pedal feel — soft, "
                        "hard, spongy, or normal?"
                    ),
                    "needs_follow_up": True,
                }

            # -------------------------------------------------
            # Problem happens while driving but not specifically
            # during braking.
            # -------------------------------------------------

            if brake_timing == "driving":

                return {
                    "is_car_related": True,
                    "response": (
                        "Thanks. I understand that the problem "
                        "can occur while driving."
                    ),
                    "follow_up_question": (
                        "Does the problem also happen when you "
                        "press the brake pedal?"
                    ),
                    "needs_follow_up": True,
                }

        # =====================================================
        # Generic brake complaint
        # =====================================================

        return {
            "is_car_related": True,
            "response": (
                "I can help investigate the brake issue. "
                "I need a little more information first."
            ),
            "follow_up_question": (
                "What are you noticing — noise, grinding, "
                "vibration, pulling, or something else?"
            ),
            "needs_follow_up": True,
        }

    # =========================================================
    # 3. ENGINE CONVERSATION
    # =========================================================

    if "engine" in full_history:

        has_engine_symptom = any(
            phrase in full_history
            for phrase in [
                "overheat",
                "overheating",
                "smoke",
                "losing power",
                "loss of power",
                "not start",
                "won't start",
                "wont start",
                "noise",
                "knocking",
                "ticking",
                "stalling",
                "stall",
            ]
        )

        if has_engine_symptom:

            return {
                "is_car_related": True,
                "response": (
                    "Thanks. I have some useful information "
                    "about the engine symptoms. I can use these "
                    "details for the diagnosis."
                ),
                "needs_follow_up": False,
            }

        return {
            "is_car_related": True,
            "response": (
                "Let's investigate the engine problem. "
                "I need a few details first."
            ),
            "follow_up_question": (
                "Is the engine failing to start, losing power, "
                "overheating, making unusual noises, or producing smoke?"
            ),
            "needs_follow_up": True,
        }

    # =========================================================
    # 4. BATTERY CONVERSATION
    # =========================================================

    if "battery" in full_history:

        has_battery_symptom = any(
            phrase in full_history
            for phrase in [
                "click",
                "clicking",
                "dim",
                "dashboard",
                "won't start",
                "wont start",
                "not start",
                "dead",
            ]
        )

        if has_battery_symptom:

            return {
                "is_car_related": True,
                "response": (
                    "Thanks. That gives me useful information "
                    "about the battery or starting issue. "
                    "I can use these symptoms for the diagnosis."
                ),
                "needs_follow_up": False,
            }

        return {
            "is_car_related": True,
            "response": (
                "A battery-related issue can cause several "
                "starting and electrical problems."
            ),
            "follow_up_question": (
                "When you try to start the car, do you hear "
                "a clicking sound, or do the dashboard lights "
                "become very dim?"
            ),
            "needs_follow_up": True,
        }

    # =========================================================
    # 5. OVERHEATING
    # =========================================================

    if (
        "overheat" in full_history
        or "overheating" in full_history
    ):

        has_overheating_detail = any(
            phrase in full_history
            for phrase in [
                "steam",
                "coolant",
                "leak",
                "leaking",
                "temperature gauge",
                "red zone",
            ]
        )

        if has_overheating_detail:

            return {
                "is_car_related": True,
                "response": (
                    "Thanks. I have enough information to "
                    "investigate the overheating issue further."
                ),
                "needs_follow_up": False,
            }

        return {
            "is_car_related": True,
            "response": (
                "An overheating engine should be handled carefully. "
                "Avoid continuing to drive if the temperature is "
                "reaching the red zone."
            ),
            "follow_up_question": (
                "Is coolant leaking, is there steam from under "
                "the hood, or is the temperature gauge simply "
                "rising above normal?"
            ),
            "needs_follow_up": True,
        }

    # =========================================================
    # 6. GENERIC CAR-RELATED CONVERSATION
    # =========================================================

    return {
        "is_car_related": True,
        "response": (
            "I can help troubleshoot that vehicle issue. "
            "Before giving a diagnosis, I need some more information."
        ),
        "follow_up_question": (
            "What symptoms are you noticing, when did the problem "
            "start, and does it happen continuously or only under "
            "certain conditions?"
        ),
        "needs_follow_up": True,
    }

