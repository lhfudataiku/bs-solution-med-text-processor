from dash import html
import dash_bootstrap_components as dbc
import re
import json
from typing import List

from webapp.ds_filters import filter_dataset
from webapp.config import WebAppConfig, WebAppVariables


def get_llm_outputs_by_note_id(note_id):
    filters = {
        "note_id": {"equals": [note_id]}
    }
    output_df = filter_dataset(
        WebAppVariables.MODEL_BILLING_DATASET, filters=filters
    )
    return output_df

def get_note_metadata_by_note_id(note_id):
    filters = {
        "note_id": {"equals": [note_id]}
    }
    output_df = filter_dataset(
        WebAppVariables.NOTE_METADATA_DATASET, filters=filters
    )
    return output_df

def get_committed_note_ids():
    filters = {
        "Verified": {"equals": [str(True)]}
    }
    output_df = filter_dataset(
        WebAppVariables.VISUALEDIT_VIEW_EDITS_DATASET, 
        filters=filters, 
        columns=['Note ID', 'Verified'],
        keep_default_na=False
    )
    return output_df['Note ID'].unique()

def get_note_summary_by_note_id(note_id):
    filters = {
        "note_id": {"equals": [note_id]}
    }
    output_df = filter_dataset(
        WebAppVariables.NOTE_SUMMARY_DATASET, filters=filters
    )
    return output_df

def get_verified_codes_by_note_id(note_id):
    filters = {
        "Note ID": {"equals": [note_id]},
        "Verified": {"equals": [str(True)]}
    }
    output_df = filter_dataset(
        WebAppVariables.VISUALEDIT_VIEW_EDITED_DATASET, 
        filters=filters, 
        columns=['Note ID', 'No', 'Concept type', 'Mapped billing code', 'Verified', 'Comments'],
        keep_default_na=False
    )
    return output_df

def get_code_labels(codes: List[str]):
    filters = {
        "billing_references": {"equals": codes}
    }
    output_df = filter_dataset(
        WebAppVariables.CODE_REFERENCE, 
        filters=filters, 
        columns = ['billing_references', 'label']
    )
    return output_df

def get_edit_logs_by_note_id(note_id):
    filters = {
        "key": {"contains": note_id}
    }
    output_df = filter_dataset(
        WebAppVariables.VISUALEDIT_VIEW_EDITLOG_DATASET, 
        filters=filters,
        columns=['date', 'user', 'key', 'column_name']
    )
    return output_df

def read_note_id(filters):
    if not isinstance(filters, list):
        return None
    try:
        for fitem in filters:
            if isinstance(fitem, dict) and fitem.get('column') == 'Note ID':
                selected_values = fitem.get('selectedValues')
                if isinstance(selected_values, dict) and selected_values:
                    return next(iter(selected_values))
    except Exception:
        return None
    return None

def create_evidence_details_map(df, domain_style_map):
    """
    Creates a single dictionary mapping each evidence string to its style
    and its correspnding concept text for the tooltip.
    
    Args:
        df (pd.DataFrame): The dataframe containing the LLM outputs.
        domain_style_map (dict): A mapping of domain names to style dictionaries.
    
    Returns:
        dict: A map like {evidences_string: {style: style_dict, concept: concept_text}}
    """

    evidence_map = {}
    for domain, style in domain_style_map.items():
        domain_df  = df[df['domain'] == domain]
        for _, row in domain_df.iterrows():
            concept = row.get('concept', 'N/A')
            domain = row.get('domain', 'N/A')
            try:
                evidence_list = json.loads(row.get('evidence', '[]'))
                for evidence_str in evidence_list:
                    quote = evidence_str.strip()
                    if quote and quote not in evidence_map:
                        evidence_map[quote] = {'style': style,'concept': concept, 'domain': domain}
            except (json.JSONDecodeError, TypeError):
                continue
    return evidence_map

def build_styled_text_components(text, details_map):
    """
    splits text into a list of strings and styled html.Span components,
    adding a 'title' attribte for hover text.
    """
    if not details_map:
        # split by newlines
        return [html.P(line) for line in text.split('\n')]
    
    # create a regex pattern that finds all quotes to be styled
    pattern = re.compile(f"({'|'.join(re.escape(key) for key in sorted(details_map.keys(), key=len, reverse=True))})")
    # split the text by the found quotes
    text_parts = pattern.split(text)
    
    # build the list of components
    final_components = []
    tooltip_components = []
    evidence_counter = 0

    for part in text_parts:
        if not part:
            continue
        if part in details_map:
            details = details_map[part]
            component_id = f"evidence-span-{evidence_counter}"
            evidence_counter += 1

            final_components.append(html.Span(part, style=details['style'], id=component_id))
            tooltip_components.append(dbc.Tooltip(f"{details['domain']}: {details['concept']}", target=component_id, style=WebAppConfig.TOOLTIP_STYLE))
        else:
            for i, line in enumerate(part.split('\n')):
                if line:
                    final_components.append(line)
                # add to line breaks for each newline character, except the last one
                if i < len(part.split('\n')) - 1:
                    final_components.append(html.Br())
                    final_components.append(html.Br())
    styled_text_div = html.Div(final_components, style={'line-height': '1.8', 'text-align': 'justify'})               
    return styled_text_div, tooltip_components
