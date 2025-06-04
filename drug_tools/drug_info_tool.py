import pandas as pd
from agents import function_tool

SINGLE_DRUG_DATA = 'data/Data Record 3 - Single-drug ADRs, indications and negative controls.xlsx'


@function_tool
def get_drug_indications(drug: str):
    """
    Retrieve therapeutic indications for a drug from the CRESCENDDI database.

    This tool returns medical conditions for which the drug is positively associated
    as a treatment (i.e., known indications).

    Only returns confirmed positive relationships. No off-label or experimental data is included.
    """
    print(f"Getting indications for {drug}")

    data = pd.read_excel('data/Data Record 3 - Single-drug ADRs, indications and negative controls.xlsx', sheet_name="Tab1 - Positive")
    drug_indications = data[(data['DRUG_CONCEPT_NAME'].str.lower() == drug.lower()) & (data['EVENT_TYPE'] == 'Indication')].rename(columns={"EVENT_CONCEPT_NAME": "INDICATION"})

    return drug_indications[["DRUG_CONCEPT_NAME", "INDICATION"]]

@function_tool
def get_drug_adverse_effects(drug: str):
    """
    Retrieve known adverse effects associated with a drug, from the CRESCENDDI database.

    This tool returns all reported adverse events linked to the drug, as positive associations.
    Each event represents a confirmed side effect based on the database.
    """
    print(f"Getting adverse effects for {drug}")

    data = pd.read_excel('data/Data Record 3 - Single-drug ADRs, indications and negative controls.xlsx', sheet_name="Tab1 - Positive")
    drug_indications = data[(data['DRUG_CONCEPT_NAME'].str.lower() == drug.lower()) & (data['EVENT_TYPE'] == 'Adverse event')].rename(columns={"EVENT_CONCEPT_NAME": "ADVERSE_EFFECT"})

    return drug_indications[["DRUG_CONCEPT_NAME", "ADVERSE_EFFECT"]]

@function_tool
def get_negative_effects(drug: str, effects: str):
    """
    Check whether a drug has *no known association* with a specific effect or condition.

    This tool returns cases where the drug is not known to cause or treat the given effect,
    based on negative controls in the CRESCENDDI database.

    Use this to confirm the absence of a link between a drug and a suspected effect.
    """
    print(f"Getting links between {drug} and {effects}")

    data = pd.read_excel('data/Data Record 3 - Single-drug ADRs, indications and negative controls.xlsx', sheet_name="Tab2 - Negative")
    no_links = data[(data['DRUG_CONCEPT_NAME'].str.lower() == drug.lower()) & (data["EVENT_CONCEPT_NAME"].str.lower() == effects.lower())].rename(columns={"EVENT_CONCEPT_NAME": "NO_LINK"})

    return no_links[["DRUG_CONCEPT_NAME", "NO_LINK"]]