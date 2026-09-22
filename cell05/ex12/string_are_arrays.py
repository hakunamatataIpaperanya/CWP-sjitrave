import sys

if len(sys.argv) != 2:
    print("none")
else:
    count = 0

    for letter in sys.argv[1]:
        if letter == "z":
            count += 1

    if count == 0:
        print("none")
    else:
        print("z" * count)