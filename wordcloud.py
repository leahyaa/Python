# Install necessary dependencies
import requests
import matplotlib.pyplot as plot
from wordcloud import WordCloud

def menu():
    #print the instruction
    print('The program performs text-based data analysis.')
    print('Choose from the following options:')
    print('1 - Use a user-specified text file')
    print('2 - Access the U.S. Constitution from Project Gutenberg')
    print("Access all 4 of Abraham Lincoln's State of the Union speeches from Project Gutenberg")
    print('4 - Quit the program')
    
    # while loop to make sure user enters the right number
    while True:
        user_num = int(input('Enter 1, 2, 3, or 4 to quit.'))
        if user_num == 1 or user_num == 2 or user_num == 3 or user_num == 4 :
            break
    return user_num


def load_localfile():
    
    while True:
        try:
            with open(input("Please enter your file name: "), 'r') as datafile:
                line_list = datafile.readlines()
                break
        except FileNotFoundError:
            print("File not found")
    return line_list
            
def process_text(dirty_text):
    ''' remove all punctuation, newlines, and numbers from the text,
        lowercase all of it, return cleaned text as a list of strings '''
    clean_text = []
    for each_line in dirty_text:
        
        # replace a bunch of characters
        fixed_text = each_line.replace('\n'," ")  
        fixed_text = fixed_text.replace('.',' ')
        fixed_text = fixed_text.replace(','," ") 
        fixed_text = fixed_text.replace('?'," ") 
        fixed_text = fixed_text.replace('!'," ") 
        fixed_text = fixed_text.replace(':'," ") 
        fixed_text = fixed_text.replace(';'," ") 
        fixed_text = fixed_text.replace('"'," ") 
        fixed_text = fixed_text.replace("'"," ") 
        fixed_text = fixed_text.replace('-'," ") 
        fixed_text = fixed_text.replace('/'," ")
        fixed_text = fixed_text.replace('\\' , " ")
        # make the words lower case
        clean_text.append(fixed_text.lower())
    
    return clean_text

def build_dict(string_list):
    ''' build a word-frequency dictionary based on the list of strings,
        return the dictionary '''
    file_dict = {}
    for each_line in string_list:
            # split each line into words
        for each_word in each_line.split():
            # update exiting key-value pair
            if each_word in file_dict:
                file_dict[each_word] += 1
                # insert new key-value
            else:
                file_dict[each_word] = 1
    return file_dict

def report_counts(word_dict):
    ''' report on the total word count and total character count '''
    # YOUR CODE HERE
    total_words = sum(word_dict.values())
    unique_words = len(word_dict)
    print('\nThere are a total of', total_words, 'words in this selection.')
    print('There are', unique_words, 'unique words in this selection.')   


def report_wordlength(w_dict):
    ''' report on the average word length, min, and max '''
    total_letters = 0
    max_length = 1
    min_length = None
    for key in w_dict:
        total_letters += len(key) * w_dict[key]
        # get the max word length
        max_length = max(max_length, len(key)) 
        # get the min word length
        if min_length is None or min_length > len(key):
            min_length = len(key) 
    # get the average word length         
    average_length = total_letters / sum(w_dict.values())
    
    print(f"\nThe average word length is {average_length:.1f}.")
    print(f"The minimum length is {min_length} and the maximum length is {max_length}.")


def report_10longest(w_dict):
    ''' report the 10 longest words in the dictionary, and their frequency '''
    # make every word-length pair a tuple, put all the tuples in a list
    w_list = []  
    for key in w_dict:    
        w_list.append((-len(key),key))
    
    # pull out the first 10 elements in the list
    top10long = sorted(w_list)[:10]
    print('\nThe 10 longest words are:')
    
    # print the top10long list
    for length,word in top10long:
        print(f"{word}, found {w_dict[word]} times")


def save_wordcloud(w_dict):
    ''' save a wordcloud figure for the dictionary '''
    # YOUR CODE HERE
    wordcloud = WordCloud(colormap='prism', background_color='white', max_words=100)
    wordcloud.fit_words(w_dict)
    wordcloud.to_file('wordcloud.png')

def graph_word_lengths(w_dict):
    ''' create a graph showing number of words of lengths 1 to 9 letters long '''
    # YOUR CODE HERE
            
    w_count = [0] * 9 # the valus list
    for key in w_dict:
        length = len(key)
        if 1 <= length <= 9:
            w_count[length-1] += w_dict[key]
    
    
    figure = plot.figure() #start with a blank figure 
    axes = figure.add_axes([0,0,1,1]) 
    labels = ['1','2','3','4','5','6','7','8','9'] 
    values = w_count
    axes.bar(labels,values) 
    axes.set_title('Number of words of each length') 
    plot.show()   


    
def load_gutenberg_constitution():
    ''' load data from Project Gutenberg into a list of lines, return list '''
    # YOUR CODE HERE
    full_text = requests.get('https://www.gutenberg.org/cache/epub/5/pg5.txt').text
    # take this big block of text and convert to a list of strings, one line per string
    text_list = full_text.split('\n') 
    # remove first 83 lines and end on line 676
    final_list = text_list[83:677]

    return final_list

def load_gutenberg_lincoln_SOTUs():
    ''' load data from Project Gutenberg into a list of lines, return list '''
    # YOUR CODE HERE
    full_text = requests.get('https://www.gutenberg.org/cache/epub/5024/pg5024.txt').text
    # take this big block of text and convert to a list of strings, one line per string
    text_list = full_text.split('\n') 
    
    return text_list

def main(): 
    while True: # while loop to make sure the program will continue unless user chose option 4
        user_num = menu()#print the menu
        if user_num == 1: # user upload file
            data_text = load_localfile() 
        elif user_num == 2: 
            data_text = load_gutenberg_constitution()
        elif user_num == 3:
            data_text = load_gutenberg_lincoln_SOTUs()
        elif user_num == 4:
            break
        # we have a dirty_text which is a string list by now
        clean_text = process_text(data_text)
        data_dict = build_dict(clean_text) 
        report_counts(data_dict)
        report_wordlength(data_dict)
        report_10longest(data_dict)
        save_wordcloud(data_dict)
        graph_word_lengths(data_dict)
        
main()
