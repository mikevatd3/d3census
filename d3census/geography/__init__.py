"""
The geography module (along with reference.py) is how you define the
geography (or sets of geographies if you're using wildcards). It will
check that the right components are present to create the geography.
"""

from dataclasses import dataclass
from urllib.parse import quote
from d3census.reference import (
    SumLevel,
    SUMLEV_LABELS,
    API_GEO_PARAMS,
    GEOID_DECOMPOSER,
    SUMLEV_FROM_PARTS,
    STRING_NAME_TRANSLATION,
)

from .tablereference import BaseGeography


@dataclass(eq=True)
class Geography(BaseGeography):
    sum_level: SumLevel
    parts: dict


def _create_geography_from_fullgeoid(geoid):
    level_code, geoid = geoid.split("US")
    sum_level = SUMLEV_LABELS[level_code]
    composition = GEOID_DECOMPOSER[sum_level]
    
    parts = {}
    position = 0
    for lev, end in composition.items():
        parts[lev] = geoid[position: position + end]
        position += end

    return Geography(
        sum_level=sum_level,
        parts=parts,
    )


def _create_geography_from_parts(**kwargs):
    try:
        parts = {
            STRING_NAME_TRANSLATION[part_name]: str(part_val)
            for part_name, part_val in kwargs.items()
        }
    
        return Geography(
            sum_level=SUMLEV_FROM_PARTS[tuple(sorted(parts.keys(), key=lambda lev: lev.value))],
            parts = parts
        )

    except KeyError:
        raise ValueError(
            f"The components you provided, {', '.join(kwargs.keys())}, are not "
            "valid geography parts or don't constitute a complete census "
            "geography specification. See "
            "https://www.census.gov/programs-surveys/geography/guidance/geo-identifiers.html"
            " for more information, or check the d3census docs."
        )


def create_geography(geoid=None, **kwargs):
    if geoid and kwargs:
        raise ValueError(
            "You can only provide a geoid or individual components, not both."
        )

    if not (geoid or kwargs):
        raise ValueError(
            "You have to provide either a full geoid or individual geography components."
        )

    if geoid:
        *sum_level, _ = geoid.split("US")

        if not sum_level:
            raise ValueError(
                "'create_geography' only accepts full geoids eg. 05000US26163."
            )
        return _create_geography_from_fullgeoid(geoid)

    return _create_geography_from_parts(**kwargs)


def create_api_call_geo_component(geo: Geography):
    *ins, _for = geo.parts.items()
    
    forstr = f"for={quote(API_GEO_PARAMS[_for[0]])}:{_for[1] if _for[1] else '1'}"

    if not ins:
        return f"{forstr}"

    ingeos = "%20".join(f"{quote(API_GEO_PARAMS[key])}:{val}" for key, val in ins)
    instr = f"in={ingeos}"
    return f"{forstr}&{instr}"


class FullGeography:
    pass

