from util.pulp import *

def run():
    elements = [1,2,3,4,5,6,7,8,9]
    sets = [[1, 2],[1, 3, 6],[2, 4, 6, 8],[3, 4, 9],[1, 9],[1, 4],[5, 7]]

    print(elements)
    print(sets)
    print("so far so good\n")

    set_element_tuples = []

    for e in elements:
        index = 0
        for set in sets:
            if e in set:
                se = [e,index,setCost(set)]
                set_element_tuples.append(tuple(se))
            index += 1
    print(set_element_tuples)


    x = pulp.LpVariable.dicts('set', set_element_tuples, lowBound=0, upBound=1)

    setCover_model = pulp.LpProblem("set cover model", pulp.LpMinimize)

    setCover_model += sum(se[2]*x[se] for se in set_element_tuples)

    setCover_model.solve()

    for se in set_element_tuples:
        if x[se].value() == 1.0:
            print se


def setCost(set):
    return sum(element for element in set)

run()
