try:
    import pandas as pd
except ImportError:
    raise ImportError("To use the profile module you must install pandas.")

from .censusify import (
    CensusifiedFunc,
    Geography,
    Edition,
    join_subshoppinglists,
    look_up,
)


def prep_cens_func(indicator):
    indicator.__name__ = indicator.__qualname__.replace(".", "")
    return CensusifiedFunc(indicator)


def build_profile(
    geographies: list[Geography],
    indicators: list[CensusifiedFunc],
    edition: Edition,
    suffix: str = "",
):
    censusified_funcs = [
        indicator if isinstance(indicator, CensusifiedFunc) else prep_cens_func(indicator)
        for indicator in indicators
    ]
    
    shopping_list = {"NAME"} | join_subshoppinglists(censusified_funcs)
    namespace = look_up(geographies, shopping_list, edition.filled_base_url)

    return pd.DataFrame(
        [
            [geo.geoid, geo.name]
            + [
                indicator.function(full_geo) 
                for indicator in censusified_funcs
            ]
            for geo, full_geo in namespace.items()
        ],
        columns=["geoid", "name"]
        + [
            indicator.function.__name__ + suffix 
            for indicator in censusified_funcs
        ],
    )
