for i in range(210235, 210301):
    divisions = []
    for d in range(2, int(i ** 0.5) + 1):

        if i % d == 0:
            divisions += [d, i // d]

    # print(divisions)
    if len(divisions) == 4:
        print(divisions)
print(210301 ** 0.5)