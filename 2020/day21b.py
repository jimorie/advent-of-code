import day21a


def find_allergen_ingredients():
    _, allergen_sources = day21a.read_fooditems()
    certain = {}
    while len(certain) < len(allergen_sources):
        for allergen, ingredients in allergen_sources.items():
            possible = ingredients.difference(certain.values())
            if len(possible) == 1:
                ingredient = possible.pop()
                certain[allergen] = ingredient
                break
        else:
            raise RuntimeError("Failed to eliminate ingredient")
        for ingredients in allergen_sources.values():
            if ingredient in ingredients:
                ingredients.remove(ingredient)
    return certain


def find_allergens():
    certain = find_allergen_ingredients()
    return ",".join(ingredient for _, ingredient in sorted(certain.items()))


if __name__ == "__main__":
    print(find_allergens())
