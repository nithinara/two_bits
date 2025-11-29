from collections import defaultdict
import random

BIT_SIZE = 2

WORD_BANK = 'word_bank.txt'
QUESTION_MARK = '?'
DELINEATE = '====='
COMMA_SEPARATOR = ', '

GAME_DESCRIPTION = ('GAME DESCRIPTION\n'
                'We have taken a word and replaced its first two letters with question marks.\n'
                'These two letters, as a unit, can be shifted elsewhere to form a new word.\n'
                'For example, ??WARD could represent REWARD.\n'
                'Shifting the RE three positions to the right would make WARRED, the answer.\n'
                'The shifted pair of letters may end up in any position within or at the end of the new word.\n'
                'Original description by Mike Shenk')
INSTRUCTIONS = ('INSTRUCTIONS\n'
                'When prompted, type in your answer.\n'
                'You get 1 point for each correct answer.\n'
                'There are no penalities for incorrect answers.\n'
                'You will play multiple rounds and receive a final score.\n'
                'If you give up for that round, type the letter "a".\n'
                'If you want to quit the game, type the letter "q"')
SEARCHING = 'Searching for a new starting word...'
QUIT = 'Q'
ANSWER = 'A'
CORRECT = 'Correct'
WRONG = 'Incorrect'
PROMPT = 'Find the solution for: '
STARTING_WORDS = 'The following were all valid starting word(s): '
SOLUTIONS = 'The following were all valid solution(s): '
SCORE = 'You have scored {} point(s) out of {} round(s)'

def run():
    word_bank = get_word_bank()
    partitioned_word_bank = partition_word_bank_by_length(word_bank)

    play_game(word_bank, partitioned_word_bank)

def get_bit_size():
    return BIT_SIZE

def get_question_marks_str():
    return ''.join([QUESTION_MARK for _ in range(get_bit_size())])

def get_random_word(word_bank):
    return random.choice(word_bank)

def enumerate_solutions(word_bank, base, bits):
    solutions = set()

    for i, char in enumerate(base):
        if i > 0:
            candidate = base[:i] + bits + base[i:]
            if candidate in word_bank:
                solutions.add(candidate)

    return solutions

def get_word_bank():
    filename = WORD_BANK

    with open(filename) as f:
        word_bank = f.read().splitlines()

    return word_bank

def partition_word_bank_by_length(word_bank):
    partitioned_word_bank = defaultdict(list)

    for word in word_bank:
        partitioned_word_bank[len(word)].append(word)

    return partitioned_word_bank

def get_starting_word_and_solutions(word_bank):
    starting_word = ''
    solutions = set()

    while not solutions:
        starting_word = get_random_word(word_bank)
        solutions = enumerate_solutions(word_bank, starting_word[get_bit_size():], starting_word[:get_bit_size()])

    return starting_word, solutions

def find_all_starting_words(starting_word, partitioned_word_bank):
    same_length_words = partitioned_word_bank[len(starting_word)]
    all_starting_words = set()

    for word in same_length_words:
        if word.endswith(starting_word[get_bit_size():]):
            all_starting_words.add(word)

    return all_starting_words

def find_valid_starting_words_and_other_solutions(all_starting_words, word_bank):
    valid_starting_words = set()
    other_solutions = set()

    for starting_word in all_starting_words:
        solutions = enumerate_solutions(word_bank, starting_word[get_bit_size():], starting_word[:get_bit_size()])
        if solutions:
            valid_starting_words.add(starting_word)
            for solution in solutions:
                other_solutions.add(solution)

    return valid_starting_words, other_solutions

def verify_valid_starting_words_not_equals_solutions(valid_starting_words, solutions):
    if len(valid_starting_words) == 1 and len(solutions) == 1 and next(iter(valid_starting_words)) == next(iter(solutions)):
        return False

    return True

def play_round(starting_word, valid_starting_words, solutions, num_rounds, num_points):
    new_round = False
    won_round = False

    while True:
        user_input = input(PROMPT + get_question_marks_str() + starting_word[get_bit_size():] + '\n')

        if user_input.lower() == QUIT.lower():
            print(STARTING_WORDS + COMMA_SEPARATOR.join(sorted(valid_starting_words)))
            print(SOLUTIONS + COMMA_SEPARATOR.join(sorted(solutions)))
            print(SCORE.format(num_points, num_rounds))
            break
        elif user_input.lower() == ANSWER.lower():
            print(STARTING_WORDS + COMMA_SEPARATOR.join(sorted(valid_starting_words)))
            print(SOLUTIONS + COMMA_SEPARATOR.join(sorted(solutions)))
            print(SCORE.format(num_points, num_rounds))
            new_round = True
            break
        elif user_input.lower() not in solutions:
            print(WRONG)
            continue
        else:
            print(CORRECT)
            print(SCORE.format(num_points + 1, num_rounds))
            new_round = True
            won_round = True
            break

    return new_round, won_round

def play_game(word_bank, partitioned_word_bank):
    print(GAME_DESCRIPTION)
    print(DELINEATE)
    print(INSTRUCTIONS)
    print(DELINEATE)

    num_rounds = 0
    num_points = 0
    play_new_round = True

    while play_new_round:
        print(SEARCHING)
        num_rounds += 1
        valid_round = False

        while not valid_round:
            starting_word, solutions = get_starting_word_and_solutions(word_bank)

            all_starting_words = find_all_starting_words(starting_word, partitioned_word_bank)

            valid_starting_words, other_solutions = find_valid_starting_words_and_other_solutions(all_starting_words, word_bank)
            solutions.update(other_solutions)

            valid_round = verify_valid_starting_words_not_equals_solutions(valid_starting_words, solutions)

        print(valid_starting_words, solutions)
        play_new_round, increment_points = play_round(starting_word, valid_starting_words, solutions, num_rounds, num_points)

        if increment_points:
            num_points += 1

if __name__ == '__main__':
    run()
