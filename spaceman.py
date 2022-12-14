import random
import re

def load_word():
    '''
    Reads a text file containing a list of space-separated words, 'words.txt',
    and pseudorandomly selects one word from the list.

    Returns: 
           string: The secret word to be used in the spaceman guessing game
    '''
    with open('words.txt', encoding='utf-8') as input_file:
        words_list = input_file.readlines()
    
    words_list = words_list[0].split(' ')
    secret_word = random.choice(words_list)
    return secret_word

def is_word_guessed(secret_word, letters_guessed):
    '''
    A function that checks if all the letters of the secret word have been guessed.

    Args:
        secret_word (string): the random word the user is trying to guess.
        letters_guessed (list of strings): list of letters that have been guessed so far.

    Returns: 
        bool: True only if all the letters of secret_word are in letters_guessed, False otherwise
    '''
    #Loop through the letters in the secret_word and check if a letter is not in lettersGuessed
    for letter in secret_word:
        if letter not in letters_guessed:
            return False
    
    return True

def get_guessed_word(secret_word, letters_guessed):
    '''
    A function that is used to get a string showing the letters guessed so far in the
    secret word and underscores for letters that have not been guessed yet.

    Args: 
        secret_word (string): the random word the user is trying to guess.
        letters_guessed (list of strings): list of letters that have been guessed so far.

    Returns: 
        string: The guessed word with the correct guesses so far filled in, and the
        letters that have yet be guessed replaced by underscores
    '''
    #Loop through the letters in secret word and build a string that shows the letters
    #that have been guessed correctly so far that are saved in letters_guessed and underscores
    #for the letters that have not been guessed yet
    out_string = ''
    for letter in secret_word:
        if letter in letters_guessed:
            out_string += letter
        else:
            out_string += '_'

    return out_string

def is_guess_in_word(guess, secret_word):
    '''
    A function to check if the guessed letter is in the secret word

    Args:
        guess (string): The letter the player guessed this round
        secret_word (string): The secret word

    Returns:
        bool: True if the guess is in the secret_word, False otherwise

    '''
    return guess in secret_word
    
def load_sinister_word(current_word, letters_guessed):
    '''
    A function that loads a new secret word, which is the same length and contains the currently
    guessed letters as the current secret word, in the same positions. The new word COULD contain
    additional occurences of already guessed letters, which will be marked as guessed and filled in.

    Args:
        current_word (string): The current secret word
        letters_guessed (list): The list of letters that have been guessed so far

    Returns:
        string: The new secret word
    '''
    #use same methods as above to open file and get list containing all the words in the file
    with open('words.txt', encoding='utf-8') as input_file:
        words_list = input_file.readlines()
    #get the string representation of the current guess progress
    guessed_word = get_guessed_word(current_word, letters_guessed)
    #build a regex out of guessed_word; '_" gets replaced with the regex [a-zA-Z]
    guessed_word = re.sub('_', '[a-zA-Z]', guessed_word)
    #spaces ensure don't match parts of words separated by line breaks
    guessed_word_regex = ' ' + guessed_word + ' '
    #find all matching words and save them in a list
    matches = re.findall(guessed_word_regex, words_list[0])
    #choose a random word from the list of matches to be the new secret word
    try:
        new_word = random.choice(matches).strip() #strip to remove leading and trailing whitespace
        #if the matches array is empty (ie no sinister match exists) an error is thrown;
        #in this case keep using the original word
    except IndexError:
        new_word = current_word

    return new_word

def spaceman(secret_word):
    '''
    A function that controls the game of spaceman. Called with a secret word
    to initiate a game of spaceman.

    Args:
      secret_word (string): the secret word to guess.

    '''
    game_over = False
    incorrect_guesses = 0
    guess_limit = len(secret_word)
    letters_guessed = []
    is_sinister = False

    #show the player information about the game according to the project spec
    print('Welcome to spaceman! Try to fill in the spaces by guessing one letter at a time.' +
          f'If you guess incorrectly {guess_limit} times, you lose!')
    print(f'There are {guess_limit} letters in the secret word.')
    play_sinister = input('Enter anything else for a normal game of spaceman, ' +
                          'or 2 for a sinister game...')
    if play_sinister == '2':
        is_sinister = True

    #primary game loop
    while not game_over:
        #show the guessed word so far
        print(f'The word so far is {get_guessed_word(secret_word, letters_guessed)}')
        print(f'The letters guessed for far are: {", ".join(letters_guessed)}')
        valid_guess = False
        #input validation, ensure guess is single letter
        while not valid_guess:
            guess = input('Enter a single letter guess: ').lower()
            if guess in letters_guessed:
                print('You already guessed that letter! Enter a different letter; no guess consumed.')
            elif len(guess) == 1 and re.search("[a-zA-Z]", guess):
                valid_guess = True
            else:
                print('Invalid guess. Single letters only! No numbers, special symbols, or words.')

        #initialize correct_guess value that will be part of sinister condition
        correct_guess = False
        #Check if the guessed letter is in the secret or not and give the player feedback
        if is_guess_in_word(guess, secret_word) is True:
            print('You\'re guess is in the word!')
            correct_guess = True
        else:
            incorrect_guesses += 1
            print(f'Oh no, the guess isn\'t in the word! {guess_limit - incorrect_guesses}' +
                  ' incorrect guesses remaining.')
        
        letters_guessed.append(guess)
        #check if the game has been won or lost
        if incorrect_guesses >= guess_limit:
            print(f'More than {guess_limit} incorrect guesses have been made, sorry, you lose!' +
                  f' The word was {secret_word}')
            game_over = True
        elif is_word_guessed(secret_word, letters_guessed) is True:
            print(f'Great job, you guessed the word, which was {secret_word}.')
            game_over = True

        #if playing sinister style, get a new word
        if is_sinister and correct_guess:
            secret_word = load_sinister_word(secret_word, letters_guessed)

#call the function spaceman to play the game as long as the player wants to keep playing

while True:
    HIDDEN_WORD = load_word()
    spaceman(HIDDEN_WORD)

    RESPONSE = input('Play again with a new word? Enter 1 to play again, any other key to quit. >')
    if RESPONSE == '1':
        continue
    else:
        break
