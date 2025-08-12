from dash import html
import dataiku
import re
import json


def load_data(note_id):
    data = dataiku.Dataset("synthetic_notes_llm_billing_sorted").get_dataframe()
    return data[data['note_id'] == note_id]

def load_selected_discharge_summary(note_id):
    data = dataiku.Dataset("synthetic_notes_prepared").get_dataframe()
    return data[data['note_id'] == note_id]

def collect_evidence_from_df(df, domain):
    evidence_set = set()
    evidence_series = df.query(f"domain=='{domain}'")['evidence'].apply(json.loads).explode()
    quotes = [str(quote).strip() for quote in evidence_series if quote]
    evidence_set.update(quotes)
    return evidence_set

def read_note_id(filters):
    if not isinstance(filters, list): return None
    try:
        for fitem in filters:
            if isinstance(fitem, dict) and fitem.get('column') == 'Note ID':
                selected_values = fitem.get('selectedValues')
                if isinstance(selected_values, dict) and selected_values:
                    return next(iter(selected_values))
    except Exception: return None
    return None

def create_evidence_style_map(evidence_set, style_dict_set):
    """Map an envidence string to its corresponding sytle dictionary"""
    h_dict = {}
    for evidence, style in zip(evidence_set, style_dict_set):
        for quote in evidence:
            if quote and quote not in h_dict:
                h_dict[quote] = style
    return h_dict

def build_styled_text_components(text, style_map):
    """splits text into a list of strings and styled html.Span components"""
    if not style_map:
        # split by newlines
        return [html.P(line) for line in text.split('\n')]
    
    # create a regex pattern that finds all quotes to be styled
    pattern = re.compile(f"({'|'.join(re.escape(key) for key in sorted(style_map.keys(), key=len, reverse=True))})")
    # split the text by the found quotes
    text_parts = pattern.split(text)
    
    # build the list of components
    final_components = []
    for part in text_parts:
        if not part:
            continue
        if part in style_map:
            final_components.append(html.Span(part, style=style_map[part]))
        else:
            for i, line in enumerate(part.split('\n')):
                if line:
                    final_components.append(line)
                # add to line breaks for each newline character, except the last one
                if i < len(part.split('\n')) - 1:
                    final_components.append(html.Br())
                    final_components.append(html.Br())
                    
    return html.Div(final_components, style={'line-height': '1.8', 'text-align': 'justify'})