from agents import function_tool
from drug_tools.data_sources import SINGLE_DRUG_DATA
from drug_tools.utils import load_excel


@function_tool
def get_drug_indications(drug: str):
    """
    Retrieve therapeutic indications for a drug from the CRESCENDDI database.

    This tool returns medical conditions for which the drug is positively associated
    as a treatment (i.e., known indications).

    Only returns confirmed positive relationships. No off-label or experimental data is included.
    """
    print(f"Getting indications for {drug}")

    df = load_excel(SINGLE_DRUG_DATA, "Tab1 - Positive")
    filtered = df[
        (df['DRUG_CONCEPT_NAME'].str.lower() == drug.lower()) &
        (df['EVENT_TYPE'] == 'Indication')
    ]
    return filtered.rename(columns={"EVENT_CONCEPT_NAME": "INDICATION"})[
        ["DRUG_CONCEPT_NAME", "INDICATION"]
    ]

@function_tool
def get_drug_adverse_effects(drug: str):
    """
    Retrieve known adverse effects associated with a drug, from the CRESCENDDI database.

    This tool returns all reported adverse events linked to the drug, as positive associations.
    Each event represents a confirmed side effect based on the database.
    """
    print(f"Getting adverse effects for {drug}")

    df = load_excel(SINGLE_DRUG_DATA, "Tab1 - Positive")
    filtered = df[
        (df['DRUG_CONCEPT_NAME'].str.lower() == drug.lower()) &
        (df['EVENT_TYPE'] == 'Adverse event')
    ]
    return filtered.rename(columns={"EVENT_CONCEPT_NAME": "ADVERSE_EFFECT"})[
        ["DRUG_CONCEPT_NAME", "ADVERSE_EFFECT"]
    ]

@function_tool
def get_negative_effects(drug: str, effects: str):
    """
    Check whether a drug has *no known association* with a specific effect or condition.

    This tool returns cases where the drug is not known to cause or treat the given effect,
    based on negative controls in the CRESCENDDI database.

    Use this to confirm the absence of a link between a drug and a suspected effect.
    """
    print(f"Getting negative effects for {drug} and {effects}")

    df = load_excel(SINGLE_DRUG_DATA, "Tab2 - Negative")
    filtered = df[
        (df['DRUG_CONCEPT_NAME'].str.lower() == drug.lower()) &
        (df['EVENT_CONCEPT_NAME'].str.lower() == effects.lower())
    ]
    return filtered.rename(columns={"EVENT_CONCEPT_NAME": "NO_LINK"})[
        ["DRUG_CONCEPT_NAME", "NO_LINK"]
    ]