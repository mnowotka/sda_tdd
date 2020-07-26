import collections
import datetime
import random
import requests
import typing
import os

RESULTS_NET_LOCATION = "http://www.mbnet.com.pl/dl.txt"
RESULTS_DISK_LOCATION = os.path.join('.', 'files', 'dl.txt')
LOTTO_NUMBERS = 6
LOTTO_NUMBERS_RANGE = 50
THREE_MONTH_WINDOW = 3 * 4 * 3
DATE_FORMAT = '%d.%m.%Y'


def fetch_results() -> None:
    res = requests.get(RESULTS_NET_LOCATION)
    if not res.ok:
        raise("Error while downloading lotto results from the Internet.")
    open(RESULTS_DISK_LOCATION, 'wb').write(res.content)


def parse_results() -> typing.Generator[typing.Tuple[int, datetime.datetime, typing.FrozenSet[int]], None, None]:
    for line in open(RESULTS_DISK_LOCATION):
        no, date, res = line.split()
        no = int(no[:-1])
        date = datetime.datetime.strptime(date, '%d.%m.%Y')
        res = frozenset(map(int, res.split(',')))
        yield no, date, res


def get_counter(results: typing.List[typing.FrozenSet[int]], window_size: int) -> typing.Counter[int]:
    window = results[-window_size:]
    counter = collections.Counter({key: 0 for key in range(1, LOTTO_NUMBERS_RANGE)})
    for result in window:
        counter.update(result)
    return counter


def get_most_frequent(results: typing.List[typing.FrozenSet[int]], window_size: int, elements: int) -> typing.List[int]:
    return [el for el, _ in get_counter(results, window_size).most_common(elements)]


def get_least_frequent(results: typing.List[typing.FrozenSet[int]], window_size: int, elements: int) -> typing.List[int]:
    return [el for el, _ in get_counter(results, window_size).most_common()][-elements:]


def get_random_sequence(results: typing.List[typing.FrozenSet[int]], elements: int) -> typing.List[int]:
    # random.seed(int("".join(map(str, sorted(results[-1])))))
    results_set = set(results)
    sample = results[-1]
    while sample in results_set:
        sample = frozenset(random.sample(list(range(1, LOTTO_NUMBERS_RANGE)), elements))
    return list(sample)


def get_weighted_random_sequence(results: typing.List[typing.FrozenSet[int]], elements: int) -> typing.List[int]:
    # random.seed(int("".join(map(str, sorted(results[-1])))))
    results_set = set(results)
    frequencies = get_counter(results, len(results)).most_common()
    weights = [weight for _, weight in frequencies]
    numbers = [number for number, _ in frequencies]
    sample = results[-1]
    while sample in results_set:
        sample = set()
        while len(sample) != elements:
            sample.update(list(set(random.choices(numbers, weights, k=elements)))[:elements-len(sample)])
    return list(sample)


def main() -> None:
    # fetch_results()
    results = []
    for no, date, res in parse_results():
        results.append(res)
    all_time_hits = get_most_frequent(results, len(results), LOTTO_NUMBERS)
    three_months_hits = get_most_frequent(results, THREE_MONTH_WINDOW, LOTTO_NUMBERS)
    all_time_misses = get_least_frequent(results, len(results), LOTTO_NUMBERS)
    three_months_misses = get_least_frequent(results, THREE_MONTH_WINDOW, LOTTO_NUMBERS)
    random_choice = get_random_sequence(results, LOTTO_NUMBERS)
    weighted_random_choice = get_weighted_random_sequence(results, LOTTO_NUMBERS)

    print(f'Most popular numbers across the whole history: {sorted(all_time_hits)}')
    print(f'Most popular numbers during last three months: {sorted(three_months_hits)}')
    print(f'Least popular numbers across the whole history: {sorted(all_time_misses)}')
    print(f'Least popular numbers during last three months: {sorted(three_months_misses)}')
    print(f'Random sample of numbers: {sorted(list(random_choice))}')
    print(f'Weighted random sample of numbers: {sorted(list(weighted_random_choice))}')


if __name__ == '__main__':
    main()