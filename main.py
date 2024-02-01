"""Test task for IS-wireless"""

import sys
import re
import tracemalloc


FILE_PATH = sys.argv[1]
COLORS = ("red", "green", "blue", "magenta")
TIME_PATTERN = r"^\d\d:\d\d:\d\d$"


def memory_usage(func):
    """custom decorator. Checks current and peak memory usage in Bytes"""

    def wrapper(*args, **kwargs):
        tracemalloc.start()
        func(*args, **kwargs)
        current, peak = tracemalloc.get_traced_memory()
        print(f"\n===========================\n"
              f"current memory usage: {current}\npeak memory usage: {peak}")
        tracemalloc.stop()

    return wrapper


def parse_line(line: str) -> tuple:
    """
    parse input str into tuple of values <seconds>, (<color>, <integer value>),
    return empty tuple if condition is not satisfied
    """

    str_parts = line.split()
    seconds = str_parts[0].split(".")[0]
    color = str_parts[1]
    error = ("useless", "error"), 1

    is_color__first_word = color in COLORS

    if is_color__first_word:
        try:
            integer = int(str_parts[2])
            return (seconds, color), integer
        except (ValueError, IndexError):
            return error

    else:
        return tuple()


def count_values(counter: dict, parsed_line: tuple) -> dict:
    """custom counter implementation, return dict with <key> and <counted value>"""

    value = parsed_line[1]

    for key in parsed_line[0]:
        if key in counter:
            counter[key] += value
        else:
            counter[key] = value

    return counter


def get_highest_second(counter: dict) -> tuple:
    """find second with the highest value and return tuple(<second>, <value>)"""

    seconds = {key: value for key, value in counter.items() if re.fullmatch(TIME_PATTERN, key)}
    highest_second, highest_value = max(seconds.items(), key=lambda item: item[1])

    return highest_second, highest_value


def print_results(counter: dict) -> None:
    """
    print results in format:
    Sum for red: <value>
    Sum for green: <value>
    Sum for blue: <value>
    Errors: <value>
    Highest value second is <second> with sum of <value>
    """

    highest_second, highest_value = get_highest_second(counter)
    magenta_value = counter.get("magenta", 0)

    for key in COLORS:
        color_value = counter.get(key, 0) + magenta_value if key != "green" else counter.get(key, 0)
        if key != "magenta":
            print(f"Sum for {key}: {color_value}")

    print(f"Errors: {counter.get("error", 0)}")
    print(f"Highest value second is {highest_second} with sum of {highest_value}")


@memory_usage
def main() -> None:
    """parse a log file and print summary"""

    line = True
    counter = {}

    with open(FILE_PATH, encoding="UTF-8") as log_file:
        while line:
            line = log_file.readline()
            if line:
                parsed_line = parse_line(line)

                if parsed_line:
                    counter = count_values(counter, parsed_line)

    print_results(counter)


if __name__ == '__main__':
    if len(sys.argv) == 1:
        print("NO FILEPATH FOUND: please pass filepath as argument")
    else:
        main()
