from collections import defaultdict
import pandas as pd

from d3census.edition import ACSEdition
from d3census.geography import Geography
from d3census.reference import SumLevel
from d3census.variable import DefinedVariable

from d3census.receiving import build_calls, run_calls, saturate_geography


class APIParameterMismatchError(Exception):
    """
    The parameter mismatch error cover errors particular to the API's
    conventions and history. For instance, ZCTAs have to have the state
    defined for years prior to 2020, otherwise they should now have the
    state defined.
    """


def build_profile(
    geographies: list[Geography],
    variables: list[DefinedVariable],
    edition: ACSEdition,
    api_key: str = "",
) -> pd.DataFrame:
    # Check for the zcta / year mismatch
    if edition.year < 2020:
        for geography in geographies:
            if (geography.sum_level == SumLevel.ZCTA) and (
                SumLevel.STATE not in geography.parts
            ):
                raise APIParameterMismatchError(
                    "When requesting ZCTAs before 2020, you must provide a state."
                )

    calls = build_calls(geographies, variables, edition, api_key)
    responses = run_calls(calls)

    geo_dicts = defaultdict(dict)

    for response in responses:
        geo_dicts[response["geoid"]].update(response)
    

    geos = [saturate_geography(response) for response in geo_dicts.values()]

    rows = []
    for geo in geos:
        rows.append(
            {
                "geoid": geo.geoid,  # type: ignore
                "name": geo.name,  # type: ignore
                **{
                    variable.function.__name__: variable.function(geo)
                    for variable in variables
                },
            }
        )

    return pd.DataFrame(rows)
