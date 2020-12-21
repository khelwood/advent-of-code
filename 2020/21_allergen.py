#!/usr/bin/env python3

"""
Each allergen is found in exactly one ingredient. Each ingredient contains zero or one allergen.
"""

import sys
from collections import namedtuple

Product = namedtuple('Product', 'items allergens')

def parse_product(line):
    line = line.strip()
    if line[-1]==')':
        line,_,allergens = line.partition('(')
        assert allergens.startswith('contains ')
        allergens = set(allergens[9:-1].strip().split(', '))
    else:
        allergens = set()
    items = set(line.strip().split())
    return Product(items, allergens)

def find_allergen_candidates(products):
    allergens = {}
    for product in products:
        for allergen in product.allergens:
            if allergen not in allergens:
                allergens[allergen] = set(product.items)
            else:
                allergens[allergen] &= set(product.items)
    return allergens

def reverse_multidict(d):
    r = {}
    for k,vs in d.items():
        for v in vs:
            if v in r:
                r[v].add(k)
            else:
                r[v] = {k}
    return r

def refine(candidates, found):
    for k,vs in candidates.items():
        if k in found:
            continue
        if len(vs)==1:
            v, = vs
            found[k] = v
            for k2,vs2 in candidates.items():
                if k2!=k:
                    vs2.discard(v)
            return True
    rev = reverse_multidict(candidates)
    rev_found = {v:k for (k,v) in found.items()}
    for v,ks in rev.items():
        if v in rev_found:
            continue
        if len(ks)==1:
            k, = ks
            found[k] = v
            rev_found[v] = k
            for k2,vs2 in candidates.items():
                if k2!=k:
                    vs2.dicard(v)
            return True
    return False

def isolate_allergens(candidates):
    found = {}
    while refine(candidates, found):
        pass
    assert len(candidates)==len(found)
    return found


def main():
    products = list(map(parse_product, sys.stdin))
    allergen_candidates = find_allergen_candidates(products)
    suspect_items = set.union(*allergen_candidates.values())
    safe_items = {item for pr in products for item in pr.items
                    if item not in suspect_items}
    print("Occurrences of safe items:",
          sum(item in safe_items for pr in products for item in pr.items))
    found = isolate_allergens(allergen_candidates)
    print("Allergen ingredients:", found)
    danger = ','.join(found[a] for a in sorted(found))
    print("Dangerous allergens list:",danger)

if __name__ == '__main__':
    main()
