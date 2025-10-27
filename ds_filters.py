import dataiku
import pandas as pd
from typing import List, Dict, Optional


def get_project_variables():
    """Get project variables from Dataiku."""
    project = dataiku.api_client().get_project()
    variables = project.get_variables()
    return variables


def filter_dataset(
    dataset_name: str,
    filters: Optional[Dict] = None,
    columns: Optional[List[str]] = None,
    infer_with_pandas=True,
    parse_dates=True,
    bool_as_str=False,
    float_precision=None,
    na_values=None,
    keep_default_na=True,
):
    """
    Filter a Dataiku dataset using pandas native operations.
    
    Args:
        dataset_name: Name of the dataset to filter
        filters: Dictionary with filtering criteria
        columns: List of columns to select
        infer_with_pandas: Whether to infer dtypes with pandas
        parse_dates: Whether to parse dates
        bool_as_str: Whether to treat booleans as strings
        float_precision: Float precision for reading
        na_values: Values to treat as NA
        keep_default_na: Whether to keep default NA values
    
    Returns:
        Filtered pandas DataFrame
    """
    dataset = dataiku.Dataset(dataset_name)
    
    # Get the full dataset first
    df = dataset.get_dataframe(
        infer_with_pandas=infer_with_pandas,
        parse_dates=parse_dates,
        bool_as_str=bool_as_str,
        float_precision=float_precision,
        na_values=na_values,
        keep_default_na=keep_default_na
    )
    
    # Apply filters if provided
    if columns:
        available_columns = [col for col in columns if col in df.columns]
        df = df[available_columns]
        
    if filters:
        df = apply_filters(df, filters)
    
    return df


def apply_filters(df: pd.DataFrame, filters: Dict) -> pd.DataFrame:
    """
    Apply filtering criteria to a DataFrame using pandas native operations.
    
    Args:
        df: DataFrame to filter
        filters: Dictionary containing filter criteria
    
    Returns:
        Filtered DataFrame
    """
    filtered_df = df.copy()
    
    for column, criteria in filters.items():
        if column not in filtered_df.columns:
            continue
            
        if isinstance(criteria, dict):
            # Handle different filter types
            if 'equals' in criteria:
                values = criteria['equals']
                if isinstance(values, list):
                    filtered_df = filtered_df[filtered_df[column].isin(values)]
                else:
                    filtered_df = filtered_df[filtered_df[column] == values]
            
            elif 'contains' in criteria:
                value = criteria['contains']
                filtered_df = filtered_df[filtered_df[column].astype(str).str.contains(str(value), na=False)]
            
            elif 'not_equals' in criteria:
                values = criteria['not_equals']
                if isinstance(values, list):
                    filtered_df = filtered_df[~filtered_df[column].isin(values)]
                else:
                    filtered_df = filtered_df[filtered_df[column] != values]
            
            elif 'greater_than' in criteria:
                filtered_df = filtered_df[filtered_df[column] > criteria['greater_than']]
            
            elif 'less_than' in criteria:
                filtered_df = filtered_df[filtered_df[column] < criteria['less_than']]
            
            elif 'between' in criteria:
                min_val, max_val = criteria['between']
                filtered_df = filtered_df[(filtered_df[column] >= min_val) & (filtered_df[column] <= max_val)]
        
        elif isinstance(criteria, list):
            # Simple list of values to match
            filtered_df = filtered_df[filtered_df[column].isin(criteria)]
        
        else:
            # Single value to match
            filtered_df = filtered_df[filtered_df[column] == criteria]
    
    return filtered_df


def filter_dataset_by_note_id(
    dataset_name: str, 
    note_id: str, 
    columns: Optional[List[str]] = None
) -> pd.DataFrame:
    """
    Filter dataset by note_id using pandas native operations.
    
    Args:
        dataset_name: Name of the dataset
        note_id: Note ID to filter by
        columns: Optional list of columns to select
    
    Returns:
        Filtered DataFrame
    """
    filters = {
        'note_id': {'equals': note_id}
    }
    return filter_dataset(
        dataset_name=dataset_name, 
        filters=filters, 
        columns=columns
    )


def filter_by_column_values(
    dataset_name: str,
    column: str,
    values: List,
    columns: Optional[List[str]] = None
) -> pd.DataFrame:
    """
    Filter dataset by specific column values.
    
    Args:
        dataset_name: Name of the dataset
        column: Column name to filter by
        values: List of values to match
        columns: Optional list of columns to select
    
    Returns:
        Filtered DataFrame
    """
    filters = {
        column: {'equals': values}
    }
    return filter_dataset(
        dataset_name=dataset_name,
        filters=filters,
        columns=columns
    )


def filter_by_column_contains(
    dataset_name: str,
    column: str,
    value: str,
    columns: Optional[List[str]] = None
) -> pd.DataFrame:
    """
    Filter dataset by column containing a specific value.
    
    Args:
        dataset_name: Name of the dataset
        column: Column name to filter by
        value: Value to search for
        columns: Optional list of columns to select
    
    Returns:
        Filtered DataFrame
    """
    filters = {
        column: {'contains': value}
    }
    return filter_dataset(
        dataset_name=dataset_name,
        filters=filters,
        columns=columns
    )


def filter_by_multiple_conditions(
    dataset_name: str,
    conditions: Dict[str, Dict],
    columns: Optional[List[str]] = None
) -> pd.DataFrame:
    """
    Filter dataset by multiple conditions.
    
    Args:
        dataset_name: Name of the dataset
        conditions: Dictionary mapping column names to their filter criteria
        columns: Optional list of columns to select
    
    Returns:
        Filtered DataFrame
    """
    return filter_dataset(
        dataset_name=dataset_name,
        filters=conditions,
        columns=columns
    )