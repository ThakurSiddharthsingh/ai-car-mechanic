"""
AI Car Mechanic - Diagnostic Engine

Rule-based diagnostic engine.

Important:
This does NOT claim to perform a definitive mechanical diagnosis.
It identifies a likely problem area from the symptoms supplied
by the user and recommends an appropriate inspection/action.
"""


# =========================================================
# HELPERS
# =========================================================

def normalize_history(message_history):
    if not message_history:
        return []

    return [
        str(message).strip()
        for message in message_history
        if str(message).strip()
    ]


def combined_text(message_history):
    return " ".join(
        normalize_history(message_history)
    ).lower()


def contains_any(text, phrases):
    return any(
        phrase in text
        for phrase in phrases
    )


def result(
    problem,
    explanation,
    severity,
    recommendation,
):
    return {
        "problem": problem,
        "explanation": explanation,
        "severity": severity,
        "recommendation": recommendation,
    }


# =========================================================
# BRAKE DIAGNOSIS
# =========================================================

def diagnose_brake_issue(messages):

    text = combined_text(messages)

    # Grinding
    if contains_any(
        text,
        [
            "grinding",
            "grind",
            "scraping",
            "metal on metal",
            "metal-to-metal",
        ],
    ):
        return result(
            "Possible severely worn brake pads",
            (
                "Grinding or scraping during braking can occur "
                "when brake-pad material is severely worn or "
                "when brake components are contacting each other."
            ),
            "high",
            (
                "Avoid unnecessary driving and have the brake "
                "system inspected as soon as possible."
            ),
        )

    # Soft/spongy pedal
    if contains_any(
        text,
        [
            "soft pedal",
            "pedal is soft",
            "pedal feels soft",
            "spongy pedal",
            "pedal is spongy",
            "pedal feels spongy",
        ],
    ):
        return result(
            "Possible brake hydraulic or brake-fluid issue",
            (
                "A soft or spongy brake pedal can be associated "
                "with air in the brake lines, low brake fluid, "
                "a hydraulic fault, or another brake-system problem."
            ),
            "high",
            (
                "Have the braking system inspected promptly. "
                "Avoid driving if braking performance is reduced."
            ),
        )

    # Hard pedal
    if contains_any(
        text,
        [
            "hard pedal",
            "pedal is hard",
            "pedal feels hard",
        ],
    ):
        return result(
            "Possible brake-assist or vacuum-system issue",
            (
                "An unusually hard brake pedal can be associated "
                "with a brake booster, vacuum supply, or brake-assist problem."
            ),
            "high",
            (
                "Have the braking system inspected promptly. "
                "Avoid unnecessary driving if significantly more "
                "force is required to stop the vehicle."
            ),
        )

    # Squealing
    if contains_any(
        text,
        [
            "squealing",
            "squeal",
            "squeaking",
            "squeak",
            "screech",
        ],
    ):
        return result(
            "Possible brake pad or brake hardware noise",
            (
                "Squealing or squeaking during braking can be "
                "associated with brake-pad wear, brake-pad vibration, "
                "brake dust, moisture, or brake hardware."
            ),
            "medium",
            (
                "Have the brake pads, rotors, and brake hardware "
                "inspected."
            ),
        )

    # Brake vibration
    if contains_any(
        text,
        [
            "brake vibration",
            "vibration when braking",
            "vibrating when braking",
            "shaking when braking",
            "judder",
            "juddering",
        ],
    ):
        return result(
            "Possible brake rotor or brake-system vibration",
            (
                "Vibration or shaking while braking can be associated "
                "with brake-rotor condition, uneven brake surfaces, "
                "brake components, or related wheel and suspension issues."
            ),
            "medium",
            (
                "Have the brake pads, rotors, wheels, and related "
                "components inspected."
            ),
        )

    # Pulling
    if contains_any(
        text,
        [
            "pulling while braking",
            "car pulls while braking",
            "vehicle pulls while braking",
            "pulls left while braking",
            "pulls right while braking",
        ],
    ):
        return result(
            "Possible uneven braking or brake-component issue",
            (
                "A vehicle pulling to one side during braking can "
                "be associated with uneven braking force, a brake "
                "caliper or pad issue, tyre condition, or wheel/suspension components."
            ),
            "high",
            (
                "Have the braking system and related wheel components "
                "inspected promptly."
            ),
        )

    return None


# =========================================================
# TYRE DIAGNOSIS
# =========================================================

def diagnose_tyre_issue(messages):

    text = combined_text(messages)

    # Flat tyre / puncture
    if contains_any(
        text,
        [
            "puncture",
            "flat tyre",
            "flat tire",
            "tyre is flat",
            "tire is flat",
            "nail in tyre",
            "nail in tire",
        ],
    ):
        return result(
            "Possible tyre puncture or tyre damage",
            (
                "A flat tyre or rapidly falling tyre pressure can "
                "be caused by a puncture, valve problem, or tyre damage."
            ),
            "high",
            (
                "Avoid driving on a severely underinflated or flat tyre. "
                "Inspect the tyre and repair or replace it as appropriate."
            ),
        )

    # Low pressure
    if contains_any(
        text,
        [
            "low tyre pressure",
            "low tire pressure",
            "tyre pressure",
            "tire pressure",
            "underinflated",
            "under inflated",
        ],
    ):
        return result(
            "Possible low tyre pressure",
            (
                "Low tyre pressure can result from normal pressure loss, "
                "a puncture, a leaking valve, temperature changes, or tyre damage."
            ),
            "medium",
            (
                "Check all tyre pressures against the vehicle manufacturer's "
                "recommended values. Inspect for punctures or leaks if pressure "
                "continues to fall."
            ),
        )

    # Vibration
    if contains_any(
        text,
        [
            "tyre vibration",
            "tire vibration",
            "tyre vibrating",
            "tyre shaking",
            "wheel vibration",
            "steering wheel vibration",
        ],
    ):
        return result(
            "Possible wheel balance, tyre, or alignment issue",
            (
                "Vehicle or steering-wheel vibration can be associated "
                "with wheel imbalance, tyre damage, uneven tyre wear, "
                "wheel condition, alignment, or suspension components."
            ),
            "medium",
            (
                "Have the tyres and wheels inspected and check wheel "
                "balancing and alignment."
            ),
        )

    # Uneven wear
    if contains_any(
        text,
        [
            "uneven tyre wear",
            "uneven tire wear",
            "uneven wear",
            "worn tyre",
            "worn tire",
        ],
    ):
        return result(
            "Possible tyre wear or wheel-alignment issue",
            (
                "Uneven tyre wear can be associated with incorrect "
                "tyre pressure, wheel alignment, wheel imbalance, "
                "suspension wear, or other wheel-related conditions."
            ),
            "medium",
            (
                "Inspect tyre pressure, tyre condition, wheel alignment, "
                "wheel balance, and suspension components."
            ),
        )

    # Pulling
    if contains_any(
        text,
        [
            "car pulls",
            "vehicle pulls",
            "pulls left",
            "pulls right",
            "pulling to the left",
            "pulling to the right",
        ],
    ):
        return result(
            "Possible wheel alignment, tyre, or suspension issue",
            (
                "A vehicle consistently pulling to one side can be "
                "associated with wheel alignment, tyre condition, "
                "brake imbalance, or steering and suspension components."
            ),
            "medium",
            (
                "Have the tyres, wheel alignment, steering, suspension, "
                "and brakes inspected."
            ),
        )

    # Tyre noise
    if contains_any(
        text,
        [
            "tyre noise",
            "tire noise",
            "tyre sound",
            "tire sound",
            "humming noise",
            "thumping noise",
        ],
    ):
        return result(
            "Possible tyre or wheel-related noise",
            (
                "Unusual tyre or wheel noise can be associated with "
                "uneven tyre wear, wheel-bearing problems, tyre damage, "
                "wheel imbalance, or other wheel-related conditions."
            ),
            "medium",
            (
                "Have the tyres, wheels, wheel bearings, and suspension "
                "components inspected."
            ),
        )

    return None


# =========================================================
# ENGINE DIAGNOSIS
# =========================================================

def diagnose_engine_issue(messages):

    text = combined_text(messages)

    # Overheating
    if contains_any(
        text,
        [
            "overheat",
            "overheating",
            "temperature gauge red",
            "temperature in red",
        ],
    ):
        return result(
            "Engine overheating",
            (
                "Engine overheating can be caused by coolant loss, "
                "radiator problems, thermostat failure, cooling-fan "
                "problems, water-pump problems, or other cooling-system faults."
            ),
            "high",
            (
                "Avoid continuing to drive if the temperature reaches "
                "the red zone. Allow the engine to cool safely and "
                "have the cooling system inspected."
            ),
        )

    # White smoke
    if "white smoke" in text:
        return result(
            "Possible coolant entering the combustion system",
            (
                "Persistent white exhaust smoke can be associated "
                "with coolant entering the combustion chamber, "
                "although other causes are possible."
            ),
            "high",
            (
                "Have the engine and cooling system inspected promptly."
            ),
        )

    # Blue smoke
    if "blue smoke" in text:
        return result(
            "Possible engine oil consumption",
            (
                "Blue exhaust smoke can indicate that engine oil "
                "is entering the combustion process."
            ),
            "medium",
            (
                "Have the engine inspected for possible oil-consumption "
                "or internal-engine issues."
            ),
        )

    # Black smoke
    if "black smoke" in text:
        return result(
            "Possible overly rich fuel mixture",
            (
                "Black exhaust smoke can occur when the engine receives "
                "more fuel than can be efficiently burned."
            ),
            "medium",
            (
                "Have the fuel and engine-management systems inspected."
            ),
        )

    # Starting problem
    if contains_any(
        text,
        [
            "won't start",
            "doesn't start",
            "not starting",
            "cannot start",
            "can't start",
        ],
    ):
        return result(
            "Engine starting problem",
            (
                "A vehicle that does not start can have several possible "
                "causes, including battery, starter, fuel, ignition, "
                "immobilizer, or engine-management problems."
            ),
            "medium",
            (
                "Check the battery and starting system and have the "
                "fuel, ignition, and engine-management systems inspected "
                "if the problem persists."
            ),
        )

    # Power loss
    if contains_any(
        text,
        [
            "losing power",
            "loss of power",
            "low power",
            "poor acceleration",
            "not accelerating",
        ],
    ):
        return result(
            "Possible engine performance issue",
            (
                "Loss of engine power can have several causes, including "
                "fuel delivery, air intake, ignition, sensors, exhaust "
                "restriction, or other engine-management problems."
            ),
            "medium",
            (
                "Have the engine-management, fuel, air-intake, ignition, "
                "and exhaust systems checked."
            ),
        )

    # Knocking
    if contains_any(
        text,
        [
            "engine knocking",
            "engine knock",
            "knocking from engine",
        ],
    ):
        return result(
            "Possible engine knocking issue",
            (
                "A knocking sound from the engine can have several "
                "causes ranging from combustion-related issues to "
                "mechanical problems."
            ),
            "high",
            (
                "Avoid unnecessary driving and have the engine inspected promptly."
            ),
        )

    # Ticking
    if contains_any(
        text,
        [
            "engine ticking",
            "ticking from engine",
            "engine ticking noise",
        ],
    ):
        return result(
            "Possible engine mechanical or valvetrain noise",
            (
                "A ticking noise from the engine can have several "
                "possible causes, including lubrication, valvetrain, "
                "or other mechanical issues."
            ),
            "medium",
            (
                "Check the engine-oil level and have the engine inspected "
                "if the noise persists or becomes louder."
            ),
        )

    return None


# =========================================================
# BATTERY / ELECTRICAL
# =========================================================

def diagnose_electrical_issue(messages):

    text = combined_text(messages)

    if contains_any(
        text,
        [
            "battery",
            "clicking when starting",
            "click when starting",
            "dashboard lights dim",
            "lights become dim",
        ],
    ):
        return result(
            "Possible weak battery or charging-system issue",
            (
                "A weak battery, charging-system problem, poor connection, "
                "or starter-related issue can cause starting and electrical symptoms."
            ),
            "medium",
            (
                "Have the battery, battery terminals, charging system, "
                "and starting system tested."
            ),
        )

    if contains_any(
        text,
        [
            "alternator",
            "charging light",
            "battery light",
            "battery warning light",
        ],
    ):
        return result(
            "Possible charging-system problem",
            (
                "A charging warning or alternator-related symptom can "
                "indicate a problem with the alternator, belt, wiring, "
                "or charging system."
            ),
            "high",
            (
                "Have the charging system inspected promptly. "
                "Avoid unnecessary driving if the vehicle is losing electrical power."
            ),
        )

    if contains_any(
        text,
        [
            "starter",
            "starter motor",
        ],
    ):
        return result(
            "Possible starter-system problem",
            (
                "A starter-related problem can prevent the engine "
                "from cranking or starting normally."
            ),
            "medium",
            (
                "Have the battery, starter motor, starter connections, "
                "and starting circuit inspected."
            ),
        )

    return None


# =========================================================
# COOLING
# =========================================================

def diagnose_cooling_issue(messages):

    text = combined_text(messages)

    if contains_any(
        text,
        [
            "overheating",
            "overheat",
            "temperature gauge red",
            "temperature high",
        ],
    ):
        return result(
            "Engine overheating / cooling-system issue",
            (
                "Overheating can be caused by coolant loss, radiator "
                "problems, thermostat failure, cooling-fan problems, "
                "water-pump problems, or other cooling-system faults."
            ),
            "high",
            (
                "Stop safely if the temperature reaches the red zone. "
                "Do not open the cooling system while it is hot. "
                "Have the cooling system inspected."
            ),
        )

    if contains_any(
        text,
        [
            "coolant leak",
            "coolant leaking",
            "coolant loss",
        ],
    ):
        return result(
            "Possible coolant leak",
            (
                "Coolant loss can occur because of a hose, radiator, "
                "water-pump, thermostat housing, reservoir, or other "
                "cooling-system problem."
            ),
            "high",
            (
                "Do not continue driving if coolant loss is significant "
                "or the engine is overheating. Have the cooling system inspected."
            ),
        )

    return None


# =========================================================
# STEERING / SUSPENSION
# =========================================================

def diagnose_steering_issue(messages):

    text = combined_text(messages)

    if contains_any(
        text,
        [
            "steering wheel vibration",
            "steering vibration",
            "steering wheel shaking",
        ],
    ):
        return result(
            "Possible wheel, tyre, alignment, or suspension issue",
            (
                "Steering-wheel vibration can be associated with tyre "
                "balance, wheel condition, alignment, suspension components, "
                "or other wheel-related problems."
            ),
            "medium",
            (
                "Have the tyres, wheels, wheel balance, alignment, "
                "and suspension components inspected."
            ),
        )

    if contains_any(
        text,
        [
            "steering pulls",
            "steering pulling",
            "car pulls",
            "vehicle pulls",
            "pulling to the left",
            "pulling to the right",
        ],
    ):
        return result(
            "Possible wheel alignment or steering issue",
            (
                "A vehicle pulling to one side can be associated with "
                "wheel alignment, tyre condition, brake imbalance, "
                "or steering and suspension components."
            ),
            "medium",
            (
                "Have the tyres, alignment, steering, suspension, "
                "and brakes inspected."
            ),
        )

    if contains_any(
        text,
        [
            "suspension noise",
            "noise over bumps",
            "clunking over bumps",
            "clunk over bumps",
            "knocking over bumps",
        ],
    ):
        return result(
            "Possible suspension-component issue",
            (
                "Clunking or knocking over bumps can be associated "
                "with worn suspension components, bushings, links, "
                "shock absorbers, or related hardware."
            ),
            "medium",
            (
                "Have the suspension and steering components inspected."
            ),
        )

    return None


# =========================================================
# TRANSMISSION / CLUTCH
# =========================================================

def diagnose_transmission_issue(messages):

    text = combined_text(messages)

    if contains_any(
        text,
        [
            "clutch slipping",
            "clutch is slipping",
            "engine revs but car doesn't accelerate",
            "engine revs but car does not accelerate",
        ],
    ):
        return result(
            "Possible clutch slipping",
            (
                "A clutch that slips can allow engine speed to increase "
                "without a corresponding increase in vehicle speed."
            ),
            "medium",
            (
                "Have the clutch and transmission inspected."
            ),
        )

    if contains_any(
        text,
        [
            "hard to shift",
            "difficulty shifting",
            "gear difficult",
            "gear is difficult",
        ],
    ):
        return result(
            "Possible gear-selection or clutch/transmission issue",
            (
                "Difficulty selecting gears can be associated with "
                "clutch, transmission, linkage, fluid, or internal "
                "gearbox problems."
            ),
            "medium",
            (
                "Have the clutch, transmission fluid where applicable, "
                "gear linkage, and transmission inspected."
            ),
        )

    if contains_any(
        text,
        [
            "grinding gear",
            "gear grinding",
            "grinding when changing gear",
        ],
    ):
        return result(
            "Possible transmission or clutch problem",
            (
                "Grinding while changing gears can indicate a clutch, "
                "synchronizer, gear, linkage, or other transmission issue."
            ),
            "high",
            (
                "Avoid forcing the gear lever and have the transmission "
                "and clutch inspected."
            ),
        )

    if contains_any(
        text,
        [
            "jerking",
            "jerking while changing gear",
            "transmission jerking",
            "gearbox jerking",
        ],
    ):
        return result(
            "Possible transmission or clutch-related issue",
            (
                "Jerking during gear changes can have several causes, "
                "including clutch, transmission, fluid, sensor, or control-system issues."
            ),
            "medium",
            (
                "Have the transmission and clutch system inspected."
            ),
        )

    return None


# =========================================================
# OIL
# =========================================================

def diagnose_oil_issue(messages):

    text = combined_text(messages)

    if contains_any(
        text,
        [
            "oil leak",
            "oil leaking",
            "oil puddle",
            "oil under car",
        ],
    ):
        return result(
            "Possible engine-oil leak",
            (
                "An oil leak can come from seals, gaskets, the oil pan, "
                "filter area, drain plug, or other engine components."
            ),
            "medium",
            (
                "Check the oil level and have the source of the leak "
                "identified and repaired."
            ),
        )

    if contains_any(
        text,
        [
            "oil warning",
            "oil warning light",
            "oil pressure light",
            "oil pressure warning",
        ],
    ):
        return result(
            "Possible engine-oil pressure problem",
            (
                "An oil-pressure warning can indicate low oil level, "
                "oil-pressure problems, lubrication-system issues, "
                "or another engine fault."
            ),
            "critical",
            (
                "Stop the engine as soon as it is safe to do so and "
                "have the vehicle inspected. Do not continue driving "
                "with an active oil-pressure warning."
            ),
        )

    if contains_any(
        text,
        [
            "burning oil",
            "oil consumption",
            "using too much oil",
            "low oil",
        ],
    ):
        return result(
            "Possible excessive engine-oil consumption",
            (
                "Low or rapidly decreasing engine-oil level can result "
                "from an external leak or internal oil consumption."
            ),
            "medium",
            (
                "Check the oil level and have the engine inspected "
                "for leaks or excessive oil consumption."
            ),
        )

    return None


# =========================================================
# FUEL
# =========================================================

def diagnose_fuel_issue(messages):

    text = combined_text(messages)

    if contains_any(
        text,
        [
            "fuel leak",
            "petrol leak",
            "gasoline leak",
            "diesel leak",
            "fuel leaking",
        ],
    ):
        return result(
            "Possible fuel-system leak",
            (
                "A fuel leak can come from fuel lines, connections, "
                "the tank, pump, injectors, or other fuel-system components."
            ),
            "critical",
            (
                "Avoid driving the vehicle and keep it away from "
                "ignition sources. Have the fuel system inspected immediately."
            ),
        )

    if contains_any(
        text,
        [
            "poor fuel economy",
            "poor mileage",
            "low mileage",
            "high fuel consumption",
            "using too much fuel",
        ],
    ):
        return result(
            "Possible fuel-efficiency issue",
            (
                "High fuel consumption can be associated with tyre pressure, "
                "driving conditions, engine tuning, sensors, injectors, "
                "air intake, or other vehicle systems."
            ),
            "medium",
            (
                "Check tyre pressure and have the engine, fuel system, "
                "air intake, and sensors inspected if the problem persists."
            ),
        )

    return None


# =========================================================
# AC
# =========================================================

def diagnose_ac_issue(messages):

    text = combined_text(messages)

    if contains_any(
        text,
        [
            "ac not cooling",
            "ac not cold",
            "air conditioner not cooling",
            "air conditioning not cooling",
            "warm air from ac",
            "hot air from ac",
        ],
    ):
        return result(
            "Possible air-conditioning cooling-system issue",
            (
                "An AC system that does not cool properly can have causes "
                "including low refrigerant, compressor problems, condenser "
                "issues, airflow restrictions, or electrical/control faults."
            ),
            "medium",
            (
                "Have the AC system, refrigerant level, compressor, "
                "condenser, and airflow checked."
            ),
        )

    if contains_any(
        text,
        [
            "weak airflow",
            "low airflow",
            "ac airflow weak",
        ],
    ):
        return result(
            "Possible AC airflow restriction or blower issue",
            (
                "Weak airflow can be associated with a clogged cabin filter, "
                "blower problem, airflow restriction, or HVAC control issue."
            ),
            "medium",
            (
                "Check the cabin air filter and have the blower and HVAC "
                "airflow system inspected."
            ),
        )

    if contains_any(
        text,
        [
            "bad smell from ac",
            "bad smell from air conditioner",
            "ac smells",
            "ac smell",
        ],
    ):
        return result(
            "Possible HVAC/cabin-air contamination issue",
            (
                "A persistent unpleasant smell from the AC can be associated "
                "with a dirty cabin filter, moisture, or microbial growth "
                "in the HVAC system."
            ),
            "low",
            (
                "Have the cabin filter and HVAC system inspected and cleaned."
            ),
        )

    return None


# =========================================================
# EXHAUST
# =========================================================

def diagnose_exhaust_issue(messages):

    text = combined_text(messages)

    if "white smoke" in text:
        return result(
            "Possible coolant entering the combustion system",
            (
                "Persistent white exhaust smoke can be associated "
                "with coolant entering the combustion chamber."
            ),
            "high",
            (
                "Have the engine and cooling system inspected promptly."
            ),
        )

    if "blue smoke" in text:
        return result(
            "Possible engine-oil burning",
            (
                "Blue exhaust smoke can indicate that engine oil "
                "is entering the combustion process."
            ),
            "medium",
            (
                "Have the engine inspected for possible oil consumption."
            ),
        )

    if "black smoke" in text:
        return result(
            "Possible overly rich fuel mixture",
            (
                "Black exhaust smoke can occur when too much fuel "
                "is being supplied relative to the available air."
            ),
            "medium",
            (
                "Have the fuel and engine-management systems inspected."
            ),
        )

    if contains_any(
        text,
        [
            "exhaust noise",
            "loud exhaust",
            "exhaust loud",
        ],
    ):
        return result(
            "Possible exhaust-system issue",
            (
                "A suddenly louder exhaust can be associated with "
                "a leak, damaged muffler, exhaust pipe, or other "
                "exhaust-system component."
            ),
            "medium",
            (
                "Have the exhaust system inspected for leaks or damage."
            ),
        )

    return None


# =========================================================
# LIGHTS / WARNING LIGHTS
# =========================================================

def diagnose_lights_issue(messages):

    text = combined_text(messages)

    if contains_any(
        text,
        [
            "check engine light",
            "check engine",
        ],
    ):
        return result(
            "Check-engine warning detected",
            (
                "A check-engine light indicates that the vehicle's "
                "engine-management system has detected a fault."
            ),
            "medium",
            (
                "Have the vehicle scanned for diagnostic trouble codes "
                "and inspect the cause before continuing normal use."
            ),
        )

    if contains_any(
        text,
        [
            "abs light",
            "abs warning",
        ],
    ):
        return result(
            "ABS warning detected",
            (
                "An ABS warning can indicate a fault in the anti-lock "
                "braking system or one of its sensors/components."
            ),
            "high",
            (
                "Have the ABS system inspected promptly. Drive cautiously "
                "and avoid unnecessary driving if braking behavior changes."
            ),
        )

    if contains_any(
        text,
        [
            "headlight not working",
            "headlights not working",
            "headlight doesn't work",
            "headlight does not work",
        ],
    ):
        return result(
            "Possible headlight electrical or bulb problem",
            (
                "A headlight that does not work can be caused by a bulb, "
                "fuse, wiring, connector, switch, or control-system issue."
            ),
            "medium",
            (
                "Check the bulb and fuse where appropriate and have "
                "the lighting circuit inspected if necessary."
            ),
        )

    if contains_any(
        text,
        [
            "light flickering",
            "lights flickering",
            "headlight flickering",
        ],
    ):
        return result(
            "Possible electrical charging or connection issue",
            (
                "Flickering lights can be associated with poor electrical "
                "connections, charging-system problems, wiring, or control components."
            ),
            "medium",
            (
                "Have the battery, alternator, wiring, and lighting circuits inspected."
            ),
        )

    return None


# =========================================================
# HORN
# =========================================================

def diagnose_horn_issue(messages):

    text = combined_text(messages)

    if contains_any(
        text,
        [
            "horn not working",
            "horn doesn't work",
            "horn does not work",
            "horn silent",
        ],
    ):
        return result(
            "Possible horn electrical problem",
            (
                "A horn that does not work can be caused by the horn unit, "
                "fuse, relay, wiring, switch, or related electrical components."
            ),
            "medium",
            (
                "Have the horn, fuse, relay, wiring, and steering-wheel "
                "switch circuit inspected."
            ),
        )

    return None


# =========================================================
# MAIN DIAGNOSIS
# =========================================================

def diagnose(message_history):

    messages = normalize_history(message_history)

    if not messages:
        return None

    text = combined_text(messages)

    # -----------------------------------------------------
    # Brake
    # -----------------------------------------------------

    if contains_any(
        text,
        [
            "brake",
            "braking",
            "brake pedal",
        ],
    ):
        result_data = diagnose_brake_issue(messages)

        if result_data:
            return result_data

    # -----------------------------------------------------
    # Tyre / wheel
    # -----------------------------------------------------

    if contains_any(
        text,
        [
            "tyre",
            "tire",
            "puncture",
            "flat tyre",
            "flat tire",
            "wheel",
            "rim",
        ],
    ):
        result_data = diagnose_tyre_issue(messages)

        if result_data:
            return result_data

    # -----------------------------------------------------
    # Cooling / overheating
    # -----------------------------------------------------

    if contains_any(
        text,
        [
            "overheat",
            "overheating",
            "coolant",
            "radiator",
            "thermostat",
            "water pump",
        ],
    ):
        result_data = diagnose_cooling_issue(messages)

        if result_data:
            return result_data

    # -----------------------------------------------------
    # Engine
    # -----------------------------------------------------

    if contains_any(
        text,
        [
            "engine",
            "motor",
            "losing power",
            "loss of power",
            "knocking",
            "ticking",
            "won't start",
            "doesn't start",
        ],
    ):
        result_data = diagnose_engine_issue(messages)

        if result_data:
            return result_data

    # -----------------------------------------------------
    # Electrical
    # -----------------------------------------------------

    if contains_any(
        text,
        [
            "battery",
            "alternator",
            "starter",
            "electrical",
            "fuse",
            "wiring",
        ],
    ):
        result_data = diagnose_electrical_issue(messages)

        if result_data:
            return result_data

    # -----------------------------------------------------
    # Steering / suspension
    # -----------------------------------------------------

    if contains_any(
        text,
        [
            "steering",
            "suspension",
            "shock absorber",
            "strut",
            "pulling",
        ],
    ):
        result_data = diagnose_steering_issue(messages)

        if result_data:
            return result_data

    # -----------------------------------------------------
    # Transmission / clutch
    # -----------------------------------------------------

    if contains_any(
        text,
        [
            "clutch",
            "gearbox",
            "transmission",
            "gear",
        ],
    ):
        result_data = diagnose_transmission_issue(messages)

        if result_data:
            return result_data

    # -----------------------------------------------------
    # Oil
    # -----------------------------------------------------

    if contains_any(
        text,
        [
            "oil",
            "engine oil",
        ],
    ):
        result_data = diagnose_oil_issue(messages)

        if result_data:
            return result_data

    # -----------------------------------------------------
    # Fuel
    # -----------------------------------------------------

    if contains_any(
        text,
        [
            "fuel",
            "petrol",
            "gasoline",
            "diesel",
            "injector",
        ],
    ):
        result_data = diagnose_fuel_issue(messages)

        if result_data:
            return result_data

    # -----------------------------------------------------
    # AC
    # -----------------------------------------------------

    if contains_any(
        text,
        [
            "ac",
            "a/c",
            "air conditioner",
            "air conditioning",
            "heater",
        ],
    ):
        result_data = diagnose_ac_issue(messages)

        if result_data:
            return result_data

    # -----------------------------------------------------
    # Exhaust
    # -----------------------------------------------------

    if contains_any(
        text,
        [
            "smoke",
            "exhaust",
            "muffler",
            "catalytic",
        ],
    ):
        result_data = diagnose_exhaust_issue(messages)

        if result_data:
            return result_data

    # -----------------------------------------------------
    # Lights
    # -----------------------------------------------------

    if contains_any(
        text,
        [
            "headlight",
            "headlights",
            "tail light",
            "indicator",
            "turn signal",
            "warning light",
            "check engine",
            "abs light",
        ],
    ):
        result_data = diagnose_lights_issue(messages)

        if result_data:
            return result_data

    # -----------------------------------------------------
    # Horn
    # -----------------------------------------------------

    if "horn" in text:
        result_data = diagnose_horn_issue(messages)

        if result_data:
            return result_data

    # -----------------------------------------------------
    # Nothing specific
    # -----------------------------------------------------

    return None