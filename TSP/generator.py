import random


def generate():
    f = open("input.txt", "w+")
    n = input()
    f.write('%s \n' % n)
    for i in range(int(n)):
        x = random.randint(-1000, 1000)
        y = random.randint(-1000, 1000)
        f.write(x.__str__() + " " + y.__str__() + "\n")


def main():
    generate()


if __name__ == '__main__':
    main()
