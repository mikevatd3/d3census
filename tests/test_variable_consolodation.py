import pytest
from d3census.geography import Geography, consolidate_calls
from d3census.reference import SumLevel


# Example test data for geography
@pytest.fixture
def sample_geographies():
    return [
        Geography(
            sum_level=SumLevel.COUNTY,
            parts={SumLevel.STATE: "26", SumLevel.COUNTY: "163"},
        ),
        Geography(
            sum_level=SumLevel.COUNTY,
            parts={SumLevel.STATE: "26", SumLevel.COUNTY: "162"},
        ),
        Geography(sum_level=SumLevel.STATE, parts={SumLevel.STATE: "26"}),
        Geography(
            sum_level=SumLevel.TRACT,
            parts={
                SumLevel.STATE: "26",
                SumLevel.COUNTY: "163",
                SumLevel.TRACT: "000500",
            },
        ),
    ]


def test_consolidate_calls_single_parent(sample_geographies):
    # Single parent: Same state (26), different counties
    consolidated = consolidate_calls(sample_geographies)

    assert (
        len(consolidated.groups) == 3
    )  # 3 unique parent sets (STATE-only, STATE+COUNTY)
    assert (
        SumLevel.COUNTY,
        frozenset({(SumLevel.STATE, "26")}),
    ) in consolidated.groups
    assert (
        SumLevel.TRACT,
        frozenset({(SumLevel.STATE, "26"), (SumLevel.COUNTY, "163")}),
    ) in consolidated.groups


def test_consolidate_calls_multiple_parents():
    geos = [
        Geography(
            sum_level=SumLevel.COUNTY,
            parts={SumLevel.STATE: "26", SumLevel.COUNTY: "163"},
        ),
        Geography(
            sum_level=SumLevel.COUNTY,
            parts={SumLevel.STATE: "27", SumLevel.COUNTY: "001"},
        ),
    ]

    consolidated = consolidate_calls(geos)

    # Each geography has a unique parent
    assert len(consolidated.groups) == 2
    assert (
        SumLevel.COUNTY,
        frozenset({(SumLevel.STATE, "26")}),
    ) in consolidated.groups
    assert (
        SumLevel.COUNTY,
        frozenset({(SumLevel.STATE, "27")}),
    ) in consolidated.groups


def test_consolidate_calls_no_parents():
    geos = [Geography(sum_level=SumLevel.NATION, parts={})]
    consolidated = consolidate_calls(geos)

    # "ALONE" parent key
    assert len(consolidated.groups) == 1
    assert (SumLevel.NATION, SumLevel.NATION) in consolidated.groups


def test_consolidate_calls_mixed_hierarchy():
    geos = [
        Geography(
            sum_level=SumLevel.COUNTY,
            parts={SumLevel.STATE: "26", SumLevel.COUNTY: "163"},
        ),
        Geography(
            sum_level=SumLevel.COUNTY_SUBDIVISION,
            parts={
                SumLevel.STATE: "26",
                SumLevel.COUNTY: "163",
                SumLevel.COUNTY_SUBDIVISION: "22000",
            },
        ),
    ]
    consolidated = consolidate_calls(geos)

    # Parent grouping: State + County
    assert len(consolidated.groups) == 2
    assert (
        len(
            consolidated.groups[
                (
                    SumLevel.COUNTY_SUBDIVISION,
                    frozenset(
                        {(SumLevel.STATE, "26"), (SumLevel.COUNTY, "163")}
                    ),
                )
            ]
        )
        == 1
    )
