from agents import function_tool
from drug_tools.data_sources import DRUG_TO_DRUG_POSITIVE, DRUG_TO_DRUG_NEGATIVE
from drug_tools.utils import load_excel


@function_tool
def get_positive_interactions(drug1: str, drug2: str):
    """
    Retrieve confirmed drug-drug interactions between two drugs, including severity levels.

    This tool queries the CRESCENDDI database for known interactions, such as adverse outcomes
    when the two drugs are combined. It also includes severity levels from ANSM data.

    Use this to check for clinically relevant interactions.
    """
    print(f"Getting positive effects between {drug1} and {drug2}")

    df = load_excel(DRUG_TO_DRUG_POSITIVE)
    filtered = df[
        (df['DRUG_1_CONCEPT_NAME'].str.lower() == drug1.lower()) &
        (df['DRUG_2_CONCEPT_NAME'].str.lower() == drug2.lower())
    ]
    return filtered.rename(columns={
        "EVENT_CONCEPT_NAME": "LINKED_EFFECT",
        "ANSM_SEV_LEVEL": "SEVERITY_LEVEL"
    })[
        ["DRUG_1_CONCEPT_NAME", "DRUG_2_CONCEPT_NAME", "LINKED_EFFECT", "SEVERITY_LEVEL"]
    ]

@function_tool
def get_negative_interactions(drug1: str, drug2: str):
    """
    Confirm the *absence* of a known interaction between two drugs.

    This tool checks the CRESCENDDI negative control dataset and returns a result
    when no interaction has been observed or reported.

    Useful for validating safety or ruling out interactions.
    """
    print(f"Getting negative effects between {drug1} and {drug2}")

    df = load_excel(DRUG_TO_DRUG_NEGATIVE)
    filtered = df[
        (df['DRUG_1_CONCEPT_NAME'].str.lower() == drug1.lower()) &
        (df['DRUG_2_CONCEPT_NAME'].str.lower() == drug2.lower())
    ]
    return filtered.rename(columns={"EVENT_CONCEPT_NAME": "NO_LINK"})[
        ["DRUG_1_CONCEPT_NAME", "DRUG_2_CONCEPT_NAME", "NO_LINK"]
    ]