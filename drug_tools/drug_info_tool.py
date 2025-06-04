import pandas as pd
from agents import function_tool
        # Implementation here

SINGLE_DRUG_DATA = 'data/Data Record 3 - Single-drug ADRs, indications and negative controls.xlsx'


@function_tool
def get_drug_indications(drug: str):
    """
    Get information about a drug indications from the CRESCENDDI database.
    """
    print(f"Getting indications for {drug}")

    data = pd.read_excel('data/Data Record 3 - Single-drug ADRs, indications and negative controls.xlsx', sheet_name="Tab1 - Positive")
    drug_indications = data[(data['DRUG_CONCEPT_NAME'] == drug) & (data['EVENT_TYPE'] == 'Indication')].rename(columns={"EVENT_CONCEPT_NAME": "INDICATION"})

    return drug_indications[["DRUG_CONCEPT_NAME", "INDICATION"]]

@function_tool
def get_drug_adverse_effects(drug: str):
    """
    Get information about a drug adverse effects from the CRESCENDDI database.
    """
    print(f"Getting adverse effects for {drug}")

    data = pd.read_excel('data/Data Record 3 - Single-drug ADRs, indications and negative controls.xlsx', sheet_name="Tab1 - Positive")
    drug_indications = data[(data['DRUG_CONCEPT_NAME'] == drug) & (data['EVENT_TYPE'] == 'Adverse event')].rename(columns={"EVENT_CONCEPT_NAME": "ADVERSE_EFFECT"})

    return drug_indications[["DRUG_CONCEPT_NAME", "ADVERSE_EFFECT"]]

@function_tool
def get_negative_effects(drug: str, effects: str):
    """
    Get information about the absence of link between drugs and effects from the CRESCENDDI database.
    """
    print(f"Getting links between {drug} and {effects}")

    data = pd.read_excel('data/Data Record 3 - Single-drug ADRs, indications and negative controls.xlsx', sheet_name="Tab2 - Negative")
    no_links = data[(data['DRUG_CONCEPT_NAME'] == drug) & (data["EVENT_CONCEPT_NAME"] == effects)].rename(columns={"EVENT_CONCEPT_NAME": "NO_LINK"})

    return no_links[["DRUG_CONCEPT_NAME", "NO_LINK"]]