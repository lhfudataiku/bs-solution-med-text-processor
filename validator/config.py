class WebAppConfig:
    # --- Base & Global Styles ---
    # Common styles shared across multiple components
    BASE_STYLE = {
        "padding": "2px 4px",
        "borderRadius": "4px",
        "cursor": "pointer",
        "transition": "all 0.2s ease-in-out"
    }
    
    HOVER_STYLE = {"boxShadow": "0px 0px 8px rgba(0, 0, 0, 0.3)"}

    TOOLTIP_STYLE = {
        'fontSize': '1.1em',
        'backgroundColor': '#343a40',
        'color': 'white',
        'borderRadius': '6px',
        'padding': '10px'
    }

    # --- Nested Classes for Grouping ---

    class Diagnosis:
        """Contains styles related to medical diagnoses."""
        # Specific styles are defined privately
        _primary_specific = {"color": "#145A32", "backgroundColor": "#E9F5EF", "fontWeight": "bold"}
        _other_specific = {"color": "#515A48", "backgroundColor": "#F3F8EC", "fontStyle": "italic"}

        # Public styles are created by merging base and specific styles
        @classmethod
        def get_primary_style(cls):
            return {**WebAppConfig.BASE_STYLE, **cls._primary_specific}
        
        @classmethod
        def get_other_style(cls):
            return {**WebAppConfig.BASE_STYLE, **cls._other_specific}

    class Procedure:
        """Contains styles related to medical procedures."""
        # Specific styles
        _major_specific = {"color": "#4A235A", "backgroundColor": "#F3EFF7", "fontWeight": "bold"}
        _other_specific = {"color": "#6C3483", "backgroundColor": "#FBF5FC", "fontStyle": "italic"}

        # Public, merged styles
        @classmethod
        def get_major_style(cls):
            return {**WebAppConfig.BASE_STYLE, **cls._major_specific}
        
        @classmethod
        def get_other_style(cls):
            return {**WebAppConfig.BASE_STYLE, **cls._other_specific}
        
class WebAppVariables:
    MODEL_BILLING_DATASET = "notes_llm_billing_w_labels"
    NOTE_METADATA_DATASET = "clinical_notes_prepared"
    NOTE_SUMMARY_DATASET = "notes_summarization"
    VISUALEDIT_VIEW_EDITS_DATASET = "billing_codes_validation_view_edits"
    VISUALEDIT_VIEW_EDITLOG_DATASET = "billing_codes_validation_view_editlog"
    VISUALEDIT_VIEW_EDITED_DATASET = "billing_codes_validation_view_edited"
    CODE_REFERENCE = "billing_codes_reference"
