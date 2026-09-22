import sys

if len(sys.argv) < 1:
    print("none")
else:
    for text in reversed(sys.argv[1:]):
        print(text)