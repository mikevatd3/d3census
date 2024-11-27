from d3census import (
    create_geography,
    Geography,
    variable,
    create_edition,
    build_profile,
)

from d3census.reference import SumLevel, Individual

from d3census.geography import create_consolodated_api_calls, consolidate_calls


@variable
def total_population(geo: Geography):
    return geo.B01001._001E



def main():
    pass



if __name__ == "__main__":
    main()
