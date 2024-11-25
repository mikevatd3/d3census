import pytest
from d3census import create_edition 
from d3census.edition import ACSEra, InvalidACSEraError, InvalidACSYearError


def test_valid_edition_one_year():
    """Test creating a valid ACSEdition for ONE_YEAR era."""
    edition = create_edition("acs1", 2020)
    assert edition.era == ACSEra.ONE_YEAR
    assert edition.year == 2020


def test_valid_edition_three_year():
    """Test creating a valid ACSEdition for THREE_YEAR era."""
    edition = create_edition("acs3", 2013)
    assert edition.era == ACSEra.THREE_YEAR
    assert edition.year == 2013


def test_valid_edition_five_year():
    """Test creating a valid ACSEdition for FIVE_YEAR era."""
    edition = create_edition("acs5", 2015)
    assert edition.era == ACSEra.FIVE_YEAR
    assert edition.year == 2015


def test_invalid_era_key():
    """Test that an invalid era key raises InvalidACSEraError."""
    with pytest.raises(InvalidACSEraError) as excinfo:
        create_edition("acs2", 2020)
    assert "Invalid era key: 'acs2'" in str(excinfo.value)


def test_invalid_year_one_year():
    """Test that an invalid year for ONE_YEAR era raises InvalidACSYearError."""
    with pytest.raises(InvalidACSYearError) as excinfo:
        create_edition("acs1", 2004)  # Year before the valid range
    assert "Invalid year: 2004 for era 'ONE_YEAR'" in str(excinfo.value)


def test_invalid_year_three_year():
    """Test that an invalid year for THREE_YEAR era raises InvalidACSYearError."""
    with pytest.raises(InvalidACSYearError) as excinfo:
        create_edition("acs3", 2015)  # Year after the valid range
    assert "Invalid year: 2015 for era 'THREE_YEAR'" in str(excinfo.value)


def test_invalid_year_five_year():
    """Test that an invalid year for FIVE_YEAR era raises InvalidACSYearError."""
    with pytest.raises(InvalidACSYearError) as excinfo:
        create_edition("acs5", 2008)  # Year before the valid range
    assert "Invalid year: 2008 for era 'FIVE_YEAR'" in str(excinfo.value)
