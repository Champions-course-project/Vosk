import json
import os


def try_to_open(input_filename):
    """
    Try to open and read selected file.\n
    On success return list with words inside the file.\n
    On failure ask for list of words from the console and return it instead.\n
    """
    words_list = None
    try:
        # option 1: if file with words is given
        if input_filename != None:
            with open(input_filename, "r", encoding="UTF-8") as IF:
                words_list = []
                for word in IF:
                    words_list.append(word.replace("\n", "").lower())
    except OSError:
        pass
    finally:
        # option 2: if file name wasn't given or is invalid
        if words_list == None:
            words_list = input(
                "Введите слово или набор слов для преобразования в набор фонем: ").lower().split(" ")
    return words_list


def wordToPhones(*input_filenames):
    """
    Transcribe word from text file or from keyboard to the text file.\n
    Return: file lexicon.txt
    """
    # open file with phones
    with open("letters_to_phones.json", "r", encoding="UTF-8") as F:
        LTF = json.load(F)
    # get words
    dict_list = [{"!SIL": ["SIL"]},
                 {"[unk]": ["GBG"]}]
    for input_filename in input_filenames:
        input_words = try_to_open(input_filename)

        # for every single word in input (empty is also a word btw):
        for input_word in input_words:
            # create an empty list of phonems
            phones_base = []
            # for every letter in the word:
            for i in range(len(input_word)):
                # if this letter is a vowel:
                if input_word[i] in LTF["vowel"]:
                    # and if this vowel can give only one sound, regardless of its neighbours:
                    if type(LTF["vowel"][input_word[i]]) == str:
                        phones_base.append(
                            (str)(LTF["vowel"][input_word[i]]) + "0")
                    # elif it can and should give two sounds:
                    elif (i == 0) or ((input_word[i - 1] in LTF["vowel"]) or (input_word[i - 1] in LTF["others"])):
                        for sound in LTF["vowel"][input_word[i]]["two"].split(" "):
                            phones_base.append((str)(sound))
                        phones_base[-1] += "0"
                    # otherwise, it can give two sounds and gives only one sound
                    else:
                        phones_base.append(
                            (str)(LTF["vowel"][input_word[i]]["one"]) + "0")
                # if, however, this letter is a consonant:
                elif input_word[i] in LTF["consonant"]:
                    # and if it can only give one sound, regardless of its neighbours:
                    if type(LTF["consonant"][input_word[i]]) == str:
                        phones_base.append(
                            (str)(LTF["consonant"][input_word[i]]))
                    # elif it can give both soft and hard sound, and should give soft sound:
                    elif (i != len(input_word) - 1) and (input_word[i + 1] in ("е", "ё", "ю", "я", "и", "ь")):
                        phones_base.append((str)(LTF["consonant"]
                                                 [input_word[i]]["soft"]))
                    # otherwise, it will give hard sound
                    else:
                        phones_base.append(
                            (str)(LTF["consonant"][input_word[i]]["hard"]))
            # if the word was empty:
            if phones_base == []:
                phones_base.append("SIL")

            # check for every possible stressed sound. j o isn't recognised as stressed sound by default, so should be reworked a bit
            all_options = []
            replaced = False
            for i in range(len(phones_base)):
                if "0" in phones_base[i]:
                    phones_base[i] = phones_base[i].replace("0", "1")
                    all_options.append(" ".join(phones_base))
                    phones_base[i] = phones_base[i].replace("1", "0")
                    replaced = True
            if not replaced:
                all_options.append(" ".join(phones_base))
            dict_list.append({input_word: all_options})
    # write everything to an output file
    with open("lexicon.txt", "w", encoding="UTF-8", newline="\n") as OF:
        for dictionary in dict_list:
            word = (list)(dictionary.keys())[0]
            phonems_list = (list)(dictionary.values())[0]
            for phonems_word in phonems_list:
                OF.write(f"{word} {phonems_word}\n")
    return


def create_grammar(input_filename):
    """
    Create G.txt file based on input words. 
    Consider that all words have equal probability of appearance.
    """
    # get input words
    input_words = ["[unk]"] + try_to_open(input_filename)
    # for every word in the input - write in in a special format
    with open("G.txt", "w", encoding="UTF-8", newline='\n') as OF:
        for word in input_words:
            OF.write(f"0 1 {word} {word}\n")
        OF.write("1 0.0\n")
    return


def append_dates_grammar(dates_grammar_filename):
    """
    Append to a G.txt file dates grammar file.
    It uses separated graph points.
    """
    input_grammar = []
    with open(dates_grammar_filename, "r", encoding="UTF-8") as F:
        for line in F:
            input_grammar.append(line.replace("\n", ""))
    with open("G.txt", "a", encoding="UTF-8", newline="\n") as OF:
        for line in input_grammar:
            output_line = line.split(" ")
            try:
                OF.write(output_line[0] + " " + output_line[1] +
                         " " + output_line[2] + " " + output_line[2] + '\n')
            except:
                OF.write(line + '\n')
    return


try:
    os.chdir("text-to-phonem test")
except (OSError, FileNotFoundError):
    pass
input_file = "input_file.txt"
dates_input_file = "dates_input.txt"
dates_grammar_file = "dates_grammar.txt"

try:
    wordToPhones(input_file, dates_input_file)
    create_grammar(input_file)
    append_dates_grammar(dates_grammar_file)
    pass
except Exception as ex:
    print("An uncaught exception.")
    print("Name: {0}".format(type(ex).__name__))
    print("Args: {0}".format(ex.args))
    raise
except KeyboardInterrupt:
    print("\nExtiting...")
