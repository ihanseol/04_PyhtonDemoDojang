length = 63

nquo, remainder = divmod(length, 25)
print(nquo, remainder)
print("-" * 80)


def loop25(n):
    for i in range((n - 1) * 25 + 1, n * 25 + 1):
        print(i)


def loop_rest(start, remainder):
    for i in range((start * 25) + 1, (start * 25) + remainder + 1):
        print(i)


# -------------------------------------------------------------------------------------

for i in range(1, nquo + 1):
    loop25(i)
    print("-" * 80)

loop_rest(nquo, remainder)


