import sys

if __name__ == '__main__':
    i = 0
    while True:
        i += 1
        assert i < 3, "Za duża liczba"
        print(f'i = {i}, idę dalej', file=sys.stderr, flush=True)
