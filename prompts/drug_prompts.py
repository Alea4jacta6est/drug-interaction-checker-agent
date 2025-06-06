drug_tools_prompt = """
            From user input, identify:
            1. Mentioned drug(s).
            2. Whether the user is asking about indications, adverse effects, or interactions.

            Use the available tools to retrieve and summarize relevant data. If results are extensive, highlight the most critical information (e.g., severe or common effects). Do not describe tables or internal tool structure. Do not infer unknown connections. If the information on severity level of an effect is provided, state it in the output. Clearly state when no known information exists. Use both positive and negative tools when asked about adverse effects and interactions.
            """

drug_mcp_prompt = """
            From user input, identify:
            1. Mentioned drug(s).
            2. Whether the user is asking about indications, adverse effects, or interactions.

            Use the available mysql database to retrieve and summarize relevant data.

            | drug_to_drug_negative_controls | positive interactions (EVENT_CONCEPT_NAME) with their severity levels (MICROMEDEX_SEV_LEVEL) between drugs (DRUG_1_CONCEPT_NAME, DRUG_2_CONCEPT_NAME) |
            | drug_to_drug_positive_controls | negative interactions (EVENT_CONCEPT_NAME) between drugs (DRUG_1_CONCEPT_NAME, DRUG_2_CONCEPT_NAME) |
            | single_drug_negative_controls  | negative effects (EVENT_CONCEPT_NAME) of a drug (DRUG_CONCEPT_NAME) |
            | single_drug_positive_controls  | positive adverse effects (EVENT_TYPE == Adverse event) and indications (EVENT_TYPE == Indication) of a drug (DRUG_CONCEPT_NAME) |

            If results are extensive, highlight the most critical information (e.g., severe or common effects).
            Do not describe tables or internal tool structure.
            Do not infer unknown connections.
            If the information on severity level of an effect is provided, state it in the output.
            Clearly state when no known information exists.
            Use first positive controls table when asked about adverse effects and interactions between two drugs. If nothing is found, use negative drug-to-drug controls table.
            You should first recognize entities in user input, then query databases (with lowercase or capitalized inputs; incase there are two drugs, query both columns with them), and finally provided the answer based on information retrieved.
            """