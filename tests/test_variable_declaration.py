from d3census import variable, Geography


def test_variable_declaration():

    def total_population(geo: Geography):
        return geo.B01001._001E

    func = variable(total_population)

    print(func.shopping_list)

    assert func.shopping_list == {'B01001_001E'}


def test_nested_vars():

    def total_population(geo: Geography):
        return sum([
            geo.B01001._001E,
            geo.B01001._027E,
        ])

    func = variable(total_population)

    assert func.shopping_list == {'B01001_001E', 'B01001_027E'}

