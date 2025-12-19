
def sentence_analysis(sentence):

    """Q1:
    Write a Python program that takes a sentence from the user and prints:

    Number of characters

    Number of words

    Number of vowels

    Hint: Use split(), loops, and vowel checking."""

    num_chars_without_space = len(sentence.replace(" ",""))
    num_words = len(sentence.split())
    vowels = set("aeiouAEIOU")
    sum_of_vowels = 0
    for ch in sentence:
        if ch in vowels:
            sum_of_vowels +=1

    return num_chars_without_space, num_words, sum_of_vowels


def even_odd(nums):

    """Q2:
    Count Even and Odd Numbers
    Take a list of numbers as input (comma-separated).
    Count how many are even and how many are odd.
    Print results.
    Example Input:
    10, 21, 4, 7, 8
    
    retuns number of even numbers and odd numbers"""
    even = 0
    odd = 0

    for num in nums:
        if(num % 2 == 0):
            even +=1
        else:
            odd +=1
    return even, odd

    
if __name__ == "__main__":
    sentence = input("Enter the sentence: ")
    num_chars, num_words, sum_of_vowel = sentence_analysis(sentence)
    print(f"number of character are in {sentence} is {num_chars}")
    print(f"number of words are in {sentence} is {num_words}")
    print(f"number of words are in {sentence} is {sum_of_vowel}")
    print("\n\n")

    user_input_nums = input("enter numbers separated by commas: ")
    number_list = []

    for item in user_input_nums.split(","): 
        number_list.append(int(item.strip()))

    even, odd = even_odd(number_list)

    print(f"number of even numbers in {number_list} is {even}")
    print(f"number of odd numbers in {number_list} is {odd}")
    print("\n\n")

