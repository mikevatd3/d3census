"""
There is a lot of futzing with the census geographies to request
exactly the data you want. This file provides a bunch of translations
to get from one representation to another for summary levels.
"""

from enum import Enum, auto


class SumLevel(Enum):
    """
    SumLevel is the default way to ID which geo type is in play
    around the library. Other representations are allowed only
    at the end-user interface: the 'create_geography' function call,
    and the final call out to the census api where you have to use
    their (surprisingly complicated) strings.
    """

    STATE = auto()
    CONGRESSIONAL_DISTRICT = auto()
    STATE_LEG_LOWER = auto()
    STATE_LEG_UPPER = auto()
    COUNTY = auto()
    ZCTA = auto()
    COUNTY_SUBDIVISION = auto()
    PLACE = auto()
    TRACT = auto()
    BLOCK_GROUP = auto()
    ELEM_SCH_DISTRICT = auto()
    SEC_SCH_DISTRICT = auto()
    UNI_SCH_DISTRICT = auto()


# translate the 'part' to the enum

STRING_NAME_TRANSLATION = {
    "state": SumLevel.STATE,
    "congressional_district": SumLevel.CONGRESSIONAL_DISTRICT,
    "state_leg_lower": SumLevel.STATE_LEG_LOWER,
    "state_leg_upper": SumLevel.STATE_LEG_UPPER,
    "county": SumLevel.COUNTY,
    "zcta": SumLevel.ZCTA,
    "county_subdivision": SumLevel.COUNTY_SUBDIVISION,
    "place": SumLevel.PLACE,
    "tract": SumLevel.TRACT,
    "block_group": SumLevel.BLOCK_GROUP,
    "elem_sch_district": SumLevel.ELEM_SCH_DISTRICT,
    "sec_sch_district": SumLevel.SEC_SCH_DISTRICT,
    "uni_sch_district": SumLevel.UNI_SCH_DISTRICT,
}

# use the IPUMS sumlev representation to get to the enum

SUMLEV_LABELS = {
    "04000": SumLevel.STATE,
    "50000": SumLevel.CONGRESSIONAL_DISTRICT,
    "05000": SumLevel.COUNTY,
    "86000": SumLevel.ZCTA,
    "62000": SumLevel.STATE_LEG_LOWER,
    "61000": SumLevel.STATE_LEG_UPPER,
    "06000": SumLevel.COUNTY_SUBDIVISION,
    "16000": SumLevel.PLACE,
    "14000": SumLevel.TRACT,
    "15000": SumLevel.BLOCK_GROUP,
    "95000": SumLevel.ELEM_SCH_DISTRICT,
    "96000": SumLevel.SEC_SCH_DISTRICT,
    "97000": SumLevel.UNI_SCH_DISTRICT,
}

# For building the final call to the census API

API_GEO_PARAMS = {
    SumLevel.STATE: "state",
    SumLevel.CONGRESSIONAL_DISTRICT: "congressional district",
    SumLevel.COUNTY: "county",
    SumLevel.ZCTA: "zcta",
    SumLevel.STATE_LEG_LOWER: "state legislative district (upper chamber)",
    SumLevel.STATE_LEG_UPPER: "state legislative district (lower chamber)",
    SumLevel.COUNTY_SUBDIVISION: "county subdivision",
    SumLevel.PLACE: "place",
    SumLevel.TRACT: "tract",
    SumLevel.BLOCK_GROUP: "block group",
    SumLevel.ELEM_SCH_DISTRICT: "school district (elementary)",  # These can't be created through this builder.
    SumLevel.SEC_SCH_DISTRICT: "school district (secondary)",
    SumLevel.UNI_SCH_DISTRICT: "school district (unified)",
}


# This shows which part consumes how many digits on a geoid

GEOID_DECOMPOSER = {
    SumLevel.STATE: {SumLevel.STATE: 2},
    SumLevel.COUNTY: {SumLevel.STATE: 2, SumLevel.COUNTY: 3},
    SumLevel.CONGRESSIONAL_DISTRICT: {
        SumLevel.STATE: 2,
        SumLevel.CONGRESSIONAL_DISTRICT: 2,
    },
    SumLevel.ZCTA: {SumLevel.ZCTA: 5},
    SumLevel.STATE_LEG_LOWER: {SumLevel.STATE: 2, SumLevel.STATE_LEG_LOWER: 3},
    SumLevel.STATE_LEG_UPPER: {SumLevel.STATE: 2, SumLevel.STATE_LEG_UPPER: 3},
    SumLevel.COUNTY_SUBDIVISION: {
        SumLevel.STATE: 2,
        SumLevel.COUNTY: 3,
        SumLevel.COUNTY_SUBDIVISION: 5,
    },
    SumLevel.PLACE: {SumLevel.STATE: 2, SumLevel.PLACE: 5},
    SumLevel.TRACT: {SumLevel.STATE: 2, SumLevel.COUNTY: 3, SumLevel.TRACT: 6},
    SumLevel.BLOCK_GROUP: {
        SumLevel.STATE: 2,
        SumLevel.COUNTY: 3,
        SumLevel.TRACT: 6,
        SumLevel.BLOCK_GROUP: 1,
    },
    SumLevel.ELEM_SCH_DISTRICT: {
        SumLevel.STATE: 2,
        SumLevel.ELEM_SCH_DISTRICT: 5,
    },
    SumLevel.SEC_SCH_DISTRICT: {
        SumLevel.STATE: 2,
        SumLevel.SEC_SCH_DISTRICT: 5,
    },
    SumLevel.UNI_SCH_DISTRICT: {
        SumLevel.STATE: 2,
        SumLevel.UNI_SCH_DISTRICT: 5,
    },
}


# If you only know which parts are present, this gets you back to
# which geoid is being built.

SUMLEV_FROM_PARTS = {
    tuple(sorted(parts.keys(), key=lambda lev: lev.value)): lev
    for lev, parts in GEOID_DECOMPOSER.items()
}
