"""
The geography module (along with reference.py) is how you define the
geography (or sets of geographies if you're using wildcards). It will
check that the right components are present to create the geography.
"""
from collections import defaultdict
from dataclasses import dataclass
from urllib.parse import quote

from d3census.reference import (
    SumLevel,
    UCG,
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
    ucgid: bool = False

    @property
    def parents(self) -> frozenset[tuple[SumLevel, str]] | SumLevel:
        """
        Parents returns tuples of parent sum_levels and their integer
        values (as strings).
        """
        key = frozenset(
            {
                (key, val)
                for key, val in self.parts.items()
                if key != self.sum_level
            }
        )

        if not key:
            return self.sum_level

        return key

    @property
    def identity(self):
        return self.parts[self.sum_level]


def _create_geography_from_ucid(ucgid):
    *sum_level, _ = ucgid.split("US")
    sum_level = sum_level[0][:3] + "00"
    level = SUMLEV_LABELS[sum_level]

    return Geography(level, {UCG.ID: ucgid}, ucgid=True)


def _create_geography_from_ipums(geoid):
    level_code, geoid = geoid.split("US")
    sum_level = SUMLEV_LABELS[level_code]

    
    if sum_level == SumLevel.NATION:
        return Geography(
            sum_level=SumLevel.NATION,
            parts={SumLevel.NATION: "1"},
        )

    composition = GEOID_DECOMPOSER[sum_level]

    parts = {}
    position = 0
    for lev, end in composition.items():
        parts[lev] =geoid[position : position + end]
        position += end

    return Geography(
        sum_level=sum_level,
        parts=parts,
    )


def _create_geography_from_parts(**kwargs):
    if "nation" in kwargs:
        return Geography(
            sum_level=SumLevel.NATION,
            parts={SumLevel.NATION: "1"},
        )
    try:
        parts = {
            STRING_NAME_TRANSLATION[part_name]: str(part_val)
            for part_name, part_val in kwargs.items()
        }

        return Geography(
            sum_level=SUMLEV_FROM_PARTS[frozenset(parts.keys())],
            parts=parts,
        )

    except KeyError:
        raise ValueError(
            f"The components you provided, {', '.join(kwargs.keys())}, are not "
            "valid geography parts or don't constitute a complete census "
            "geography specification. See "
            "https://www.census.gov/programs-surveys/geography/guidance/geo-identifiers.html"
            " for more information, or check the d3census docs."
        )


def create_geography(geoid=None, ucgid=None, **kwargs):
    if (geoid and kwargs) or (geoid and ucgid) or (ucgid and kwargs):
        raise ValueError(
            "You can only provide a geoid, ucgid, or individual components, not multiple."
        )

    if not (geoid or kwargs or ucgid):
        raise ValueError(
            "You have to provide either a full geoid, ucgid, or individual geography components."
        )

    if geoid:
        *sum_level, _ = geoid.split("US")

        if not sum_level:
            raise ValueError(
                "'create_geography' only accepts full geoids eg. 05000US26163."
            )
        return _create_geography_from_ipums(geoid)

    if ucgid:
        *sum_level, _ = ucgid.split("US")

        if not sum_level:
            raise ValueError(
                "'create_geography' only accepts full ucgids eg. 0500000US26163."
            )
        return _create_geography_from_ucid(ucgid)

    return _create_geography_from_parts(**kwargs)


@dataclass
class CallTree:
    groups: defaultdict


def consolidate_calls(geos: list[Geography]) -> CallTree:
    """
    This takes a list of geographies and organizes them by their parent
    geographies.
    """

    groups = defaultdict(list)

    for geo in geos:
        groups[geo.parents].append(geo)

    return CallTree(groups)


def create_consolodated_api_calls(tree: CallTree):
    """
    This takes the CallTree created by 'consolidate_calls' and returns
    a list of the geography portion of the api calls.
    """

    calls = []
    for parents, children in tree.groups.items():
        child_str = ",".join([child.identity for child in children])

        match parents:
            case SumLevel():
                calls.append(f"for={quote(API_GEO_PARAMS[parents])}:{child_str}")

            case frozenset():
                child_str = ",".join([child.identity for child in children])
                ingeos = "%20".join(
                    f"{quote(API_GEO_PARAMS[key])}:{val}" for key, val in parents
                )

                sumlevel = children[0].sum_level

                for_str = f"for={quote(API_GEO_PARAMS[sumlevel])}:{child_str}"
                in_str = f"in={ingeos}"

                calls.append(f"{for_str}&{in_str}")

            case _:
                raise TypeError(f"{type(parents)} isn't a valid parent type.")

    return calls


def create_api_call_geo_component(geo: Geography):
    *ins, _for = sorted(geo.parts.items(), key=lambda item: item[0].value)

    if geo.ucgid == True:
        return f"ucgid={_for[1]}"

    for_str = f"for={quote(API_GEO_PARAMS[_for[0]])}:{_for[1] if _for[1] else '1'}"

    if not ins:
        return f"{for_str}"

    ingeos = "%20".join(
        f"{quote(API_GEO_PARAMS[key])}:{val}" for key, val in ins
    )
    in_str = f"in={ingeos}"

    return f"{for_str}&{in_str}"


class FullGeography:
    pass
