from d3census import variable, create_geography, Geography, Edition


@variable
def some_variable(geo: Geography):
    pass


def main():
    geo = create_geography(state=26, county=163)


if __name__ == "__main__":
    main()
