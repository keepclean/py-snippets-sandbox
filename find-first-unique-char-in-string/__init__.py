import string
import random
import time


def firstUniqChar(s: str) -> int:
    letters = set(s)
    index = [s.index(l) for l in letters if s.count(l) == 1]
    return min(index) if len(index) > 0 else -1


def firstUniqCharV2(s: str) -> int:
    """
    enumerate isn't slow
    the slowness was in setdefault method

    setdefault might be replaced with
    d[x] = d.get(x, 0) + 1
    """
    if not s:
        return -1

    count = dict()
    len_s = len(s)
    # for i, j in enumerate(s):
    n = 0
    for i in s:
        count[i] = n + len_s
        n += 1

    min_j = min(count, key=count.get)
    min_j_index = count[min_j] - len_s

    if min_j_index > len_s:
        return -1

    return min_j_index


def main():
    random.seed(time.time_ns())
    letters = string.ascii_lowercase
    len_letters = len(letters)
    s = "".join(
        letters[random.randint(a=0, b=len_letters - 1)]
        for _ in range(random.randint(a=5000, b=10000))
    )

    print("lenght of string: {}".format(len(s)))

    # TODO learn how to use timeit
    now = time.time()
    firstUniqChar(s=s)
    print("{:.4f}".format(time.time() - now))

    now = time.time()
    firstUniqCharV2(s=s)
    print("{:.4f}".format(time.time() - now))


if __name__ == "__main__":
    main()
