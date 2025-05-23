from typing import Any
from itertools import product
import asyncio

from d3census.variable import DefinedVariable
from d3census.geography import (
    consolidate_calls,
    create_consolodated_api_calls,
    FullGeography,
    Geography,
)
from d3census.edition import ACSEdition
from d3census.requestmanager import request_manager
from d3census.reference import ERA_STR_TRANSLATION

from d3census.reference import (
    SumLevel,
    GEO_TO_API_PARAMS,
    SUMLEV_FROM_PARTS,
    SUMLEV_TO_STEM,
    GEOID_DECOMPOSER,
)


def build_calls(
    geographies: list[Geography],
    variables: list[DefinedVariable],
    edition: ACSEdition,
    api_key: str = "",
) -> list[str]:
    shopping_list = set()
    for variable in variables:
        shopping_list.update(variable.shopping_list)

    base_url = f"https://api.census.gov/data/{edition.year}/acs/{ERA_STR_TRANSLATION[edition.era]}"
    key_string = f"&key={api_key}" if api_key else ""

    call_tree = consolidate_calls(geographies)
    geo_parts = create_consolodated_api_calls(call_tree)
    
    def chunk(lst, n):
        for i in range(0, len(lst), n):
            yield lst[i:i+n]

    # chunk out var string to 50 vars
    
    template = "{base_url}?get=NAME,{vars_str}&{geo_part}{key_string}"

    return [
        template.format(
            base_url=base_url,
            vars_str=",".join(vars_str),
            geo_part=geo_part,
            key_string=key_string,
        )
        for geo_part, vars_str in product(geo_parts, chunk(list(shopping_list), 25))
    ]


def safeish_float_cast(value: Any) -> str | float:
    try:
        return float(value)
    except (ValueError, TypeError):
        return float("NaN")


def build_geoid(row: dict, sumlevel: SumLevel):
    stem = SUMLEV_TO_STEM[sumlevel]
    parts = GEOID_DECOMPOSER[sumlevel].keys()
    
    if sumlevel == SumLevel.ZCTA:
        parts = {part for part in parts if part != SumLevel.STATE}

    return stem + "US" + "".join(row[part] for part in parts)


def run_calls(calls):
    """
    WARNING: this does two things -- makes the requests and prepares the
    response to interface with the rest of the system.
    """
    # Concern one is only one line, so that's why its here.
    responses = asyncio.run(request_manager(calls))

    dicts = []
    for msg in responses:
        header, *rows = msg

        sumlev_key = frozenset(
            {
                GEO_TO_API_PARAMS[col]
                for col in header
                if col in GEO_TO_API_PARAMS
            }
        )
        sumlevel = SUMLEV_FROM_PARTS[sumlev_key]

        # Now we know what the geoids are, we can reassemble the full geoids
        labeled = [
            {
                GEO_TO_API_PARAMS.get(key, key): val
                for key, val in zip(header, row)
            }
            for row in rows
        ]

        dicts.extend(
            [
                {"geoid": build_geoid(row, sumlevel)}
                | {"name": row["NAME"].replace(";", ",")}
                | {
                    key: safeish_float_cast(
                        val
                    )  # Need to cast this to a float or something
                    for key, val in row.items()
                    if ((not isinstance(key, SumLevel)) and (key != "NAME"))
                }
                for row in labeled
            ]
        )

    return dicts


class ACSTable:
    """
    This is the empty table type that can be instantiated
    to then fill with value attributes.
    """


def saturate_geography(row):
    result = FullGeography()

    for key, value in row.items():
        try:
            table, variable = key.split("_")

            if not hasattr(result, table):
                result.__setattr__(table, ACSTable())

            result.__getattribute__(table).__setattr__(
                "_" + variable, safeish_float_cast(value)
            )  # The casting should probably be done elsewhere

        except ValueError:
            result.__setattr__(key, value)

    return result
