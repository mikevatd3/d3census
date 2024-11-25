import pandas as pd

from d3census.edition import ACSEdition
from d3census.geography import Geography
from d3census.variable import  DefinedVariable

from d3census.receiving import build_calls, run_calls, saturate_geography


def build_profile(
    geographies: list[Geography],
    variables: list[DefinedVariable],
    edition: ACSEdition,
    api_key: str = ""
) -> pd.DataFrame:

    calls = build_calls(geographies, variables, edition, api_key)
    responses = run_calls(calls)
    geos = [saturate_geography(response) for response in responses]

    rows = []
    for geo in geos:
        rows.append({
            "geoid": geo.geoid, # type: ignore
            "name": geo.name, # type: ignore
            **{
                variable.function.__name__: variable.function(geo)
                for variable in variables
            }
        })
    
    return pd.DataFrame(rows)
