import sys

if len(sys.argv) == 1:
    print("none")
else:
    print("parameters:", len(sys.argv) - 1)

    for word in sys.argv[1:]:
        print(word + ":", len(word))