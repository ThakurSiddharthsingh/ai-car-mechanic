
"""
Rule-based vehicle diagnostic engine.

The diagnostic engine uses the most recent relevant vehicle
problem in the conversation so that an older problem does not
override a newer problem.

Example:

User:
    My brakes are making a grinding noise.

Later:

User:
    My engine is overheating and there is steam.

The second message should produce an engine diagnosis rather
than repeating the old brake diagnosis.
"""


# =========================================================
# HELPER FUNCTIONS
# =========================================================

def normalize_history(message_history):
    """
    Convert the message history into a clean list of strings.
    """

    if not message_history:
        return []

    return [
        str(message).strip()
        for message in message_history
        if str(message).strip()
    ]


def get_latest_problem_context(message_history):
    """
    Identify the most recent major vehicle-system mentioned
    by the user.

    This prevents old problems from dominating a newer problem.
    """

    messages = normalize_history(message_history)

    if not messages:
        return []

    # Work backwards because the newest message is the most
    # relevant message.

    for index in range(len(messages) - 1, -1, -1):

        message = messages[index].lower()

        # -----------------------------------------------------
        # Engine / overheating
        # -----------------------------------------------------

        if any(
            keyword in message
            for keyword in [
                "engine",
                "overheat",
                "overheating",
                "steam",
                "coolant",
                "smoke",
                "losing power",
                "loss of power",
                "won't start",
                "wont start",
                "not start",
            ]
        ):
            return messages[index:]

        # -----------------------------------------------------
        # Brake
        # -----------------------------------------------------

        if any(
            keyword in message
            for keyword in [
                "brake",
                "brakes",
                "braking",
                "brake pedal",
            ]
        ):
            return messages[index:]

        # -----------------------------------------------------
        # Battery
        # -----------------------------------------------------

        if any(
            keyword in message
            for keyword in [
                "battery",
                "battery dead",
                "clicking",
                "dashboard lights dim",
            ]
        ):
            return messages[index:]

        # -----------------------------------------------------
        # Tyre / wheel
        # -----------------------------------------------------

        if any(
            keyword in message
            for keyword in [
                "tyre",
                "tire",
                "puncture",
                "flat tyre",
                "flat tire",
            ]
        ):
            return messages[index:]

        # -----------------------------------------------------
        # Steering / suspension
        # -----------------------------------------------------

        if any(
            keyword in message
            for keyword in [
                "steering",
                "suspension",
                "shock absorber",
            ]
        ):
            return messages[index:]

    # If no specific subsystem was identified, use the
    # complete history.
    return messages


# =========================================================
# BRAKE DIAGNOSIS
# =========================================================

def diagnose_brake_issue(message_history):

    text = " ".join(message_history).lower()

    # -----------------------------------------------------
    # Grinding / scraping
    # -----------------------------------------------------

    if any(
        word in text
        for word in [
            "grinding",
            "grind",
            "scraping",
            "scrape",
            "metal on metal",
            "metal-to-metal",
        ]
    ):
        return {
            "problem": "Possible severely worn brake pads",
            "explanation": (
                "A grinding or scraping sound during braking can "
                "occur when brake pad material is severely worn "
                "and braking components begin contacting each other."
            ),
            "severity": "high",
            "recommendation": (
                "Avoid unnecessary driving and have the braking "
                "system inspected as soon as possible. Continued "
                "driving may damage the brake rotors and reduce "
                "braking performance."
            ),
        }

    # -----------------------------------------------------
    # Soft / spongy pedal
    # -----------------------------------------------------

    if any(
        phrase in text
        for phrase in [
            "soft pedal",
            "pedal is soft",
            "pedal feels soft",
            "brake pedal is soft",
            "brake pedal feels soft",
            "spongy pedal",
            "pedal is spongy",
            "pedal feels spongy",
            "brake pedal is spongy",
            "brake pedal feels spongy",
        ]
    ):
        return {
            "problem": "Possible brake hydraulic system issue",
            "explanation": (
                "A soft or spongy brake pedal can be associated "
                "with air in the brake lines, low brake fluid, "
                "a hydraulic system problem, or other brake-system faults."
            ),
            "severity": "high",
            "recommendation": (
                "Have the brake system inspected promptly. "
                "Avoid driving if braking performance is reduced."
            ),
        }

    # -----------------------------------------------------
    # Hard pedal
    # -----------------------------------------------------

    if any(
        phrase in text
        for phrase in [
            "hard pedal",
            "pedal is hard",
            "pedal feels hard",
            "brake pedal is hard",
            "brake pedal feels hard",
            "hard",
        ]
    ):
        return {
            "problem": "Possible brake assist or vacuum-system issue",
            "explanation": (
                "An unusually hard brake pedal can be associated "
                "with a brake booster, vacuum supply, or brake-assist "
                "problem."
            ),
            "severity": "high",
            "recommendation": (
                "Have the braking system inspected promptly. "
                "If the pedal requires significantly more force "
                "than usual, avoid unnecessary driving."
            ),
        }

    # -----------------------------------------------------
    # Squealing / squeaking
    # -----------------------------------------------------

    if any(
        word in text
        for word in [
            "squeal",
            "squealing",
            "squeak",
            "squeaking",
            "screech",
            "screeching",
        ]
    ):
        return {
            "problem": "Brake pad or brake hardware noise",
            "explanation": (
                "A squealing or squeaking noise during braking "
                "can be caused by brake pad wear, brake pad vibration, "
                "brake dust, moisture, or brake hardware."
            ),
            "severity": "medium",
            "recommendation": (
                "Have the brake pads, rotors, and brake hardware "
                "inspected. If the pads are significantly worn, "
                "they may need replacement."
            ),
        }

    # -----------------------------------------------------
    # Vibration
    # -----------------------------------------------------

    if any(
        word in text
        for word in [
            "vibration",
            "vibrating",
            "shaking",
            "shake",
            "judder",
            "juddering",
        ]
    ):
        return {
            "problem": "Possible brake rotor or brake-system vibration",
            "explanation": (
                "Vibration or shaking while braking can be associated "
                "with brake rotor condition, uneven brake surfaces, "
                "brake components, or other wheel and suspension issues."
            ),
            "severity": "medium",
            "recommendation": (
                "Have the brake rotors, pads, wheels, and related "
                "components inspected."
            ),
        }

    # -----------------------------------------------------
    # Pulling
    # -----------------------------------------------------

    if any(
        phrase in text
        for phrase in [
            "pulling",
            "pulls to the left",
            "pulls to the right",
            "pull left",
            "pull right",
            "car pulls",
            "vehicle pulls",
        ]
    ):
        return {
            "problem": "Possible uneven braking or brake component issue",
            "explanation": (
                "A vehicle pulling to one side during braking can "
                "be associated with uneven braking force, a brake "
                "caliper or pad issue, tyre problems, or other "
                "wheel and suspension components."
            ),
            "severity": "high",
            "recommendation": (
                "Have the braking system and related wheel components "
                "inspected promptly."
            ),
        }

    # -----------------------------------------------------
    # General brake noise
    # -----------------------------------------------------

    if any(
        word in text
        for word in [
            "noise",
            "sound",
            "click",
            "clicking",
        ]
    ):
        return {
            "problem": "Brake system noise",
            "explanation": (
                "A noise that occurs when the brake pedal is pressed "
                "can be related to brake pads, rotors, brake hardware, "
                "brake dust, or other braking system components."
            ),
            "severity": "medium",
            "recommendation": (
                "Have the brake pads, rotors, and brake hardware "
                "inspected. If the noise becomes grinding, braking "
                "performance changes, or warning lights appear, "
                "have the vehicle inspected promptly."
            ),
        }

    return None


# =========================================================
# ENGINE DIAGNOSIS
# =========================================================

def diagnose_engine_issue(message_history):

    text = " ".join(message_history).lower()

    # -----------------------------------------------------
    # Overheating + steam
    # -----------------------------------------------------

    if (
        ("overheat" in text or "overheating" in text)
        and "steam" in text
    ):
        return {
            "problem": "Engine overheating with possible cooling-system issue",
            "explanation": (
                "Engine overheating accompanied by steam can indicate "
                "coolant loss, a cooling-system problem, or another "
                "condition causing excessive engine temperature."
            ),
            "severity": "high",
            "recommendation": (
                "Stop the vehicle safely and allow the engine to cool. "
                "Do not open the radiator or coolant reservoir while "
                "the engine is hot. Have the cooling system inspected."
            ),
        }

    # -----------------------------------------------------
    # General overheating
    # -----------------------------------------------------

    if (
        "overheat" in text
        or "overheating" in text
    ):
        return {
            "problem": "Engine overheating",
            "explanation": (
                "An overheating engine can result from coolant problems, "
                "radiator issues, thermostat failure, cooling-fan problems, "
                "water-pump problems, or other cooling-system faults."
            ),
            "severity": "high",
            "recommendation": (
                "Avoid continuing to drive if the temperature gauge "
                "reaches the red zone. Allow the engine to cool safely "
                "and have the cooling system inspected."
            ),
        }

    # -----------------------------------------------------
    # White smoke
    # -----------------------------------------------------

    if "white smoke" in text:
        return {
            "problem": "Possible coolant entering the combustion system",
            "explanation": (
                "Persistent white smoke from the exhaust can be "
                "associated with coolant entering the combustion "
                "chamber, although other causes are possible."
            ),
            "severity": "high",
            "recommendation": (
                "Have the engine and cooling system inspected promptly."
            ),
        }

    # -----------------------------------------------------
    # Blue smoke
    # -----------------------------------------------------

    if "blue smoke" in text:
        return {
            "problem": "Possible engine oil consumption",
            "explanation": (
                "Blue exhaust smoke can indicate that engine oil "
                "is entering the combustion process."
            ),
            "severity": "medium",
            "recommendation": (
                "Have the engine inspected for possible oil "
                "consumption or internal engine issues."
            ),
        }

    # -----------------------------------------------------
    # Black smoke
    # -----------------------------------------------------

    if "black smoke" in text:
        return {
            "problem": "Possible overly rich fuel mixture",
            "explanation": (
                "Black exhaust smoke can occur when the engine "
                "is receiving more fuel than can be efficiently burned."
            ),
            "severity": "medium",
            "recommendation": (
                "Have the fuel and engine-management systems inspected."
            ),
        }

    # -----------------------------------------------------
    # Engine won't start
    # -----------------------------------------------------

    if any(
        phrase in text
        for phrase in [
            "won't start",
            "wont start",
            "not start",
            "doesn't start",
            "doesnt start",
        ]
    ):
        return {
            "problem": "Engine starting problem",
            "explanation": (
                "A vehicle that does not start can have several possible "
                "causes, including battery, starter, fuel, ignition, or "
                "engine-management problems."
            ),
            "severity": "medium",
            "recommendation": (
                "Have the starting, electrical, fuel, and ignition "
                "systems inspected."
            ),
        }

    # -----------------------------------------------------
    # Loss of power
    # -----------------------------------------------------

    if any(
        phrase in text
        for phrase in [
            "losing power",
            "loss of power",
            "low power",
            "poor acceleration",
            "not accelerating",
        ]
    ):
        return {
            "problem": "Possible engine performance issue",
            "explanation": (
                "Loss of engine power can have several causes, including "
                "fuel delivery, air intake, ignition, sensor, exhaust, "
                "or other engine-management problems."
            ),
            "severity": "medium",
            "recommendation": (
                "Have the engine-management, fuel, air-intake, ignition, "
                "and exhaust systems checked."
            ),
        }

    # -----------------------------------------------------
    # Engine knocking
    # -----------------------------------------------------

    if any(
        word in text
        for word in [
            "knocking",
            "engine knock",
        ]
    ):
        return {
            "problem": "Possible engine knocking issue",
            "explanation": (
                "A knocking sound from the engine can have several "
                "causes, ranging from combustion-related issues to "
                "mechanical problems."
            ),
            "severity": "high",
            "recommendation": (
                "Avoid unnecessary driving and have the engine "
                "inspected promptly."
            ),
        }

    return None


# =========================================================
# BATTERY DIAGNOSIS
# =========================================================

def diagnose_battery_issue(message_history):

    text = " ".join(message_history).lower()

    if (
        "battery" in text
        and any(
            word in text
            for word in [
                "click",
                "clicking",
            ]
        )
    ):
        return {
            "problem": "Possible weak or discharged battery",
            "explanation": (
                "Repeated clicking when attempting to start the "
                "vehicle can occur when the battery does not have "
                "enough power to operate the starter properly."
            ),
            "severity": "medium",
            "recommendation": (
                "Have the battery charge and condition checked. "
                "The charging and starting systems may also need inspection."
            ),
        }

    if (
        "battery" in text
        and any(
            word in text
            for word in [
                "dim",
                "dashboard lights dim",
            ]
        )
    ):
        return {
            "problem": "Possible weak or discharged battery",
            "explanation": (
                "Very dim dashboard or vehicle lights can occur "
                "when battery voltage is low or the electrical "
                "system is not receiving sufficient power."
            ),
            "severity": "medium",
            "recommendation": (
                "Have the battery and charging system tested."
            ),
        }

    if "battery" in text:
        return {
            "problem": "Possible battery or charging-system issue",
            "explanation": (
                "Battery-related problems can be caused by a weak "
                "battery, charging-system fault, loose connection, "
                "or another electrical issue."
            ),
            "severity": "medium",
            "recommendation": (
                "Have the battery, terminals, and charging system tested."
            ),
        }

    return None


# =========================================================
# TYRE DIAGNOSIS
# =========================================================

def diagnose_tyre_issue(message_history):

    text = " ".join(message_history).lower()

    if any(
        word in text
        for word in [
            "puncture",
            "flat tyre",
            "flat tire",
            "tyre is flat",
            "tire is flat",
            "tyre pressure",
            "tire pressure",
        ]
    ):
        return {
            "problem": "Possible tyre pressure or puncture issue",
            "explanation": (
                "A flat tyre or rapidly falling tyre pressure can "
                "be caused by a puncture, valve problem, or tyre damage."
            ),
            "severity": "high",
            "recommendation": (
                "Avoid driving on a severely underinflated or flat "
                "tyre. Inspect the tyre and repair or replace it."
            ),
        }

    return None


# =========================================================
# STEERING / SUSPENSION DIAGNOSIS
# =========================================================

def diagnose_steering_issue(message_history):

    text = " ".join(message_history).lower()

    if any(
        phrase in text
        for phrase in [
            "steering wheel shaking",
            "steering wheel vibration",
            "steering vibration",
        ]
    ):
        return {
            "problem": "Possible wheel, tyre, alignment, or suspension issue",
            "explanation": (
                "Steering-wheel vibration can be associated with tyre "
                "balance, wheel condition, alignment, suspension "
                "components, or other wheel-related problems."
            ),
            "severity": "medium",
            "recommendation": (
                "Have the tyres, wheels, wheel balance, alignment, "
                "and suspension components inspected."
            ),
        }

    if any(
        phrase in text
        for phrase in [
            "steering pulls",
            "steering pulling",
            "car pulls",
            "vehicle pulls",
        ]
    ):
        return {
            "problem": "Possible wheel alignment or steering issue",
            "explanation": (
                "A vehicle that consistently pulls to one side can "
                "be associated with wheel alignment, tyre condition, "
                "brake imbalance, or steering and suspension components."
            ),
            "severity": "medium",
            "recommendation": (
                "Have the tyres, alignment, steering, suspension, "
                "and brakes inspected."
            ),
        }

    return None


# =========================================================
# MAIN DIAGNOSIS
# =========================================================

def diagnose(message_history):
    """
    Diagnose the most recent vehicle problem.
    """

    # Get only the context belonging to the latest problem.
    problem_context = get_latest_problem_context(message_history)

    if not problem_context:
        return None

    text = " ".join(problem_context).lower()

    # -----------------------------------------------------
    # IMPORTANT:
    # Check the subsystem that is actually present in the
    # latest problem.
    # -----------------------------------------------------

    # Brake
    if "brake" in text:
        result = diagnose_brake_issue(problem_context)

        if result:
            return result

    # Engine
    if any(
        keyword in text
        for keyword in [
            "engine",
            "overheat",
            "overheating",
            "steam",
            "coolant",
            "smoke",
        ]
    ):
        result = diagnose_engine_issue(problem_context)

        if result:
            return result

    # Battery
    if "battery" in text:
        result = diagnose_battery_issue(problem_context)

        if result:
            return result

    # Tyre
    if any(
        keyword in text
        for keyword in [
            "tyre",
            "tire",
            "puncture",
            "flat tyre",
            "flat tire",
        ]
    ):
        result = diagnose_tyre_issue(problem_context)

        if result:
            return result

    # Steering / suspension
    if any(
        keyword in text
        for keyword in [
            "steering",
            "suspension",
            "shock absorber",
        ]
    ):
        result = diagnose_steering_issue(problem_context)

        if result:
            return result

    return None

