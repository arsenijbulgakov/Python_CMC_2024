import argparse
import cowsay


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('-e')
    parser.add_argument('-f')
    parser.add_argument('-l', action='store_true')
    parser.add_argument('-n', action='store_true')
    parser.add_argument('-T')
    parser.add_argument('-W', type=int)

    parser.add_argument('-b', action='store_true')
    parser.add_argument('-d', action='store_true')
    parser.add_argument('-g', action='store_true')
    parser.add_argument('-p', action='store_true')
    parser.add_argument('-s', action='store_true')
    parser.add_argument('-t', action='store_true')
    parser.add_argument('-w', action='store_true')
    parser.add_argument('-y', action='store_true')

    parser.add_argument('message', nargs='*')

    args = parser.parse_args()

    if args.l:
        print(cowsay.list_cows())
        return

    cow = "default"
    cowfile = None
    if args.f is not None:
        if args.f.startswith("/"):
            cowfile = args.f
        else:
            cow = args.f

    eyes = "oo"
    if args.e is not None:
        eyes = args.e[:2]

    tongue = "  "
    if args.T is not None:
        tongues = args.T[:2]

    width = 40
    if args.W is not None:
        width = args.W

    wrap_text = True
    if args.n:
        wrap_text = False

    preset = None
    if args.b:
        preset = "b"
    elif args.d:
        preset = "d"
    elif args.g:
        preset = "g"
    elif args.p:
        preset = "p"
    elif args.s:
        preset = "s"
    elif args.t:
        preset = "t"
    elif args.w:
        preset = "w"
    elif args.y:
        preset = "y"

    message = " ".join(args.message)

    print(cowsay.cowsay(
        message=message,
        cow=cow,
        preset=preset,
        eyes=eyes,
        tongue=tongue,
        width=width,
        wrap_text=wrap_text,
        cowfile=cowfile
    ))



if __name__ == '__main__':
    main()
