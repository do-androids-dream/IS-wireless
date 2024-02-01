import datetime
import random
import sys


def generate_example_input_data(fname: str, size: int) -> None:
    maxbytes = size * 1024 * 1024
    totaldata = 0
    lines = []
    start = datetime.datetime.now()
    for i in range(10**10):
        now = start + datetime.timedelta(milliseconds=100 * i)
        timestamp = now.strftime("%H:%M:%S.%f")
        if random.randint(0, 2):
            lines.append(f"{timestamp} useless line")
        else:
            word = random.choice((" red ", " green ", " blue ", " magenta "))
            line = timestamp + word
            line += random.choice((str(random.randint(1, 1000)), "", word))
            totaldata += len(line)
            if totaldata > maxbytes:
                break
            lines.append(line)
            if i and i % 1000 == 0:
                print(f"Generating, iteration #{i}")

    with open(fname, "w", encoding="UTF-8") as fhandle:
        print("\n".join(lines), file=fhandle)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("pass filename and max size (in megabytes) to generate")
    else:
        generate_example_input_data(sys.argv[1], int(sys.argv[2]))
