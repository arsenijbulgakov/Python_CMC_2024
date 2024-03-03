import argparse
import cowsay
import random
import urllib.request
from typing import List


def ask(prompt: str, valid: List[str] = None) -> str:
    cow = random.choice(cowsay.list_cows())
    print(cowsay.cowsay(message=prompt, cow=cow))
    while True:
        guess = input()
        if valid is None or guess in valid:
            return guess
        else:
            print(cowsay.cowsay(message="Вы ввели недопустимое слово, попробуйте еще раз", cow=cow))


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
