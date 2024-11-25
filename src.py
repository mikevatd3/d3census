from d3census import create_geography, Geography, create_edition, variable
from d3census.profile import build_profile


@variable
def num_children_under_five(geo: Geography):
    """
    Count of the number of children under five.
    """
    return geo.B01001._003E + geo.B01001._027E


@variable
def pct_under_five_below_poverty(geo: Geography):
    """
    When dividing and using geographies that could have 0 in the 
    denominator, (like tracts) you have to catch the ZeroDivisionError!
    """
    try:
        return sum([
            geo.B17001._004E,
            geo.B17001._018E,
        ]) / sum([
            geo.B17001._004E,
            geo.B17001._018E,
            geo.B17001._033E,
            geo.B17001._047E,
        ])

    except ZeroDivisionError:
        return 0


profile = build_profile(
    [
        create_geography(geoid="01000US"), # US overall
        # create_geography(nation="1"), # Another way to show US overall
        create_geography(geoid="04000US26"),
        create_geography(state="26", county="163", tract="*")
    ],
    [
        pct_under_five_below_poverty,
        num_children_under_five,
    ],
    create_edition("acs5", 2016)
)

profile.to_csv("test_profile.csv")
