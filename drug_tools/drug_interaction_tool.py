import pandas as pd

from agents import function_tool

DRUG_TO_DRUG_POSITIVE = 'data/Data Record 1 - Positive Controls.xlsx'
DRUG_TO_DRUG_NEGATIVE = 'data/Data Record 2 - Negative Controls.xlsx'

@function_tool
def get_positive_interactions(drug1: str, drug2: str):
    """
    Get information about drug1 and drug2 interactions from the CRESCENDDI database.
    """
    print(f"Getting positive effects between {drug1} and {drug2}")

    data = pd.read_excel('data/Data Record 1 - Positive Controls.xlsx')
    pos_effects = data[(data['DRUG_1_CONCEPT_NAME'] == drug1) & (data["DRUG_2_CONCEPT_NAME"] == drug2)].rename(columns={"EVENT_CONCEPT_NAME": "LINKED_INTERACTION", "ANSM_SEV_LEVEL": "SEVERITY_LEVEL"})

    return pos_effects[["DRUG_1_CONCEPT_NAME", "DRUG_2_CONCEPT_NAME", "LINKED_INTERACTION", "SEVERITY_LEVEL"]]

@function_tool
def get_negative_interactions(drug1: str, drug2: str):
    """
    Get information about the absence of interaction between drug1 and drug2 from the CRESCENDDI database.
    """
    print(f"Getting negative effects between {drug1} and {drug2}")

    data = pd.read_excel("data/Data Record 2 - Negative Controls.xlsx")
    neg_effects = data[(data['DRUG_1_CONCEPT_NAME'] == drug1) & (data["DRUG_2_CONCEPT_NAME"] == drug2)].rename(columns={"EVENT_CONCEPT_NAME": "NO_LINK"})

    return neg_effects[["DRUG_CONCEPT_NAME", "NO_LINK"]]