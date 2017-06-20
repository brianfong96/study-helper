'''
Study helper

Can write to text files to generate tests

Can take a test

Prints
    Multiple choice questions
    Fill in the blank
    True or False
    Reads from a text file using readline and .split('//')

FIXES & Upgrades
10/09/2016 - fixed answers checking for spaces in fill in the blank
10/10/2016 - checks for user answer on MC and TF now
10/10/2016 - stops generating file with same name in memory
10/11/2016 - can edit files now, fixed fill in the blank prompt, fixed program crash from just enter as answer input

'''

#===================================================================================
# Imports
#===================================================================================

from random import randint
import os
import sqlite3
#===================================================================================
# Classes
#===================================================================================

class Study_Helper:
    
    def __init__(self):
        self.prompt_start_menu ='''
=================================================
START MENU
=================================================
Hi! My name is %s
I will be your study helper!
I can let you :
    -write your own tests by entering questions and answers,
    -take a test that you wrote for practice

Here are the lists of test files that you can read from: '''
        self.name = input('''
Enter the name of your study helper:
> ''')
        self.start_menu()

    def start_menu(self):
        '''
        Clears all variable
        prints an introduction
        determines what mode to go to
        '''
        
        # numbers
        self.question_number = 0
        self.question_number_total = 0
        self.score = 0
        self.score_total = 0
        self.current_question_number = 0
        self.unanswered_questions = 0
        self.answer = 2                         # answer for multiple choice

        # strings
        self.data_file = ''
        self.question_prompt = ''
        self.user_answer = ''
        self.memory_file = 'memory.txt'
        self.backup = 'backup memory.txt'
        self.user_file = ''
        self.user_in = ''
        self.user_question = ''
        self.answer_type =''
        
        # lists
        self.question = []
        self.question_bank = []
        self.used_question_bank = []
        self.current_question = []
        self.file_list = []
        self.invalid_chars = [',', '*', '\'', '"', '/', '\\', '[', ']', ':', ';', '|', '=']

        # Booleans
        self.valid_input = False
        self.getting_input = False
        self.valid_file = False
        self.is_terminated = False

        
        self.file_read_memory()
        print(self.prompt_start_menu %self.name)
        for i in range(0, len(self.file_list), 2):
            if i != len(self.file_list)-1:
                print("%s, %s" %(self.file_list[i], self.file_list[i+1]))
            else :
                print("%s" %self.file_list[i])

        while not self.valid_input:
            self.user_answer = input('''
Do you want to read or write a test file?
    (Enter 'r', 'w', or 'q' to quit)...
> ''').upper()
            if self.user_answer == 'R' or self.user_answer == 'W' or self.user_answer == 'Q':
                self.valid_input = True
                
        if self.user_answer == 'R':
            self.user_file_read()
        elif self.user_answer == 'W':
            self.user_file_write()
        elif self.user_answer == 'Q':
            self.terminate()
            
#==========================================================================================================
# Write to text file methods
#==========================================================================================================

    def user_file_write(self):
        '''
            User writes a file automatically adds split character '//'
            asks for type of question
            asks for question
            asks for multiple choices if type is MC
            asks for answer
            saves name to memory through file_write_ememory
        '''

        print('''
=================================================
GOING INTO WRITE MODE...
=================================================
''')
        
        self.valid_input = False
        # Get file name        
        while not self.valid_input:
            self.user_file = input("""
Please enter the name of your file...
> """)
            for i in range(len(self.invalid_chars)):
                if not self.invalid_chars[i] in self.user_file :
                    self.valid_input = True
                elif not self.valid_input:
                    print('''
You've entered an invalid file name
''')
        if self.user_file[len(self.user_file)-4:] != '.txt':
            self.user_file += '.txt'
            
        try:
            
            self.file = open(self.user_file, 'r')
            self.is_getting_file = True
            while(self.is_getting_file and not self.is_terminated):        
                if not self.is_terminated: 
                    self.temp = self.file.readline().split('//')                
                    if self.temp[0] == 'END':
                        self.temp.close()
                        self.is_getting_file = False
                    for string in self.temp:
                        #print(string)
                        if string != '\n':
                            self.user_question += string+'//'
                        else:
                            self.user_question += string
                        #print(self.user_question)
            self.file = open(self.user_file, 'w')
            
        except:
            self.file =  open(self.user_file, 'w')
            
        self.getting_input = True
        self.valid_input = False

        # Get questions for test
        while self.getting_input:
            self.valid_input = False
            
            # get question type
            while not self.valid_input:
                self.user_in = input('''
Please enter your question type
'MC' - for multiple choice
'FB' - for fill in the blank
'TF' - for true/false
> ''').upper()
                if self.user_in == 'MC' or self.user_in == 'FB' or self.user_in == 'TF':
                    self.valid_input = True
                    self.user_question += self.user_in + '//'
                    self.temp = self.user_in
                else:
                    print('''
You've entered an invalid question type
''')

            # get question
            self.valid_input = False
            while not self.valid_input:
                self.user_in = input('''
Enter your question as is and press enter when done
(Do not include backslash or '//' in your question)
> ''')
                if not '\\' in self.user_in and not '//' in self.user_in : self.valid_input = True
                else:
                    print('''
You entered backslash or '//'in your question.
Please try again...
''')
            self.user_question += self.user_in + '//'
              
            if self.temp == 'MC': self.write_multiple_choice()
            elif self.temp == 'FB': self.write_fill_in_the_blank()
            elif self.temp == 'TF': self.write_true_false()

            self.user_question += '\n'
            self.user_in = input('''
Do you want to end?
Enter 'y' to end
Otherwise press anything and 'enter' to continue writing more questions
> ''').upper()
            if self.user_in == 'Y': self.getting_input = False
            else : self.getting_input = True
            

        self.user_question += '\nEND//'
        self.file.write(self.user_question)
        self.file.close()
        self.file_write_memory()


    def file_write_memory(self):
        '''
        Writes a filename to memory
        '''
        
        print('''
=================================================
WRITING FILE TO MEMORY...
=================================================
''')
        self.file_read_memory()
        if not self.user_file in self.file_list :
            self.file_list.append(self.user_file + '//\n')
        self.file_list.append('END//')
        self.memory = open(self.memory_file, 'w')
        for i in range(len(self.file_list)):
            self.memory.write(self.file_list[i]+'//\n')
        self.memory.close()
        print('''
=================================================
SUCCESSFUL WRITE TO MEMORY...
=================================================
''')

        self.return_to_start()
                          
    def write_multiple_choice(self):
        '''
            Get 4 choices for multiple choice and the write answer
        '''
        
        self.getting_input = True
        i = 1
        while self.getting_input:
            self.valid_input = False
            # Get the first four choices
            if i < 5:
                while not self.valid_input:            
                    self.user_in = input('''
Enter choice number %d
(Do not include backslash or '//' in the choice)
> ''' %i)
                    if not '\\' in self.user_in and not '//' in self.user_in : self.valid_input = True
                    else:
                        print('''
You entered backslash or '//' in your answer.
Please try again...
''')
            
            else:
                while not self.valid_input:
                    self.user_in = input('''
Enter the answer to your question as is
('a', 'b', 'c' , or 'd')
> ''').upper()
                    if self.user_in == 'A' or self.user_in == 'B' or self.user_in == 'C' or self.user_in == 'D':
                        self.valid_input = True
                        self.getting_input = False
                    else:
                        print('''
You've entered an invalid answer
Please try again
''')
            i += 1
            self.user_question += self.user_in + '//'


    def write_fill_in_the_blank(self):
        '''
            Writes the answer to fill in the blank
        '''
        self.valid_input = False

        while not self.valid_input:            
            self.user_in = input('''
Enter the answer to your question as is
(Do not include backslash or '//' in your answer)
> ''')
            if not '\\' in self.user_in and not '//' in self.user_in : self.valid_input = True
            else:
                print('''
You entered backslash or '//' in your answer.
Please try again...
''')
        self.user_question += self.user_in + '//'

    def write_true_false(self):
        '''
            Write the answer to true and false
        '''
        self.valid_input = False
        
        while not self.valid_input:
            self.user_in = input('''
Enter the answer to your question as is
('t' for true or 'f' for false)
> ''')
            if self.user_in == 't' or self.user_in == 'f':
                self.valid_input = True
            else:
                print('''
You've entered an invalid answer
Please try again
''')
        self.user_question += self.user_in + '//'

#==========================================================================================================
# Read text file and generate test methods
#==========================================================================================================

    def file_read_memory(self):
        '''
            reads file name from memory and stores in file_list
        '''
        
        print('''
=================================================
READING MEMORY...
=================================================
''')
        self.file_list = []
        self.memory = open(self.memory_file, 'r')
        self.is_getting_file = True
        
        while(self.is_getting_file and not self.is_terminated):
            if os.stat(self.memory_file).st_size == 0:
                print('''
=================================================
CORRUPTED MEMORY GOING TO BACK UP...
=================================================
''')
                self.is_getting_file = False
                self.memory.close()
                self.read_backup()
                self.start_menu()
                
            if not self.is_terminated: 
                self.file = self.memory.readline().split('//')
                if self.file[0] == 'END':
                    self.memory.close()
                    self.is_getting_file = False
                elif self.file[0] != '\n' and len(self.file[0]) > 0:
                    self.file_list.append(self.file[0])
            
        
    def read_backup(self):
        '''
            If memory.txt is blank, read backup to memory.txt and resume program
        '''
        # clear file list
        self.file_list = []
        
        print('''
=================================================
READING BACKUP...
=================================================
''')

        self.is_getting_file = True
        self.backup_file = open(self.backup, 'r')
        while(self.is_getting_file and not self.is_terminated):
            self.file = self.backup_file.readline().split('//')
            self.file_list.append(self.file[0])
            if self.file[0] == 'END':
                self.is_getting_file = False
                
        # write backup to memory
        self.memory = open(self.memory_file, 'w')
        for i in range(len(self.file_list)):
            self.memory.write(self.file_list[i])
            self.memory.write("//\n")
        self.memory.write("END//")
        self.memory.close()
        print('''
=================================================
FINISH READING BACKUP...
=================================================
''')
        
    def user_file_read(self):
        '''
            Gets the user to input the file to be read
        '''
        print('''
=================================================
GOING INTO READ MODE...
=================================================
''')

        self.valid_input = False

        while(not self.valid_input and not self.is_terminated):
            self.data_file = input('''
Enter the file you want to read from...
> ''')
            if self.data_file[len(self.data_file)-4:] != '.txt':
                self.data_file += '.txt'
            try:
                self.data = open(self.data_file, 'r')
                self.valid_input = True
                self.valid_file = True
            except:
                print('''\nSorry the file you are trying to read does not exist yet...
Do you want to return to start menu?''')
                self.user_answer = input('''Enter 'y' to go back...
> ''').upper()
                if self.user_answer == 'Y':
                    self.start_menu()

        if not self.is_terminated:
            self.get_questions()

    def get_questions(self):
        '''
            Get question based on question type stored in question[0]
            Closes file when question type is 'END'
        '''
        
        print('''
=================================================
GETTING QUESTIONS...
=================================================
''')
        
        self.is_getting_question = True
        
        while(self.is_getting_question and self.valid_file and not self.is_terminated):
            self.question = self.data.readline().split('//')
            if self.question[0] == 'END':
                self.data.close()
                self.is_getting_question = False
            elif self.question[0] != '\n':
                self.question_bank.append(self.question)
                self.question_number_total += 1
                
        if not self.is_terminated:        
            self.unanswered_questions = self.question_number_total 

            self.output_questions()
        
    def output_questions(self):
        '''
            prints out the questions in question bank in a random order
        '''
        
        print('''
=================================================
OUTPUTTING QUESTIONS...
=================================================
''')

        while self.unanswered_questions > 0 and not self.is_terminated:

            self.question_number += 1
            
            self.current_question_number = randint(0, self.unanswered_questions-1)
            self.current_question = self.question_bank[self.current_question_number]

            self.question_prompt = self.current_question[1]

            if self.current_question[0] == 'MC' : self.multiple_choice()
            elif self.current_question[0] == 'FB' : self.fill_in_the_blank()
            elif self.current_question[0] == 'TF' : self.true_false()

            self.score_total += 1
            self.question_bank[self.current_question_number], self.question_bank[self.unanswered_questions-1] = self.question_bank[self.unanswered_questions-1],self.question_bank[self.current_question_number]
            self.unanswered_questions -= 1
            
        if not self.is_terminated:    
            print('''
No more unanswered questions in %s''' %self.data_file)
            self.return_to_start()
            
    def multiple_choice(self):
        '''
            [(0)question type, (1)question, (2)A, (3)B, (4)C, (5)D, (6)Answer]
        '''
        print('''\nQuestion %s)
%s
    A) %s
    B) %s
    C) %s
    D) %s
    Enter 'a', 'b', 'c', or 'd'
    ''' %(self.question_number, self.question_prompt, self.current_question[2], self.current_question[3],
          self.current_question[4], self.current_question[5]))
        self.check_answer()
        
    def fill_in_the_blank(self):
        '''
            [(0)question type, (1)question, (2)answer]    
        '''
        print('''
Question %d)
%s''' %(self.question_number,self.question_prompt))
        self.check_answer()     
        
    def true_false(self):
        '''
            [(0)question type, (1)question,(2)answer]
        '''
        print('''
Question %d)
%s
(T)rue
(F)alse
    Enter 't' or 'f' ''' %(self.question_number, self.question_prompt))
        self.check_answer()     

    def check_answer(self):
        '''
            Checks user answer when answering question
        '''
        self.answer = 2
        self.answer_type = self.current_question[0]
        self.valid_input = False

        if self.answer_type == 'MC':
            self.answer = 6
            
        while not self.valid_input and not self.is_terminated:
            self.user_answer = input('''
Enter your answer (or 'q' to quit)...
> ''').upper()
            if self.user_answer == 'Q':
                    self.terminate()
                    
            if self.answer_type == 'FB':
                self.valid_input = True
                
            elif self.answer_type == 'MC':
                if self.user_answer == 'A' or self.user_answer == 'B' or self.user_answer == 'C' or self.user_answer == 'D':
                    self.valid_input = True
                else:
                    print('''
You've entered an invalid answer
Please try again
''')
            elif self.answer_type == 'TF':
                if self.user_answer == 'T' or self.user_answer == 'F':
                    self.valid_input = True
                else:
                    print('''
You've entered an invalid answer
Please try again
''')

        if self.valid_input and not self.is_terminated:
            if self.user_answer.replace(' ','') == self.current_question[self.answer].upper().replace(' ',''):
                print('''
You got the answer correct!''')
                self.score += 1
                
            else:
                print('''
Your answer is wrong! The correct answer is %s'''
%self.current_question[self.answer].upper())




                

    def print_final_score(self):
        print('''
Your final score is %d/%d''' %(self.score, self.score_total))

#==========================================================================================================
# Finishing methods
#==========================================================================================================

    def return_to_start(self):
        if(self.score_total != 0):
            self.print_final_score()
        
        print('''
Do you want to go to start menu?''')
        self.valid_input = False

        while (not self.valid_input) :
            self.user_answer = input('''
Enter 'y' or 'n'...
> ''').upper()
            if self.user_answer == 'Y' or self.user_answer == 'N' :
                self.valid_input = True

        if self.user_answer == 'Y' :
            self.start_menu()

        if not self.is_terminated:
            self.terminate()

    def terminate(self):
        self.is_terminated = True
        input('''
PRESS ENTER TO TERMINATE %s...
> ''' %self.name)
        
#===================================================================================
# Program Start
#===================================================================================

sh = Study_Helper()




