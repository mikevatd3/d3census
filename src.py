from d3census import (
    variable,
    create_geography,
    create_edition,
    Geography,
)
from d3census.profile import build_profile


@variable
def some_variable(geo: Geography):
    return geo.B01001._001E


@variable
def another_variable(geo: Geography):
    return geo.B01001._002E


def main():
    edition = create_edition("acs5", 2022)

    profile = build_profile(
        [
            create_geography(state="26", county="163", tract="*"),
        ],
        [some_variable, another_variable],
        edition,
    )

    profile.to_csv("test_profile.csv")


if __name__ == "__main__":
    main()
