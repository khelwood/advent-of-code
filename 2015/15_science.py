#!/usr/bin/env python3

import sys

from collections import namedtuple

Ingredient = namedtuple('Ingredient', 'name properties')

GOOD_PROPS = tuple('capacity durability flavor texture'.split())

def read_ingredient(line):
    name, props = map(str.strip, line.split(':'))
    props = { k:int(v) for (k,v) in map(str.split, props.split(', ')) }
    return Ingredient(name, props)

def score_recipe(recipe):
    scores = [0]*len(GOOD_PROPS)
    for ing, num in recipe:
        for i,prop in enumerate(GOOD_PROPS):
            scores[i] += ing.properties[prop]*num
    product = 1
    for score in scores:
        product *= max(score, 0)
    return product

def totallers(num, total):
    if total==0:
        yield [0]*num
        return
    if num==1:
        yield [total]
        return
    for i in range(total+1):
        for rest in totallers(num-1, total-i):
            yield [i]+rest

def calorie_count(recipe):
    score = 0
    for ing, num in recipe:
        score += ing.properties['calories']*num
    return max(0, score)

def iter_recipes(ingredients, total):
    for amounts in totallers(len(ingredients), total):
        yield list(zip(ingredients, amounts))

def main():
    lines = sys.stdin.read().strip().split('\n')
    ingredients = [read_ingredient(line) for line in lines]
    total_amount = 100
    best_score = max(map(score_recipe, iter_recipes(ingredients, total_amount)))
    print("Best score:", best_score)
    calories = 500
    best_score = max(map(score_recipe,
                        (rec for rec in iter_recipes(ingredients, total_amount)
                         if calorie_count(rec)==calories)))
    print("Best score with %s calories: %s"%(calories,best_score))

if __name__ == '__main__':
    main()
