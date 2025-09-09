import dataiku
from webaiku.apis.dataiku.api import dataiku_api
from webaiku.apis.dataiku.formula import DataikuFormula
from webaiku.apis.dataiku.filters import CustomFilter, FilterType
from typing import List, Dict, TypedDict, Union, Optional
import io
import pandas as pd
import functools

CSV_SEP = "\t"
CSV_DOUBLE_QUOTE = True
CSV_QUOTE_CHAR = '"'


class DatasetFilter(TypedDict):
    column: str
    filter: CustomFilter


def get_project_variables():
    project = dataiku_api.project
    variables = project.get_variables()
    return variables


@functools.cache
def include_sdoh():
    project_variables = get_project_variables()
    return project_variables.get("standard", {}).get("sdoh_data", None)


@functools.cache
def k_neighbors() -> int:
    project_variables = get_project_variables()
    return project_variables.get("standard", {}).get("k_neighbors", 20)


def create_filter_expression(filters: List[DatasetFilter]):
    formula = DataikuFormula()
    for filter in filters:
        formula.filter_column_by_custom_filters(filter["column"], filter["filter"])
    return formula.execute()


def filter_dataset(
    datasetName: str,
    filters: Union[List[DatasetFilter], str],
    columns: Optional[List[str]] = None,
    infer_with_pandas=True,
    parse_dates=True,
    bool_as_str=False,
    float_precision=None,
    na_values=None,
    keep_default_na=True,
):
    dataset = dataiku.Dataset(project_key=dataiku_api.project_key, name=datasetName)
    (names, dtypes, parse_date_columns) = dataset._get_dataframe_schema(
        parse_dates=parse_dates,
        infer_with_pandas=infer_with_pandas,
        bool_as_str=bool_as_str,
    )

    req_data = {
        "filterExpression": create_filter_expression(filters=filters)
        if isinstance(filters, list)
        else filters,
        "format": "tsv-excel-noheader",
    }

    path = f"/projects/{dataiku_api.project_key}/datasets/{datasetName}/data"
    response = dataiku_api._client._perform_raw("POST", path=path, body=req_data)
    if response.status_code == 200:
        sd = io.BytesIO()
        sd.write(response.raw.data)
        sd.seek(0)
        result = pd.read_table(
            sd,
            names=names,
            dtype=dtypes,
            header=None,
            sep=CSV_SEP,
            doublequote=CSV_DOUBLE_QUOTE,
            quotechar=CSV_QUOTE_CHAR,
            parse_dates=parse_date_columns,
            float_precision=float_precision,
            na_values=na_values,
            keep_default_na=keep_default_na,
        )
        if columns and len(columns) > 1:
            result = result[columns]
        return result
    else:
        err_data = response.text
        if err_data:
            raise Exception(
                "Failed to retreive sampled Dataset %s : %s" % (datasetName, err_data)
            )
        else:
            raise Exception("Failed to retreive sampled Dataset %s" % (datasetName))


def filter_dataset_by_note_id(
    datasetName: str, note_id: str, columns: Optional[str] = None
) -> pd.DataFrame:
    custom_filter = CustomFilter(
        filterType=FilterType.Equals, value=note_id, toValue=None, operator="and"
    )
    datasetFilter = DatasetFilter(column="note_id", filter=custom_filter)
    return filter_dataset(
        datasetName=datasetName, filters=[datasetFilter], columns=columns
    )
