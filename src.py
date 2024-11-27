import pandas as pd
from d3census import create_geography, Geography, create_edition, variable
from d3census.profile import build_profile


# Mark the Python functions that you'd like to use as variables with the 
# 'variable' decorator.


@variable
def num_children_under_five(geo: Geography): # Type defs help with autocomplete!
    """
    Count of the number of children under five.
    """
    
    # If you're coming from tearsheet you have to follow this variable formatting
    # (along with adding the 'E' for estimate).
    return geo.B01001._003E + geo.B01001._027E


@variable
def pct_under_five_below_poverty(geo: Geography):

    # Python functions like 'sum' are available for use with the acs variables
    # as usual.

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

    # When dividing (especially when using smaller geographies) be
    # sure to catch the 'ZeroDivisionError!'

    except ZeroDivisionError:
        return 0



join_columns = ["geoid", "name"]

profile = build_profile(
    [
        create_geography(state="26", zcta="48202")
    ],
    [
        pct_under_five_below_poverty,
        num_children_under_five,
    ],
    create_edition("acs5", 2012)
)

print(profile)

