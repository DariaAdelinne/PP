import itertools

houses = [1, 2, 3, 4, 5]

colors = ['red', 'green', 'white', 'yellow', 'blue']
nationalities = ['Brit', 'Swede', 'Dane', 'Norwegian', 'German']
drinks = ['tea', 'coffee', 'milk', 'beer', 'water']
cigarettes = ['Pall Mall', 'Dunhill', 'Blend', 'Camel', 'Marlborough']
pets = ['dog', 'birds', 'cats', 'horse', 'fish']

for color_perm in itertools.permutations(colors):
    if nationalities[color_perm.index('red')] != 'Brit':
        continue

    idx_green = color_perm.index('green')
    idx_white = color_perm.index('white')
    if idx_green + 1 != idx_white:
        continue

    for nat_perm in itertools.permutations(nationalities):
        if nat_perm[0] != 'Norwegian':
            continue

        idx_nor = nat_perm.index('Norwegian')
        if not (idx_nor > 0 and color_perm[idx_nor - 1] == 'blue') and not (idx_nor < 4 and color_perm[idx_nor + 1] == 'blue'):
            continue

        for drink_perm in itertools.permutations(drinks):
            if drink_perm[nat_perm.index('Dane')] != 'tea':
                continue

            if drink_perm[color_perm.index('green')] != 'coffee':
                continue

            if drink_perm[2] != 'milk':
                continue

            for cig_perm in itertools.permutations(cigarettes):
                if cig_perm[color_perm.index('yellow')] != 'Dunhill':
                    continue

                if drink_perm[cig_perm.index('Camel')] != 'beer':
                    continue

                if cig_perm[nat_perm.index('German')] != 'Marlborough':
                    continue

                for pet_perm in itertools.permutations(pets):
                    if pet_perm[nat_perm.index('Swede')] != 'dog':
                        continue

                    if pet_perm[cig_perm.index('Pall Mall')] != 'birds':
                        continue

                    idx_blend = cig_perm.index('Blend')
                    if not ((idx_blend > 0 and pet_perm[idx_blend - 1] == 'cats') or (idx_blend < 4 and pet_perm[idx_blend + 1] == 'cats')):
                        continue

                    idx_dun = cig_perm.index('Dunhill')
                    if not ((idx_dun > 0 and pet_perm[idx_dun - 1] == 'horse') or (idx_dun < 4 and pet_perm[idx_dun + 1] == 'horse')):
                        continue

                    if not ((idx_blend > 0 and drink_perm[idx_blend - 1] == 'water') or (idx_blend < 4 and drink_perm[idx_blend + 1] == 'water')):
                        continue

                    fish_owner = nat_perm[pet_perm.index('fish')]
                    print(f"The person who keeps the fish is: {fish_owner}")
                    raise SystemExit
