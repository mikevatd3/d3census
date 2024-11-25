from dataclasses import dataclass
from d3census.reference import ACSEra, ERA_MAPPINGS, VALID_YEARS_BY_ERA


@dataclass
class ACSEdition:
    era: ACSEra
    year: int


class InvalidACSEraError(Exception):
    """Raised when an invalid ACS era is specified."""
    pass


class InvalidACSYearError(Exception):
    """Raised when a year is invalid for the specified ACS era."""
    pass


def create_edition(era_key: str, year: int) -> ACSEdition:
    """
    Creates an ACSEdition instance based on the specified era and year.

    Args:
        era_key (str): The ACS era key (e.g., "acs1", "acs3", "acs5").
        year (int): The year of the data.

    Returns:
        ACSEdition: The created ACSEdition instance.

    Raises:
        InvalidACSEraError: If the specified era key is invalid.
        InvalidACSYearError: If the year is not valid for the specified era.
    """
    if era_key not in ERA_MAPPINGS:
        raise InvalidACSEraError(f"Invalid era key: '{era_key}'. Must be one of {list(ERA_MAPPINGS.keys())}.")

    era = ERA_MAPPINGS[era_key]

    if year not in VALID_YEARS_BY_ERA[era]:
        valid_range = VALID_YEARS_BY_ERA[era]
        raise InvalidACSYearError(
            f"Invalid year: {year} for era '{era.name}'. "
            f"Valid years are {valid_range.start}-{valid_range.stop - 1}."
        )

    return ACSEdition(era, year)
