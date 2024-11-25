import inspect
import textwrap
import ast

from ast import NodeVisitor, Attribute

from .geography import Geography, FullGeography


class GeoVisitor(NodeVisitor):
    def __init__(self) -> None:
        # Give local precidence
        self.target_variables = set()
        super().__init__()

    def visit_Attribute(self, node: Attribute) -> None:
        match node:
            case Attribute(value=Attribute(attr=attr), attr=sub_attr):
                if hasattr(Geography, attr):
                    self.target_variables.add(attr + sub_attr)
            case _:
                return


def write_variable_shopping_list(function) -> set[str]:
    tree = ast.parse(textwrap.dedent(inspect.getsource(function)))
    visitor = GeoVisitor()
    visitor.visit(tree)

    return visitor.target_variables


class DefinedVariable:
    """
    A censusified function can only take a single Geography variable.
    """

    def __init__(self, function):
        shopping_list = write_variable_shopping_list(function)

        if not shopping_list:
            raise ValueError(
                "No Census variables to look up in censusified function."
            )

        self._shopping_list = shopping_list
        self.function = function

    @property
    def shopping_list(self) -> set[str]:
        return self._shopping_list

    def __call__(self, full_geo: FullGeography):
        return self.function(full_geo)


def variable(function):
    return DefinedVariable(function)
