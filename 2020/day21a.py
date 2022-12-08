import collections
import itertools
import util


def parse_food(line):
    ingredients, allergens = line.split(" (contains ")
    return (ingredients.split(), allergens.strip(")").split(", "))


def read_fooditems():
    ingredients_counter = collections.Counter()
    allergen_sources = {}
    for line in util.readlines():
        ingredients, allergens = parse_food(line)
        for allergen in allergens:
            if allergen in allergen_sources:
                allergen_sources[allergen].intersection_update(ingredients)
            else:
                allergen_sources[allergen] = set(ingredients)
        ingredients_counter.update(ingredients)
    return ingredients_counter, allergen_sources


def find_safe_ingredient_count():
    ingredients_counter, allergen_sources = read_fooditems()
    for ingredient in itertools.chain.from_iterable(allergen_sources.values()):
        ingredients_counter.pop(ingredient, None)
    return sum(ingredients_counter.values())


if __name__ == "__main__":
    print(find_safe_ingredient_count())
