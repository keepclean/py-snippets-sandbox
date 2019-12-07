#!/usr/bin/env python

import string


def main():
    l = string.ascii_letters
    len_l = len(l)
    columns, reminder = divmod(len_l, 10)
    for r in range(10):
        s = list()
        for c in range(columns):
            index = c * 10 + r
            s.append("{:>2}) {}".format(index + 1, l[index]))

        if reminder > 0:
            s.append("{:>2}) {}".format(len_l - reminder + 1, l[-reminder]))
            reminder -= 1

        print(" ".join(s))


if __name__ == "__main__":
    main()
