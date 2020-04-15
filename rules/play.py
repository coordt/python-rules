from rules import expressions, parser

context1 = {
    "price": {
        "value": 3.45,
        "unit": "USD"
    },
    "name": "foobar inc"
}

context2 = {
    "price": {
        "value": 45.00,
        "unit": "USD"
    },
    "name": "cyanic ltd"
}

expr = {
    "type": "operator",
    "operator": "*",
    "left_side": {
        "type": "context reference",
        "name": "price.value",
        "default": None,
    },
    "right_side": 1.25
}

expr_json = '''{
    "type": "operator",
    "operator": "*",
    "left_side": {
        "type": "context reference",
        "name": "price.value",
        "default": null
    },
    "right_side": 1.25
}'''

func1 = parser.parse(expr)
func2 = parser.parse(expr_json)

assert str(func1) == str(func2) == "price.value * 1.25"
assert func1(context1) == func2(context1) == 4.3125
assert func1(context2) == func2(context2) == 56.25

r = expressions.ContextReference("price.value")
c = expressions.Constant(1.25)
o = expressions.Operator("*", r, c)
assert str(o) == "price.value * 1.25"

assert o(context1) == 4.3125

assert o(context2) == 56.25
