import pandas as pd

from agents import function_tool

DRUG_TO_DRUG_POSITIVE = 'data/Data Record 1 - Positive Controls.xlsx'
DRUG_TO_DRUG_NEGATIVE = 'data/Data Record 2 - Negative Controls.xlsx'

@function_tool
def get_positive_interactions(drug1: str, drug2: str):
    """
    Retrieve confirmed drug-drug interactions between two drugs, including severity levels.

    This tool queries the CRESCENDDI database for known interactions, such as adverse outcomes
    when the two drugs are combined. It also includes severity levels from ANSM data.

    Use this to check for clinically relevant interactions.
    """
    print(f"Getting positive effects between {drug1} and {drug2}")

    data = pd.read_excel('data/Data Record 1 - Positive Controls.xlsx')
    pos_effects = data[(data['DRUG_1_CONCEPT_NAME'].str.lower() == drug1.lower()) & (data["DRUG_2_CONCEPT_NAME"].str.lower() == drug2.lower())].rename(columns={"EVENT_CONCEPT_NAME": "LINKED_EFFECT", "ANSM_SEV_LEVEL": "SEVERITY_LEVEL"})

    return pos_effects[["DRUG_1_CONCEPT_NAME", "DRUG_2_CONCEPT_NAME", "LINKED_EFFECT", "SEVERITY_LEVEL"]]

@function_tool
def get_negative_interactions(drug1: str, drug2: str):
    """
    Confirm the *absence* of a known interaction between two drugs.

    This tool checks the CRESCENDDI negative control dataset and returns a result
    when no interaction has been observed or reported.

    Useful for validating safety or ruling out interactions.
    """
    print(f"Getting negative effects between {drug1} and {drug2}")

    data = pd.read_excel("data/Data Record 2 - Negative Controls.xlsx")
    neg_effects = data[(data['DRUG_1_CONCEPT_NAME'].str.lower() == drug1.lower()) & (data["DRUG_2_CONCEPT_NAME"].str.lower() == drug2.lower())].rename(columns={"EVENT_CONCEPT_NAME": "NO_LINK"})

    return neg_effects[["DRUG_1_CONCEPT_NAME", "DRUG_2_CONCEPT_NAME", "NO_LINK"]]