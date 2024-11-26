import pytest
from d3census import create_geography, Geography
from d3census.reference import UCG, SumLevel


def test_diff_method_same_result():
    assert create_geography("05000US26163") == create_geography(state=26, county=163)

# Test: Valid Full Geoid for State
def test_create_geography_full_geoid_state():
    result = create_geography(geoid="04000US26")
    expected = Geography(sum_level=SumLevel.STATE, parts={SumLevel.STATE: "26"})
    assert result == expected

# Test: Valid Full Geoid for County
def test_create_geography_full_geoid_county():
    result = create_geography(geoid="05000US26163")
    expected = Geography(
        sum_level=SumLevel.COUNTY,
        parts={SumLevel.STATE: "26", SumLevel.COUNTY: "163"}
    )
    assert result == expected

# Test: Valid Full Geoid for Place
def test_create_geography_full_geoid_place():
    result = create_geography(geoid="16000US2616000")
    expected = Geography(
        sum_level=SumLevel.PLACE,
        parts={SumLevel.STATE: "26", SumLevel.PLACE: "16000"}
    )
    assert result == expected

# Test: Valid Components for State
def test_create_geography_parts_state():
    result = create_geography(state="26")
    expected = Geography(sum_level=SumLevel.STATE, parts={SumLevel.STATE: "26"})
    assert result == expected

# Test: Valid Components for County
def test_create_geography_parts_county():
    result = create_geography(state="26", county="163")
    expected = Geography(
        sum_level=SumLevel.COUNTY,
        parts={SumLevel.STATE: "26", SumLevel.COUNTY: "163"}
    )
    assert result == expected

# Test: Valid Components for Place
def test_create_geography_parts_place():
    result = create_geography(state="26", place="16000")
    expected = Geography(
        sum_level=SumLevel.PLACE,
        parts={SumLevel.STATE: "26", SumLevel.PLACE: "16000"}
    )
    assert result == expected

# Test: Mixed Inputs (Geoid and Parts)
def test_create_geography_mixed_inputs():
    with pytest.raises(ValueError, match="You can only provide a geoid, ucgid, or individual components, not multiple."):
        create_geography(geoid="04000US26", state="26")

# Test: Missing Both Geoid and Parts
def test_create_geography_missing_inputs():
    with pytest.raises(ValueError, match="You have to provide either a full geoid, ucgid, or individual geography components."):
        create_geography()

# Test: Invalid Geoid Format
def test_create_geography_invalid_geoid_format():
    with pytest.raises(ValueError, match="'create_geography' only accepts full geoids eg. 05000US26163."):
        create_geography(geoid="05000")

# Test: Invalid Parts
def test_create_geography_invalid_parts():
    with pytest.raises(ValueError, match="The components you provided, invalid, are not valid geography parts"):
        create_geography(invalid="123")

# Test: Valid Full Geoid for Tract
def test_create_geography_full_geoid_tract():
    result = create_geography(geoid="14000US26163521400")
    expected = Geography(
        sum_level=SumLevel.TRACT,
        parts={SumLevel.STATE: "26", SumLevel.COUNTY: "163", SumLevel.TRACT: "521400"}
    )
    assert result == expected

# Test: Valid Full Geoid for Block Group
def test_create_geography_full_geoid_block_group():
    result = create_geography(geoid="15000US261635214001")
    expected = Geography(
        sum_level=SumLevel.BLOCK_GROUP,
        parts={
            SumLevel.STATE: "26",
            SumLevel.COUNTY: "163",
            SumLevel.TRACT: "521400",
            SumLevel.BLOCK_GROUP: "1"
        }
    )
    assert result == expected

# Test: Valid Components for Tract
def test_create_geography_parts_tract():
    result = create_geography(state="26", county="163", tract="521400")
    expected = Geography(
        sum_level=SumLevel.TRACT,
        parts={SumLevel.STATE: "26", SumLevel.COUNTY: "163", SumLevel.TRACT: "521400"}
    )
    assert result == expected

# Test: Valid Components for Block Group
def test_create_geography_parts_block_group():
    result = create_geography(state="26", county="163", tract="521400", block_group="1")
    expected = Geography(
        sum_level=SumLevel.BLOCK_GROUP,
        parts={
            SumLevel.STATE: "26",
            SumLevel.COUNTY: "163",
            SumLevel.TRACT: "521400",
            SumLevel.BLOCK_GROUP: "1"
        }
    )
    assert result == expected

# Test: Valid Full Geoid for Elementary School District
def test_create_geography_full_geoid_elem_school_district():
    result = create_geography(geoid="95000US12345")
    expected = Geography(
        sum_level=SumLevel.ELEM_SCH_DISTRICT,
        parts={SumLevel.STATE: "12", SumLevel.ELEM_SCH_DISTRICT: "345"}
    )
    assert result == expected

# Test: Valid Components for Elementary School District
def test_create_geography_parts_elem_school_district():
    result = create_geography(state="12", elem_sch_district="345")
    expected = Geography(
        sum_level=SumLevel.ELEM_SCH_DISTRICT,
        parts={SumLevel.STATE: "12", SumLevel.ELEM_SCH_DISTRICT: "345"}
    )
    assert result == expected

# Test: Valid Full Geoid for Unified School District
def test_create_geography_full_geoid_uni_school_district():
    result = create_geography(geoid="97000US12345")
    expected = Geography(
        sum_level=SumLevel.UNI_SCH_DISTRICT,
        parts={SumLevel.STATE: "12", SumLevel.UNI_SCH_DISTRICT: "345"}
    )
    assert result == expected

# Test: Valid Components for Unified School District
def test_create_geography_parts_uni_school_district():
    result = create_geography(state="12", uni_sch_district="345")
    expected = Geography(
        sum_level=SumLevel.UNI_SCH_DISTRICT,
        parts={SumLevel.STATE: "12", SumLevel.UNI_SCH_DISTRICT: "345"}
    )
    assert result == expected

# Test: Valid Full Geoid for Secondary School District
def test_create_geography_full_geoid_sec_school_district():
    result = create_geography(geoid="96000US12345")
    expected = Geography(
        sum_level=SumLevel.SEC_SCH_DISTRICT,
        parts={SumLevel.STATE: "12", SumLevel.SEC_SCH_DISTRICT: "345"}
    )
    assert result == expected

# Test: Valid Components for Secondary School District
def test_create_geography_parts_sec_school_district():
    result = create_geography(state="12", sec_sch_district="345")
    expected = Geography(
        sum_level=SumLevel.SEC_SCH_DISTRICT,
        parts={SumLevel.STATE: "12", SumLevel.SEC_SCH_DISTRICT: "345"}
    )
    assert result == expected

# Test: Valid Components for Secondary School District
def test_create_geography_parts_ucgid():
    result = create_geography(ucgid="860Z200US15007")
    expected = Geography(
        sum_level=SumLevel.ZCTA,
        parts={UCG.ID: "860Z200US15007"},
        ucgid=True
    )
    assert result == expected
