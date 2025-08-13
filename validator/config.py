

class WebAppConfig:
    # Primary Diagnosis: Dark Green (#23a373)
    PRIMARY_DIAG_STYLE = {
        "color": "#145A32", "backgroundColor": "#E9F5EF", "padding": "2px 4px",
        "borderRadius": "4px", "fontWeight": "bold"
    }
    # Related Diagnosis: Light Green (#8abb4c)
    OTHER_DIAG_STYLE = {
        "color": "#515A48", "backgroundColor": "#F3F8EC", "padding": "2px 4px",
        "borderRadius": "4px", "fontStyle": "italic"
    }
    # Major Procedure: Dark Purple (#875eaf)
    MAJOR_PROC_STYLE = {
        "color": "#4A235A", "backgroundColor": "#F3EFF7", "padding": "2px 4px",
        "borderRadius": "4px", "fontWeight": "bold"
    }
    # Other Procedures: Light Purple (#d1a9da)
    OTHER_PROC_STYLE = {
        "color": "#6C3483", "backgroundColor": "#FBF5FC", "padding": "2px 4px",
        "borderRadius": "4px", "fontStyle": "italic" 
    }

    BASE_STYLE = {
        "padding": "2px 4px", "borderRadius": "4px", "cursor": "pointer", 
        "transition": "all 0.2s ease-in-out"}
    
    HOVER_STYLE = {"boxShadow": "0px 0px 8px rgba(0, 0, 0, 0.3)"}

    TOOLTIP_STYLE = {
        'font-size': '1.1em',
        'background-color': '#343a40',
        'color': 'white',
        'border-radius': '6px',
        'padding': '10px'
    }
