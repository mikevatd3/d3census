import pytest
from d3census import (
    create_geography,
    create_edition,
    build_profile,
    variable,
    Geography,
)
from d3census.profile import APIParameterMismatchError


def test_zip_pre_2020():
    @variable
    def total_population(geo: Geography):
        return geo.B01001._001E
    
    with pytest.raises(
        APIParameterMismatchError,
        match="When requesting ZCTAs before 2020, you must provide a state."
    ):
        _ = build_profile(
            [create_geography(zcta="40202")],
            [total_population],
            create_edition("acs5", 2017),
        )
