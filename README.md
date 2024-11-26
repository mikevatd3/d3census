# d3census

A Python library for building custom variables from any year, geography, or data point from the American Community Survey.


## Basic Profile Creation

```python
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


# 'build_profile' outputs the typical pandas dataframe

profile.to_csv("test_profile.csv")
```


## Creating profiles over time


```python
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

years = []
for year in range(2015, 2023): # Remember to add 1 to final year!
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
        create_edition("acs1", year) # Use the 1-year to avoid overlapping survey periods
    )
    
    profile = (
        profile.set_index(join_columns)
        .rename(columns={col: f"{col}_{year}" for col in profile.columns})
    )

    years.append(profile)

result = pd.concat(years, axis=1)

result.to_csv("test_overtime_profile.csv")

```

## When using in a Jupyter notebook

D3Census makes mutiple calls to the Census API asynchronously, which currently breaks when running within a jupyter notebook. The solution currently is to use nest_asyncio.

```
pip install nest_asyncio
```

Then within your notebook before calling any censusified functions add:

```python
import nest_asyncio

nest_asyncio.apply()
```

## Providing your API key

'build_profile' **optionally** accepts your Census API key as a keyword argument (if this ever becomes a problem).

```python
profile = build_profile(
    ...,
    api_key="provide your key here",
)
```
