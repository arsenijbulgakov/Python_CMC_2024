import argparse
import cowsay
import random
import urllib.request
from io import StringIO
from typing import List


hedgehog_cow = cowsay.read_dot_cow(StringIO("""

$the_cow = <<EOC;
  $thoughts
    $thoughts
      $thoughts
       $thoughts

    ______________________¶________________________________
_____________________¶¶¶_______________________________
___________________¶¶¶¶¶¶______________________________
__________________¶¶___¶¶¶¶___________¶¶¶¶¶¶___________
_________________¶¶____¶¶¶¶¶_____¶¶¶¶¶¶¶¶¶¶____________
________________¶¶_____¶¶¶¶¶¶¶¶¶¶¶_____¶¶¶¶____________
_____¶¶¶¶¶¶¶¶¶¶¶¶_______¶¶¶¶¶¶¶________¶¶¶¶____________
_____¶¶¶_¶_¶¶¶¶¶¶______¶¶¶¶¶_________¶¶¶_¶¶____________
_____¶¶¶____¶¶¶¶¶¶¶_____¶¶___________¶¶¶_¶¶_¶¶_________
_____¶¶¶____¶¶¶___________¶¶_________¶¶¶_¶___¶_________
_____¶¶¶____¶¶¶_________¶¶_¶¶_______¶¶¶¶¶¶_____________
_____¶¶¶__¶¶¶¶¶¶¶_____¶¶¶___¶____¶_¶¶¶¶¶_¶¶¶¶¶_________
____¶¶__¶¶¶_____¶¶¶_______________¶¶¶_________¶¶¶¶¶¶¶¶_
____¶__¶¶________¶¶¶_________¶_____¶¶______________¶¶¶_
___¶¶_¶¶__________¶¶________¶¶_______¶___________¶¶¶¶¶_
__¶¶__¶¶__________¶¶¶¶¶¶¶¶¶__¶¶_______¶______¶_¶¶¶¶¶¶__
__¶___¶¶_____¶¶¶¶_¶¶¶¶___¶¶¶¶__________¶____¶¶¶¶¶¶¶¶¶__
__¶____¶¶____¶¶¶¶¶¶________¶¶¶_________¶¶¶¶¶¶¶¶¶¶¶__¶__
_¶¶_____¶¶¶¶¶¶¶¶¶¶_____¶____¶¶¶_________¶¶¶¶¶¶¶¶¶__¶___
_¶________¶¶¶¶_¶¶___¶¶¶¶_____¶¶_________¶__¶¶¶_¶_______
_¶¶_________¶__¶¶____¶¶_____¶¶¶¶¶¶¶_____¶______¶¶______
_¶¶_________¶¶__¶¶_________¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶_____¶¶_____
__¶_____________¶¶¶¶_____¶¶¶¶¶¶_¶¶¶¶¶¶¶¶¶¶¶¶_____¶¶____
__¶¶______________¶¶¶¶¶¶¶¶¶¶______________¶¶______¶¶___
__¶¶¶¶¶¶¶¶___¶¶¶______¶¶¶_________¶_______¶¶¶¶¶¶___¶___
__¶______¶¶____________________¶_¶¶¶_____¶¶¶¶¶¶¶¶¶¶¶¶__
__¶¶¶¶¶_¶¶¶_________________¶_¶_¶__¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶__
_____¶¶¶¶¶_______________¶_______¶__¶¶¶¶¶__________¶¶__
_______¶¶¶______¶_¶¶¶_¶¶¶_¶_¶____¶__¶__________________
_________¶¶¶¶____¶_¶_¶_¶________¶___¶¶_________________
___________¶¶¶¶¶____________¶¶¶____¶¶¶_________________
_______________¶¶¶¶¶¶¶¶¶¶¶¶¶__¶¶¶¶¶¶¶__________________
__________________¶¶___¶¶_¶¶____¶______________________
__________________¶¶___¶___¶¶__________________________
______________¶_____¶¶______¶¶_________________________
______________¶¶____¶______¶¶¶_________________________
_______________¶¶¶¶¶¶¶__¶¶¶¶¶__________________________
_______________________________________________________

EOC"""))


def ask(prompt: str, valid: List[str] = None) -> str:
    print(cowsay.cowsay(message=prompt, cowfile=hedgehog_cow))
    while True:
        guess = input()
        if valid is None or guess in valid:
            return guess
        else:
            print(cowsay.cowsay(message="Вы ввели недопустимое слово, попробуйте еще раз", cowfile=hedgehog_cow))


def inform(format_string: str, bulls: int, cows: int) -> None:
    cow = random.choice(cowsay.list_cows())
    print(cowsay.cowsay(message=format_string.format(bulls, cows), cow=cow))


def bullscows(guess: str, secret: str) -> (int, int):
    bulls = 0
    cows = 0

    for char1, char2 in zip(guess, secret):
        if char1 == char2:
            bulls += 1
    cows = len(set.intersection(set(guess), set(secret)))

    return bulls, cows


def gameplay(ask: callable, inform: callable, words: List[str]) -> int:
    secret = random.choice(words)
    num_iters = 0
    
    while True:
        num_iters += 1
        guess = ask("Введите слово: ", words)
        bulls, cows = bullscows(guess, secret)
        inform("Быки: {}, Коровы: {}", bulls, cows)
        if guess == secret:
            return num_iters


def get_words_by_url(url: str) -> List[str]:
    text = urllib.request.urlopen(url)
    lst = []

    for line in text:
        decoded_line = line.decode("utf-8")[:-1]
        lst.append(decoded_line)

    return lst


def get_words_from_file(filename: str) -> List[str]:
    with open(filename, "r") as f:
        words = list(map(lambda x: x[:-1], f.readlines()))
    return words


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dict', required=False, default='https://raw.githubusercontent.com/Harrix/Russian-Nouns/main/dist/russian_nouns.txt', type=str)
    parser.add_argument('--length', required=False, default=5, type=int)
    args = parser.parse_args()

    if args.dict.startswith('http:') or args.dict.startswith('https:'):
        words = get_words_by_url(args.dict)
    else:
        words = get_words_from_file(args.dict)

    words = [word for word in words if len(word) == args.length]
    num_iters = gameplay(ask, inform, words)
    print(f"Поздравляем! Вы угадали слово. Число попыток: {num_iters}")


if __name__ == "__main__":
    main()
