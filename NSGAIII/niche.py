from __future__ import division


def niche_counting(count, population):
    niche_count = [0 for _ in xrange(count)]
    for individual in population:
        niche_count[individual.closest_ref] += 1
    return niche_count

def niching(k, no_ref_points, population, last_level):
    blah = len(population)
    new_population = []
    remove_candidates = []
    while len(population) < blah + k:
        # print "Len of population: ", len(population)
        # print "no_ref_points: ", no_ref_points

        niche_count = [(i, count) for i, count in enumerate(niche_counting(no_ref_points, population))]
        # print "Niche Count: ", niche_count

        for i in remove_candidates:
            niche_count[i] = (i, 1e32)
        count_last_level = niche_counting(no_ref_points, last_level)
        candidate = sorted(niche_count, key=lambda x: x[1])[0]
        if count_last_level[candidate[0]] == 0:
            # print "remove ref ", candidate
            remove_candidates.append(candidate[0])
        else:
            population.append([can for can in last_level if can.closest_ref == candidate[0]][0])
            # print "Found ref"

    return population


