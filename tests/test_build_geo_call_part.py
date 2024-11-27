import pytest
from d3census.reference import UCG, SumLevel
from d3census.geography import Geography, create_api_call_geo_component


@pytest.mark.parametrize(
    "geography, expected_string",
    [
        # Test case 1: State-level geography
        (
            Geography(sum_level=SumLevel.STATE, parts={SumLevel.STATE: "26"}),
            "for=state:26",
        ),
        # Test case 2: County-level geography
        (
            Geography(
                sum_level=SumLevel.COUNTY,
                parts={SumLevel.STATE: "26", SumLevel.COUNTY: "163"},
            ),
            "for=county:163&in=state:26",
        ),
        # Test case 3: County subdivision geography
        (
            Geography(
                sum_level=SumLevel.COUNTY_SUBDIVISION,
                parts={
                    SumLevel.STATE: "26",
                    SumLevel.COUNTY: "163",
                    SumLevel.COUNTY_SUBDIVISION: "22000",
                },
            ),
            "for=county%20subdivision:22000&in=state:26%20county:163",
        ),
        # Test case 4: Tract-level geography
        (
            Geography(
                sum_level=SumLevel.TRACT,
                parts={
                    SumLevel.STATE: "26",
                    SumLevel.COUNTY: "163",
                    SumLevel.TRACT: "000500",
                },
            ),
            "for=tract:000500&in=state:26%20county:163",
        ),
        (
            Geography(
                sum_level=SumLevel.ZCTA,
                parts={UCG.ID: "860Z200US15007"},
                ucgid=True
            ),
            "ucgid=860Z200US15007",
        ),
        (
            Geography(
                sum_level=SumLevel.ZCTA,
                parts={SumLevel.STATE: "26", SumLevel.ZCTA: "48202"},
            ),
            "for=zip%20code%20tabulation%20area:48202&in=state:26",
        ),
    ],
)
def test_geography_to_api_string(geography, expected_string):
    # Verify correct geography portion of API call string
    result = create_api_call_geo_component(geography)
    assert result == expected_string
