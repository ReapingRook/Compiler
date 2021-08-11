# Project 5
# Code gen
# COP4620
# Bryan Colon
# N01417983
# Date Due: 4/23/2020
# Date Submitted: 4/23/2020

import sys
import re

class Lexer:
    def __init__(self, fn):
        self.fn = fn
        self.fileLines = []
        self.comment_flag = False
        self.tokens = []
        self.keywords_checklist = ["else", "if", "int", "return", "void", "while", "float"]
        self.i = 0

        self.q = 1  
        self.t = 0  

        self.cur_f = 0 
        self.incur_f = 0 
        self.exp = 0

        self.listq = []
        self.listnum = 0
        self.iffr = []
        self.ifbk = []
        self.inifq = 0
        self.ifbr = 0
        self.elbr = 0

        self.d_check = 0
        self.wendbr = 0
        self.lastw = 0
        self.wlist = []  
        self.wnum = 0
        self.inwq = 0

    def get_file_lines(self):
        try:
            k = open(self.fn, "r")
            self.fileLines = k.read().splitlines()
            k.close()

        except IOError:
            print("Error: File does not appear to exist")

    def get_tokens(self):
        for line in self.fileLines:
            #if line != '':
                #print("INPUT: " + line)
            # Process comments
            line = self.process_comments(line)
            if self.comment_flag == False:
                # Extract tokens
                self.extract_tokens(line)

    def process_comments(self, line):
        if self.comment_flag == True:
            if "*/" in line:
                self.comment_flag = False
                # Get index at end of block comment
                comment_end_idx = line.find("*/") + 2 # offset by 2 to start at end of "*/" sequence
                line = line[comment_end_idx:]
                line = self.process_comments(line) # recursively call until end of comments
        else:
            if "/*" in line:
                self.comment_flag = True
                comment_begin_idx = line.find("/*") # find beginning of block comment
                self.extract_tokens(line[:comment_begin_idx])
                line = self.process_comments(line) # recursively call until end of comments
            elif "//":
                line = self.process_line_comments(line)
        return line

    def process_line_comments(self, line):
        comment_begin_idx = line.find("//") # find beginning of line comment
        if comment_begin_idx != -1:
            line = line[:comment_begin_idx]
        return line

    def extract_tokens(self, line):
        keywords = ["else", "if", "int", "return", "void", "while", "float"]
        # Initialize regular expressions
        s1 = "[a-zA-Z]+"
        s2 = "[0-9]+"
        s3 = "\/|\+|-|\*|<=|<|>=|>|==|!=|=|;|,|\(|\)|\{|\}|\[|\]"
        s4 = "(?:(?:@|!|_).*?[0-9]*(?=\\b))"
        s5 = "[@!_]+"        
        p = "(%s)|(%s)|(%s)|(%s)|(%s)" % (s1, s2, s3, s4, s5)
        for match in re.findall(p, line):
            if match[0]:
                if match[0] in keywords:
                    #print("KW: " + match[0])
                    self.tokens.append(match[0])
                else:
                    #print("ID: " + match[0])
                    self.tokens.append(match[0])
            elif match[1]:
                #print("INT: " + match[1])
                self.tokens.append(match[1])
            elif match[2]:
                #print(match[2])
                self.tokens.append(match[2])
            elif match[3]:
                #print("Error: " + match[3])
                self.tokens.append(match[3])
            elif match[4]:
                #print("Error: " + match[4])
                self.tokens.append(match[4])

    def watch_decent(self):
        check = self.tokens[self.i]
        #print(self.tokens[self.i])
        #print(self.i)

    def accept(self):
        self.i += 1

    def reject(self):
        print("REJECT")
        sys.exit()

    def number(self, numcheck):
        return any(char.isdigit() for char in numcheck)

    def is_rel(self, t):
        return t == "<=" or t == "<" or t == ">" or t == ">=" or t == "==" or t == "!="
    
    def is_multi(self, m):
        return m == "*" or m == "/"

    def is_add(self, m):
        return m == "+" or m == "-"

    def q_list(self):
        self.q += 1
        
    def not_rel(self, k):
        return self.tokens[k] != "<" and self.tokens[k] != "<=" and self.tokens[k] != ">" and self.tokens[k] != ">=" and self.tokens[k] != "==" and self.tokens[k] != "!="
    
    def check_re(self,token):
        return token.isalnum() or "[" in token or ("(" in token and ")" in token) or (re.search('[a-z]', token) == True and "(" in token) or token in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" or token in "0123456789" or token in "abcdefghijklmnopqrstuvwxyz"

    def numtype_check(self, num):
        return num == "int" or num == "float"
    
    def not_math(self, sym):
        return sym != "*" and sym != "/" and sym != "+" and sym != "-" and sym != "="

    def parr_part(self, x):
        f = x.partition('(')[-1].rpartition(')')[0]
        return f

    def par_part(self, x):
        f = x.partition('(')
        return f

    def cb_part(self, x):
        f = x.partition('[')
        return f

    def cbr_part(self, x):
        f = x.partition('[')[-1].rpartition(']')[0]
        return f

    def program(self): #1
        self.tokens.append("$")
        print("----------------------------------------------------")
        self.watch_decent()
        self.declaration_list()
        if self.tokens[self.i] == "$":
            finish = 1
        else:
            self.reject()

        print("----------------------------------------------------")
        
    def declaration_list(self): #2
        self.watch_decent()
        self.declaration()
        self.declaration_list_prime()

    def declaration_list_prime(self): #3
        self.watch_decent()
        if self.tokens[self.i] == "int" or self.tokens[self.i] == "float" or self.tokens[self.i] == "void":
            self.declaration()
            self.declaration_list_prime()
        elif self.tokens[self.i] == "$":
            return
        else:
            return    

    def declaration(self): #4
        self.watch_decent()
        self.type_specifier()
        letterchecker = self.tokens[self.i].isalpha()
        if self.tokens[self.i] not in self.keywords_checklist and letterchecker is True:
            self.accept()
            fp = []
            if self.tokens[self.i] == "main":
                print(str(self.q) + "    func         " + self.tokens[self.i-1] + "        void        0")
                self.q_list()
                self.cur_f = self.tokens[self.i-1]
            else:
                if self.tokens[self.i-2] == "void":
                    if self.tokens[self.i+1] == "void":
                        print(str(self.q) + "    func         " + self.tokens[self.i - 1] + "        void        0")
                        self.q_list()
                        self.cur_f = self.tokens[self.i - 1]
                    else:
                        k = self.i + 1
                        paramcount = 0
                        qu_check = self.q + 1
                        while self.tokens[k] != ")":
                            if self.numtype_check(self.tokens[k]) == True:
                                paramcount += 1
                                fp.append(str(qu_check) + "    param        4                       " + self.tokens[k + 1])
                                qu_check += 1
                                k += 2
                                if self.tokens[k] == ",":
                                    k += 1
                        print(str(self.q) + "    func         " + self.tokens[self.i - 1] + "        " + self.tokens[self.i - 2] + "        " + str(paramcount))
                        self.q = qu_check
                        for h in fp:
                            print(h)
                        self.cur_f = self.tokens[self.i - 1]
                else:
                    if self.tokens[self.i+1] == "void":
                        print(str(self.q) + "    func         " + self.tokens[self.i - 1] + "        void        0")
                        self.q_list()
                        self.cur_f = self.tokens[self.i - 1]
                    else:
                        k = self.i + 1
                        paramcount = 0
                        qu_check = self.q + 1
                        while self.tokens[k] != ")":
                            if self.numtype_check(self.tokens[k]) == True:
                                paramcount += 1
                                fp.append(str(qu_check) + "    param     4                       " + self.tokens[k + 1])
                                qu_check += 1
                                k += 2
                                if self.tokens[k] == ",":
                                    k += 1
                        print(str(self.q) + "    func         " + self.tokens[self.i - 1] + "        " + self.tokens[self.i - 2] + "        " + str(paramcount))
                        self.q = qu_check
                        for h in fp:
                            print(h)
                        self.cur_f = self.tokens[self.i - 1]

            if self.tokens[self.i] == ";":
                self.accept()

            elif self.tokens[self.i] == "[":
                self.accept()

                numchecker = self.number(self.tokens[self.i])
                if numchecker is True:
                    self.accept()
                    if self.tokens[self.i] == "]":
                        self.accept()
                        if self.tokens[self.i] == ";":
                            self.accept()
                        else:
                            self.reject()
                    else:
                        self.reject()
                else:
                    self.reject()
            elif self.tokens[self.i] == "(":
                self.accept()
                self.params()
                if self.tokens[self.i] == ")":
                    self.accept()
                    self.compound_stmt()
                else:
                    self.reject()
            else:
                self.reject()
        else:
            self.reject()

    def var_declaration(self): #5
        self.watch_decent()
        self.type_specifier()

        letterchecker = self.tokens[self.i].isalpha()
        if self.tokens[self.i] not in self.keywords_checklist and letterchecker is True:
            self.accept()

            if self.tokens[self.i] != "[":
                if self.inwq == 1:
                    self.wlist.append(str(self.q) + "    alloc        4                      " + self.tokens[self.i-1])
                    self.q_list()
                elif self.inifq == 1:
                    self.listq.append(str(self.q) + "    alloc        4                      " + self.tokens[self.i-1])
                    self.q_list()
                else:
                    print(str(self.q) + "    alloc        4                      " + self.tokens[self.i-1])
                    self.q_list()
        else:
            self.reject()

        if self.tokens[self.i] == ";":
            self.accept()
        elif self.tokens[self.i] == "[":
            self.accept()

            alloc = int(self.tokens[self.i]) * int(4)

            if self.inwq == 1:
                self.wlist.append(str(self.q) + "    alloc        " + str(alloc) + "                   " + self.tokens[self.i - 2])
                self.q_list()
            elif self.inifq == 1:
                self.listq.append(str(self.q) + "    alloc        "+ str(alloc) + "                  " + self.tokens[self.i - 2])
                self.q_list()
            else:
                print(str(self.q) + "    alloc        " + str(alloc) + "                   " + self.tokens[self.i - 1])
                self.q_list()

            letterchecker = self.number(self.tokens[self.i])
            if letterchecker is True:
                self.accept()
                if self.tokens[self.i] == "]":
                    self.accept()
                    if self.tokens[self.i] == ";":
                        self.accept()
                        return
                    else:
                        self.reject()
                else:
                    self.reject()
            else:
                self.reject()
        else:
            self.reject()

        
    #def var_declaration_prime(self):

    def type_specifier(self): #6
        self.watch_decent()
        if self.tokens[self.i] == "int" or self.tokens[self.i] == "void" or self.tokens[self.i] == "float":
            self.accept()
        else:
            return

    def fun_declaration(self): #7
        self.watch_decent()
        self.type_specifier()
        letterchecker = self.tokens[self.i].isalpha()
        if self.tokens[self.i] not in self.keywords_checklist and letterchecker is True:
            self.accept()
        else:
            return
        if self.tokens[self.i] == "(":
            self.accept()
        else:
            self.reject()
        self.params()
        if self.tokens[self.i] == ")":
            self.accept()
        else:
            self.reject()
        self.compound_stmt()

    def params(self): #8
        self.watch_decent()
        if self.tokens[self.i] == "int" or self.tokens[self.i] == "float" or self.tokens[self.i] == "void":
            self.param_list()
        else:
            self.reject()
    
    def param_list(self): #9
        self.watch_decent()
        self.param()
        self.param_list_prime()

    def param_list_prime(self): #10
        self.watch_decent()
        if self.tokens[self.i] == ",":
            self.accept()
            self.param()
            self.param_list_prime()
        elif self.tokens[self.i] == ")":
            return
        else:
            return

    def param(self): #11
        self.watch_decent()
        self.type_specifier()

        letterchecker = self.tokens[self.i].isalpha()
        if self.tokens[self.i] not in self.keywords_checklist and letterchecker is True:
            self.accept()
            if self.tokens[self.i] == "[":
                self.accept()
                if self.tokens[self.i] == "]":
                    self.accept()
                    return
                else:
                    self.reject()
        else:
            if self.tokens[self.i-1] == "void":
                return
            else:
                self.reject()

    #def param_prime(self):

    def compound_stmt(self): #12
        self.watch_decent()
        if self.tokens[self.i] == "{":
            self.accept()
            self.incur_f += 1

            if self.incur_f > 1:
                if self.inwq == 1:
                    self.wlist.append(str(self.q) + "    block                      ")
                    self.q_list()
                elif self.inifq == 1:
                    self.listq.append(str(self.q) + "    block                      ")
                    self.q_list()
                else:
                    print(str(self.q) + "    block                      ")
                    self.q_list()
        else:
            return
        
        self.local_delclarations()
        self.statement_list()

        if self.tokens[self.i] == "}":
            self.accept()

            self.incur_f -= 1
            if self.incur_f > 0:
                if self.inwq == 1:
                    self.wlist.append(str(self.q) + "    end           block        ")
                    self.q_list()
                elif self.inifq == 1:
                    self.listq.append(str(self.q) + "    end           block        ")
                    self.q_list()
                else:
                    print(str(self.q) + "    end           block        ")
                    self.q_list()

            if self.incur_f == 0:
                print(str(self.q) + "    end           func        " + self.cur_f)
                self.q_list()
        else:
            self.reject()

    def local_delclarations(self): #13
        self.watch_decent()
        self.local_delclarations_prime()

    def local_delclarations_prime(self): #14
        self.watch_decent()
        if self.tokens[self.i] == "int" or self.tokens[self.i] == "void" or self.tokens[self.i] == "float":
            self.var_declaration()
            self.local_delclarations_prime()
        else:
            return

    def statement_list(self): #15
        self.watch_decent()
        self.statement_list_prime()

    def statement_list_prime(self): #16
        self.watch_decent()
        letterchecker = self.tokens[self.i].isalpha()
        numchecker = self.number(self.tokens[self.i])
        if self.tokens[self.i] not in self.keywords_checklist and letterchecker is True:
            self.statement()
            self.statement_list_prime()
        elif numchecker is True:
            self.statement()
            self.statement_list_prime()
        elif self.tokens[self.i] == "(" or self.tokens[self.i] == ";" or self.tokens[self.i] == "{" or self.tokens[self.i] == "if" or self.tokens[self.i] == "while" or self.tokens[self.i] == "return":
            self.statement()
            self.statement_list_prime()
        elif self.tokens[self.i] == "}":
            return
        else:
            return

    def statement(self): #17
        self.watch_decent()
        letterchecker = self.tokens[self.i].isalpha()
        numchecker = self.number(self.tokens[self.i])
        if self.tokens[self.i] not in self.keywords_checklist and letterchecker is True:
            self.expression_stmt()
        elif numchecker is True:
            self.expression_stmt()
        elif self.tokens[self.i] == "(" or self.tokens[self.i] == ";":
            self.expression_stmt()
        elif self.tokens[self.i] == "{":
            self.compound_stmt()
        elif self.tokens[self.i] == "if":
            self.selection_stmt()
        elif self.tokens[self.i] == "while":
            self.iteration_stmt()
        elif self.tokens[self.i] == "return":
            self.return_stmt()
        else:
            self.reject()

    def expression_stmt(self): #18
        self.watch_decent()
        letterchecker = self.tokens[self.i].isalpha()
        numchecker = self.number(self.tokens[self.i])
        if self.tokens[self.i] not in self.keywords_checklist and letterchecker is True:
            self.expression()
            if self.tokens[self.i] == ";":
                self.accept()
            else:
                self.reject()
        elif numchecker is True:
            self.expression()
            if self.tokens[self.i] == ";":
                self.accept()
            else:
                self.reject()
        elif self.tokens[self.i] == "(":
            self.expression()
            if self.tokens[self.i] == ";":
                self.accept()
            else:
                self.reject()
        elif self.tokens[self.i] == ";":
            self.accept()
        else:
            self.reject()

    def selection_stmt(self): #19
        self.watch_decent()
        if self.tokens[self.i] == "if":
            self.accept()
        else:
            return

        if self.tokens[self.i] == "(":
            self.accept()

            k = self.i
            self.iffr = ""
            compar = 0
            back_check = 0
            while  self.not_rel(k) == True:
                if self.tokens[k] == "[" or back_check == 1:
                    self.iffr = self.iffr + self.tokens[k]
                    back_check = 1
                    if self.tokens[k] == "]":
                        back_check = 0
                else:
                    self.iffr = self.iffr + " " + self.tokens[k]
                k += 1

            compar = self.tokens[k]
            self.iffr = self.in_to_post(self.iffr)
            lastif = self.post_eval(self.iffr)

            k += 1
            back_check = 0
            self.ifbk = ""
            while self.tokens[k] != ")":
                if self.tokens[k] == "[" or back_check == 1:
                    self.ifbk = self.ifbk + self.tokens[k]
                    back_check = 1
                    if self.tokens[k] == "]":
                        back_check = 0
                else:
                    self.ifbk = self.ifbk + " " + self.tokens[k]
                k += 1

            self.ifbk = self.in_to_post(self.ifbk)
            lastif1 = self.post_eval(self.ifbk)

            print(str(self.q) + "    comp          " + lastif + "        " + lastif1 + "        t" + str(self.t))
            self.q_list()
            temp = "t" + str(self.t)
            self.t += 1

            if compar == ">":
                print(str(self.q) + "    BGT          " + temp + "                    " + str(self.q + 2))
                self.q_list()
            elif compar == ">=":
                print(str(self.q) + "    BGET          " + temp + "                    " + str(self.q + 2))
                self.q_list()
            elif compar == "<":
                print(str(self.q) + "    BLT          " + temp + "                    " + str(self.q + 2))
                self.q_list()
            elif compar == "<=":
                print(str(self.q) + "    BLET          " + temp + "                    " + str(self.q + 2))
                self.q_list()
            elif compar == "==":
                print(str(self.q) + "    BEQ          " + temp + "                    " + str(self.q + 2))
                self.q_list()
            else:  # comparison == "!="
                print(str(self.q) + "    BNEQ          " + temp + "                    " + str(self.q + 2))
                self.q_list()

            self.listq.append(str(self.q) + "    BR                                   ")
            self.q_list()

        else:
            self.reject()
        self.expression()
        if self.tokens[self.i] == ")":
            self.accept()
        else:
            self.reject()

        self.statement()

        if self.tokens[self.i] == "else":
            self.listq[self.listnum] = self.listq[self.listnum] + str(self.q + 1)
        else:
            self.listq[self.listnum] = self.listq[self.listnum] + str(self.q)
        elsech = 0

        for h in self.listq:
            print(h)
        self.inifq = 0

        if self.tokens[self.i] == "else":
            self.accept()

            self.listq.append(str(self.q) + "    BR                                   ")
            elsech = len(self.listq)
            self.q_list()
            self.inifq = 1

            self.statement()

            self.listq[elsech - 1] = self.listq[elsech - 1] + str(self.q)

            for h in range(elsech - 1, len(self.listq)):
                print(self.listq[h])
            self.inifq = 0

        else:
            return

    #def selection_stmt_prime(self):

    def iteration_stmt(self): #20
        self.watch_decent()
        if self.tokens[self.i] == "while":
            self.accept()
        else:
            return
        if self.tokens[self.i] == "(":
            self.accept()

            self.wendbr = self.q  # get start of while loop line for last quadruple in the block

            k = self.i
            wlistfront = ""
            compar = 0
            back_check = 0
            while  self.not_rel(k) == True:
                if self.tokens[k] == "[" or back_check == 1:
                    wlistfront = wlistfront + self.tokens[k]
                    back_check = 1
                    if self.tokens[k] == "]":
                        back_check = 0
                else:
                    wlistfront = wlistfront + " " + self.tokens[k]
                k += 1

            compar = self.tokens[k]
            wlistfront = self.in_to_post(wlistfront)
            self.lastw = self.post_eval(wlistfront)

            k += 1
            back_check = 0
            wlistback = ""
            while self.tokens[k] != ")":
                if self.tokens[k] == "[" or back_check == 1:
                    wlistback = wlistback + self.tokens[k]
                    back_check = 1
                    if self.tokens[k] == "]":
                        back_check = 0
                else:
                    wlistback = wlistback + " " + self.tokens[k]
                k += 1

            wlistback = self.in_to_post(wlistback)
            lastw1 = self.post_eval(wlistback)

            if self.inwq == 1:
                self.wlist.append(str(self.q) + "    comp         " + self.lastw + "        " + lastw1 + "        t" + str(self.t))
            else:
                print(str(self.q) + "    comp         " + self.lastw + "        " + lastw1 + "        t" + str(self.t))
            self.q_list()
            temp = "t" + str(self.t)
            self.t += 1

            if compar == ">":
                if self.inwq == 1:
                    self.wlist.append(str(self.q) + "    BGT         " + temp + "                    " + str(self.q + 2))
                else:
                    print(str(self.q) + "    BGT         " + temp + "                    " + str(self.q + 2))
                self.q_list()
            elif compar == ">=":
                if self.inwq == 1:
                    self.wlist.append(str(self.q) + "    BGET         " + temp + "                    " + str(self.q + 2))
                else:
                    print(str(self.q) + "    BGET         " + temp + "                    " + str(self.q + 2))
                self.q_list()
            elif compar == "<":
                if self.inwq == 1:
                    self.wlist.append(str(self.q) + "    BLT         " + temp + "                    " + str(self.q + 2))
                else:
                    print(str(self.q) + "    BLT         " + temp + "                    " + str(self.q + 2))
                self.q_list()
            elif compar == "<=":
                if self.inwq == 1:
                    self.wlist.append(str(self.q) + "    BLET         " + temp + "                    " + str(self.q + 2))
                else:
                    print(str(self.q) + "    BLET         " + temp + "                    " + str(self.q + 2))
                self.q_list()
            elif compar == "==":
                if self.inwq == 1:
                    self.wlist.append(str(self.q) + "    BEQ         " + temp + "                    " + str(self.q + 2))
                else:
                    print(str(self.q) + "    BEQ         " + temp + "                    " + str(self.q + 2))
                self.q_list()
            else:  # comparison == "!="
                if self.inwq == 1:
                    self.wlist.append(str(self.q) + "    BNEQ         " + temp + "                    " + str(self.q + 2))
                else:
                    print(str(self.q) + "    BNEQ         " + temp + "                    " + str(self.q + 2))
                self.q_list()

            self.wlist.append(str(self.q) + "    BR                                   ")
            self.q_list()

        else:
            self.reject()

        self.expression()

        if self.tokens[self.i] == ")":
            self.accept()
        else:
            self.reject()

        self.inwq = 1
        self.d_check += 1

        self.statement()
        self.d_check -= 1

        self.wlist[self.wnum] = self.wlist[self.wnum] + str(self.q + 1) + "h"
        self.inwq = 0

        if self.d_check == 0:
            for h in self.wlist:
                print(h)

        if self.inwq == 1:
            self.wlist.append(str(self.q) + "    BR                                      " + str(self.wendbr))
        else:
            print(str(self.q) + "    BR                                      " + str(self.wendbr))
        self.q_list()


    def return_stmt(self): #21
        self.watch_decent()
        if self.tokens[self.i] == "return":
            self.accept()
        else:
            return
        letterchecker = self.tokens[self.i].isalpha()
        numchecker = self.number(self.tokens[self.i])
        if self.tokens[self.i] == ";":
            self.accept()

            print(str(self.q) + "    return                        ")
            self.q_list()
            return

        elif self.tokens[self.i] not in self.keywords_checklist and letterchecker is True:

            if self.tokens[self.i + 1] == "[":
                k = self.i
                return_e = ""
                while self.tokens[k] != ";":
                    return_e = return_e + self.tokens[k]
                    k += 1

                c1 = self.cb_part(return_e)
                c2 = self.cbr_part(return_e)
                if self.number(c2) == False:
                    print(str(self.q) + "    mult         " + c2 + "        4          t" + str(self.t))
                    self.q_list()
                    temp = "t" + str(self.t)
                    self.t += 1
                    c2 = temp
                else:
                    c2 = int(c2) * 4
                print(str(self.q) + "    disp         " + c1[0] + "        " + str(c2) + "        t" + str(self.t))
                self.q_list()
                temp = "t" + str(self.t)
                self.t += 1

                print(str(self.q) + "    return                               " + temp)
                self.q_list()

            else:
                print(str(self.q) + "    return                               " + self.tokens[self.i])
                self.q_list()

            self.expression()

            if self.tokens[self.i] == ";":
                self.accept()
                return
            else:
                self.reject()
        elif numchecker is True:
            print(str(self.q) + "    return                               " + self.tokens[self.i])
            self.q_list()

            self.expression()
            if self.tokens[self.i] == ";":
                self.accept()
                return
            else:
                self.reject()
        elif self.tokens[self.i] == "(":

            k = self.i + 1
            back_check = 0
            expret = ""
            while self.tokens[k] != ")":
                if self.tokens[k] == "[" or back_check == 1:
                    expret = expret + self.tokens[k]
                    back_check = 1
                    if self.tokens[k] == "]":
                        back_check = 0
                else:
                    expret = expret + " " + self.tokens[k]
                k += 1

            expret = self.in_to_post(expret)
            lastexpret = self.post_eval(expret)

            print(str(self.q) + "    return                               " + lastexpret)
            self.q_list()

            self.expression()
            if self.tokens[self.i] == ";":
                self.accept()
                return
            else:
                self.reject()
        else:
            self.reject()


    def expression(self): #22
        self.watch_decent()
        letterchecker = self.tokens[self.i].isalpha()
        numchecker = self.number(self.tokens[self.i])
        if self.tokens[self.i] not in self.keywords_checklist and letterchecker is True:
            self.accept()

            if self.tokens[self.i] == "[" and self.exp == 0:
                k = self.i - 1
                check = ""
                while self.tokens[k] != "=":
                    check = check + self.tokens[k]
                    k += 1
                self.i = k
                assign = check

                if self.inwq == 1:
                    c1 = self.cb_part(assign)
                    c2 = self.cbr_part(assign)
                    if self.number(c2) == False:
                        self.wlist.append(str(self.q) + "    mult         " + c2 + "        4           t" + str(self.t))
                        self.q_list()
                        temp = "t" + str(self.t)
                        self.t += 1
                        c2 = temp
                    else:
                        c2 = int(c2) * 4
                    self.wlist.append(str(self.q) + "    disp         " + c1[0] + "        " + str(c2) + "        t" + str(self.t))
                    self.q_list()
                    temp = "t" + str(self.t)
                    self.t += 1
                    assign = temp

                elif self.inifq == 1:
                    c1 = self.cb_part(assign)
                    c2 = self.cbr_part(assign)
                    if self.number(c2) == False:
                        self.listq.append(str(self.q) + "    mult         " + c2 + "        4           t" + str(self.t))
                        self.q_list()
                        temp = "t" + str(self.t)
                        self.t += 1
                        c2 = temp
                    else:
                        c2 = int(c2) * 4
                    self.listq.append(str(self.q) + "    disp         " + c1[0] + "        " + str(c2) + "        t" + str(self.t))
                    self.q_list()
                    temp = "t" + str(self.t)
                    self.t += 1
                    assign = temp

                else:
                    c1 = self.cb_part(assign)
                    c2 = self.cbr_part(assign)
                    if self.number(c2) == False:
                        print(str(self.q) + "    mult         " + c2 + "     4           t" + str(self.t))
                        self.q_list()
                        temp = "t" + str(self.t)
                        self.t += 1
                        c2 = temp
                    else:
                        c2 = int(c2) * 4
                    print(str(self.q) + "    disp         " + c1[0] + "        " + str(c2) + "        t" + str(self.t))
                    self.q_list()
                    temp = "t" + str(self.t)
                    self.t += 1
                    assign = temp

            else:
                assign = self.tokens[self.i - 1]

            if self.tokens[self.i] == "(" and self.exp == 0:
                k = self.i
                exquad = self.tokens[self.i - 1]
                while self.tokens[k] != ";":
                    exquad = exquad + self.tokens[k]
                    k += 1

                if self.inwq == 1:
                    pc = 0
                    c1 = self.parr_part(exquad)
                    c2 = self.par_part(exquad)
                    if ',' in c1:
                        c1 = c1.split(',')
                    for h in c1:
                        pc += 1
                        self.wlist.append(str(self.q) + "    arg                                  " + h)
                        self.q_list()

                    self.wlist.append(str(self.q) + "    call         " + c2[0] + "        " + str(pc) + "        t" + str(self.t))
                    self.q_list()
                    self.t += 1

                elif self.inifq == 1:
                    pc = 0
                    c1 = self.parr_part(exquad)
                    c2 = self.par_part(exquad)
                    if ',' in c1:
                        c1 = c1.split(',')
                    for h in c1:
                        pc += 1
                        self.listq.append(str(self.q) + "    arg                                  " + h)
                        self.q_list()

                    self.listq.append(str(self.q) + "    call         " + c2[0] + "        " + str(pc) + "        t" + str(self.t))
                    self.q_list()
                    self.t += 1

                else:
                    pc = 0
                    c1 = self.parr_part(exquad)
                    c2 = self.par_part(exquad)
                    if ',' in c1:
                        c1 = c1.split(',')
                    for h in c1:
                        pc += 1
                        print(str(self.q) + "    arg                                  " + h)
                        self.q_list()

                    print(str(self.q) + "    call         " + c2[0] + "        " + str(pc) + "        t" + str(self.t))
                    self.q_list()
                    self.t += 1

            if self.tokens[self.i] == "=":
                k = self.i + 1
                exquad = ""
                back_check = 0
                pch = 0
                while self.tokens[k] != ";":
                    if self.tokens[k] == "[" or back_check == 1:
                        exquad = exquad + self.tokens[k]
                        back_check = 1
                        if self.tokens[k] == "]":
                            back_check = 0
                    elif self.tokens[k] == "(" or pch == 1:
                        if self.not_math(self.tokens[k - 1]) == True:
                            exquad = exquad + self.tokens[k]
                            pch = 1
                            if self.tokens[k] == ")":
                                pch = 0
                        else:
                            exquad = exquad + " " + self.tokens[k]
                    else:
                        exquad = exquad + " " + self.tokens[k]
                    k += 1
                exquad = self.in_to_post(exquad)
                last_e = self.post_eval(exquad)

                if self.inwq == 1:
                    if "(" in last_e:
                        pc = 0
                        c1 = self.parr_part(last_e)
                        c2 = self.par_part(last_e)
                        if ',' in c1:
                            c1 = c1.split(',')
                        for h in c1:
                            pc += 1
                            self.wlist.append(str(self.q) + "    arg                                  " + h)
                            self.q_list()

                        self.wlist.append(str(self.q) + "    call         " + c2[0] + "        " + str(pc) + "        t" + str(self.t))
                        self.q_list()
                        temp = "t" + str(self.t)
                        self.t += 1
                        self.wlist.append(str(self.q) + "    assgn        " + temp + "                    " + str(assign))
                        self.q_list()
                        self.exp = 1

                    elif "[" in last_e:
                        c1 = self.cb_part(last_e)
                        c2 = self.cbr_part(last_e)
                        if self.number(c2) == False:
                            self.wlist.append(str(self.q) + "    mult         " + c2 + "        4            t" + str(self.t))
                            self.q_list()
                            temp = "t" + str(self.t)
                            self.t += 1
                            c2 = temp
                        else:
                            c2 = int(c2) * 4
                        self.wlist.append(str(self.q) + "    disp         " + c1[0] + "        " + str(c2) + "        t" + str(self.t))
                        self.q_list()
                        temp = "t" + str(self.t)
                        self.t += 1

                        self.wlist.append(str(self.q) + "    assgn         " + temp + "                    " + str(assign))
                        self.q_list()
                        self.exp = 1

                    else:
                        self.wlist.append(str(self.q) + "    assgn         " + last_e + "                    " + str(assign))
                        self.q_list()
                        self.exp = 1

                elif self.inifq == 1:
                    if "(" in last_e:
                        pc = 0
                        c1 = self.parr_part(last_e)
                        c2 = self.par_part(last_e)
                        if ',' in c1:
                            c1 = c1.split(',')
                        for h in c1:
                            pc += 1
                            self.listq.append(str(self.q) + "    arg                                  " + h)
                            self.q_list()

                        self.listq.append(str(self.q) + "    call         " + c2[0] + "        " + str(pc) + "        t" + str(self.t))
                        self.q_list()
                        temp = "t" + str(self.t)
                        self.t += 1
                        self.listq.append(str(self.q) + "    assgn        " + temp + "                    " + str(assign))
                        self.q_list()
                        self.exp = 1

                    elif "[" in last_e:
                        c1 = self.cb_part(last_e)
                        c2 = self.cbr_part(last_e)
                        if self.number(c2) == False:
                            self.listq.append(str(self.q) + "    mult         " + c2 + "        4           t" + str(self.t))
                            self.q_list()
                            temp = "t" + str(self.t)
                            self.t += 1
                            c2 = temp
                        else:
                            c2 = int(c2) * 4
                        self.listq.append(str(self.q) + "    disp         " + c1[0] + "        " + str(c2) + "        t" + str(self.t))
                        self.q_list()
                        temp = "t" + str(self.t)
                        self.t += 1

                        self.listq.append(str(self.q) + "    assgn        " + temp + "                    " + str(assign))
                        self.q_list()
                        self.exp = 1

                    else:
                        self.listq.append(str(self.q) + "    assgn        " + last_e + "                    " + str(assign))
                        self.q_list()
                        self.exp = 1

                else:
                    if "(" in last_e:
                        pc = 0
                        c1 = self.parr_part(last_e)
                        c2 = self.par_part(last_e)
                        if ',' in c1:
                            c1 = c1.split(',')
                        for h in c1:
                            pc += 1
                            print(str(self.q) + "    arg                                  " + h)
                            self.q_list()

                        print(str(self.q) + "    call         " + c2[0] + "        " + str(pc) + "        t" + str(self.t))
                        self.q_list()
                        temp = "t" + str(self.t)
                        self.t += 1
                        print(str(self.q) + "    assgn        " + temp + "                    " + str(assign))
                        self.q_list()
                        self.exp = 1

                    elif "[" in last_e:
                        c1 = self.cb_part(last_e)
                        c2 = self.cbr_part(last_e)
                        if self.number(c2) == False:
                            print(str(self.q) + "    mult         " + c2 + "        4           t" + str(self.t))
                            self.q_list()
                            temp = "t" + str(self.t)
                            self.t += 1
                            c2 = temp
                        else:
                            c2 = int(c2) * 4
                        print(str(self.q) + "    disp         " + c1[0] + "        " + str(c2) + "        t" + str(self.t))
                        self.q_list()
                        temp = "t" + str(self.t)
                        self.t += 1

                        print(str(self.q) + "    assgn        " + temp + "                    " + str(assign))
                        self.q_list()
                        self.exp = 1

                    else:
                        print(str(self.q) + "    assgn  " + last_e + "                    " + str(assign))
                        self.q_list()
                        self.exp = 1

            self.expression_prime()
            self.exp = 0


        elif self.tokens[self.i] == "(":
            self.accept()
            self.expression()
            if self.tokens[self.i] == ")":
                self.accept()
                self.term_prime()
                self.additive_expression_prime()
                if self.is_rel(self.tokens[self.i]) is True:
                    self.relop()
                    self.additive_expression()
                elif self.is_add(self.tokens[self.i]) is True:
                    self.additive_expression_prime()
                    if self.is_rel(self.tokens[self.i]) is True:
                        self.relop()
                        self.additive_expression()
                elif self.is_rel(self.tokens[self.i]) is True:
                    self.relop()
                    self.additive_expression()
                else:
                    return
            else:
                self.reject()
        elif numchecker is True:
            self.accept()

            self.term_prime()
            self.additive_expression_prime()
            if self.is_rel(self.tokens[self.i]) is True:
                self.relop()
                self.additive_expression()
            elif self.is_add(self.tokens[self.i]) is True:
                self.additive_expression_prime()
                if self.is_rel(self.tokens[self.i]) is True:
                    self.relop()
                    self.additive_expression()
            elif self.is_rel(self.tokens[self.i]) is True:
                self.relop()
                self.additive_expression()
            else:
                return
        else:
            self.reject()

    def expression_prime(self): #23
        self.watch_decent()
        if self.tokens[self.i] == "=":
            self.accept()
            self.expression()
        elif self.tokens[self.i] == "[":
            self.accept()
            self.expression()
            if self.tokens[self.i - 1] == "[":
                self.reject()
            if self.tokens[self.i] == "]":
                self.accept()
                if self.tokens[self.i] == "=":
                    self.accept()
                    self.expression()
                elif self.is_multi(self.tokens[self.i]) is True:
                    self.term_prime()
                    self.additive_expression_prime()
                    if self.tokens[self.i] == "<=" or self.tokens[self.i] == ">" or self.tokens[self.i] == ">=" or self.tokens[self.i] == "==" or self.tokens[self.i] == "!=":
                        self.relop()
                        self.additive_expression()
                    else:
                        return
                elif self.is_add(self.tokens[self.i]) is True:
                    self.additive_expression_prime()
                    if self.tokens[self.i] == "<=" or self.tokens[self.i] == ">" or self.tokens[self.i] == ">=" or self.tokens[self.i] == "==" or self.tokens[self.i] == "!=":
                        self.relop()
                        self.additive_expression()
                elif self.tokens[self.i] == "<=" or self.tokens[self.i] == ">" or self.tokens[self.i] == ">=" or self.tokens[self.i] == "==" or self.tokens[self.i] == "!=":
                    self.relop()
                    self.additive_expression()
                else:
                    return
            else:
                self.reject()
        elif self.tokens[self.i] == "(":
            self.accept()
            self.args()
            if self.tokens[self.i] == ")":
                self.accept()
                if self.is_multi(self.tokens[self.i]) is True:
                    self.term_prime()
                    self.additive_expression_prime()
                    if self.is_rel(self.tokens[self.i]) is True:
                        self.relop()
                        self.additive_expression()
                    else:
                        return
                elif self.is_add(self.tokens[self.i]) is True:
                    self.additive_expression_prime()
                    if self.is_rel(self.tokens[self.i]) is True:
                        self.relop()
                        self.additive_expression()
                elif self.is_rel(self.tokens[self.i]) is True:
                    self.relop()
                    self.additive_expression()
                else:
                    return
            else:
                self.reject()
        elif self.is_multi(self.tokens[self.i]) is True:
            self.term_prime()
            self.additive_expression_prime()
            if self.is_rel(self.tokens[self.i]) is True:
                self.relop()
                self.additive_expression()
            else:
                return
        elif self.is_add(self.tokens[self.i]) is True:
            self.additive_expression_prime()
            if self.is_rel(self.tokens[self.i]) is True:
                self.relop()
                self.additive_expression()
            else:
                return
        elif self.is_rel(self.tokens[self.i]) is True:
            self.relop()
            self.additive_expression()
        else:
            return

    def var(self): #24
        self.watch_decent()
        letterchecker = self.tokens[self.i].isalpha()

        if self.tokens[self.i] not in self.keywords_checklist and letterchecker is True:
            self.accept()
        else:
            return
        if self.tokens == "[":
            self.accept()
            self.expression()
            if self.tokens[self.i] == "]":
                self.accept()
            else:
                self.reject()
        else:
            return

    def simple_expression(self): #25
        self.watch_decent()
        self.additive_expression()
        if self.is_rel(self.tokens[self.i]):
            self.relop()
            self.additive_expression()
        else:
            return

    def relop(self): #26
        self.watch_decent()
        if self.is_rel(self.tokens[self.i]) is True:
            self.accept()
        else:
            return

    def additive_expression(self): #27
        self.watch_decent()
        self.term()
        self.additive_expression_prime()

    def additive_expression_prime(self): #28
        self.watch_decent()
        if self.is_add(self.tokens[self.i]) is True:
            self.addop()
            self.term()
            self.additive_expression_prime()
        else:
            return

    def addop(self): #29
        self.watch_decent()
        if self.is_add(self.tokens[self.i]) is True:
            self.accept()
        else:
            return

    def term(self): #30
        self.watch_decent()
        self.factor()
        self.term_prime()

    def term_prime(self): #31
        self.watch_decent()
        if self.is_multi(self.tokens[self.i]) is True:
            self.mulop()
            self.factor()
            self.term_prime()
        else:
            return

    def mulop(self): #32
        self.watch_decent()
        if self.is_multi(self.tokens[self.i]) is True:
            self.accept()
        else:
            return

    def factor(self): #33
        letterchecker = self.tokens[self.i].isalpha()
        numchecker = self.number(self.tokens[self.i])

        if self.tokens[self.i] not in self.keywords_checklist and letterchecker is True:
            self.accept()

            if self.tokens[self.i] == "[":
                self.accept()
                self.expression()
                if self.tokens[self.i] == "]":
                    self.accept()
                else:
                    return
            elif self.tokens[self.i] == "(":
                self.accept()
                self.args()
                if self.tokens[self.i] == ")":
                    self.accept()
                else:
                    return
            else:
                return
        elif numchecker is True:
            self.accept()
        elif self.tokens[self.i] == "(":
            self.accept()
            self.expression()
            if self.tokens[self.i] == ")":
                self.accept()
            else:
                return
        else:
            self.reject()

    def call(self): #34
        letterchecker = self.tokens[self.i].isalpha()
        if self.tokens[self.i] not in self.keywords_checklist and letterchecker is True:
            self.accept() 
            if self.tokens[self.i] == "(":
                self.accept()
                self.args()
                if self.tokens[self.i] == ")":
                    self.accept()
                else:
                    self.reject()
            else:
                self.reject()
        else:
            return

    def args(self): #35
        letterchecker = self.tokens[self.i].isalpha()
        numchecker = self.number(self.tokens[self.i])

        if self.tokens[self.i] not in self.keywords_checklist and letterchecker is True:
            self.arg_list()
        elif numchecker is True:
            self.arg_list()
        elif self.tokens[self.i] == "(":
            self.arg_list()
        elif self.tokens[self.i] == ")":
            return
        else:
            return

    def arg_list(self): #36
        self.expression()
        self.arg_list_prime()

    def arg_list_prime(self): #37
        if self.tokens[self.i] == ",":
            self.accept()
            self.expression()
            self.arg_list_prime()
        elif self.tokens[self.i] == ")":
            return
        else:
            return



    def in_to_post(self, ine):
        precedence = {}
        precedence["*"] = 3
        precedence["/"] = 3
        precedence["+"] = 2
        precedence["-"] = 2
        precedence["("] = 1
        ost = Stack()
        post_li = []
        tokenList = ine.split()

        for token in tokenList:
            if self.check_re(token) == True:
                post_li.append(token)
            elif token == '(':
                ost.push(token)
            elif token == ')':
                top = ost.pop()
                while top != '(':
                    post_li.append(top)
                    top = ost.pop()
            else:
                while (not ost.isEmpty()) and \
                   (precedence[ost.peek()] >= precedence[token]):
                      post_li.append(ost.pop())
                ost.push(token)

        while not ost.isEmpty():
            post_li.append(ost.pop())
        return " ".join(post_li)


    def post_eval(self, poe):
        op_prStack = Stack()
        tokenList = poe.split()

        for token in tokenList:
            if self.check_re(token) == True:
                op_prStack.push(token)
            else:
                op_pr2 = op_prStack.pop()
                op_pr1 = op_prStack.pop()
                result = self.op_math(token,op_pr1,op_pr2)
                op_prStack.push(result)
        return op_prStack.pop()

    def op_math(self, m, x, y):

        if m == "*":
            if self.inwq == 1:
                if "(" in x:
                        pc = 0
                        c1 = self.parr_part(x)
                        c2 = self.par_part(x)
                        if ',' in c1:
                            c1 = c1.split(',')
                        for h in c1:
                            pc += 1
                            self.wlist.append(str(self.q) + "    arg                                 " + h)
                            self.q_list()

                        self.wlist.append(str(self.q) + "    call         " + c2[0] + "        " + str(pc) + "        t" + str(self.t))
                        self.q_list()
                        temp = "t" + str(self.t)
                        self.t += 1
                        x = temp

                if "(" in y:
                        pc = 0
                        c1 = self.parr_part(y)
                        c2 = self.par_part(y)
                        if ',' in c1:
                            c1 = c1.split(',')
                        for h in c1:
                            pc += 1
                            self.wlist.append(str(self.q) + "    arg                                 " + h)
                            self.q_list()

                        self.wlist.append(str(self.q) + "    call         " + c2[0] + "        " + str(pc) + "        t" + str(self.t))
                        self.q_list()
                        temp = "t" + str(self.t)
                        self.t += 1
                        y = temp

                if "[" in x:
                    c1 = self.cb_part(x)
                    c2 = self.cbr_part(x)
                    if self.number(c2) == False:
                        self.wlist.append(str(self.q) + "    mult         " + c2 + "        4           t" + str(self.t))
                        self.q_list()
                        temp = "t" + str(self.t)
                        self.t += 1
                        c2 = temp
                    else:
                        c2 = int(c2) * 4
                    self.wlist.append(str(self.q) + "    disp         " + c1[0] + "        " + str(c2) + "        t" + str(self.t))
                    self.q_list()
                    temp = "t" + str(self.t)
                    self.t += 1
                    x = temp

                if "[" in y:
                    c1 = self.cb_part(y)
                    c2 = self.cbr_part(y)
                    if self.number(c2) == False:
                        self.wlist.append(str(self.q) + "    mult         " + c2 + "        4           t" + str(self.t))
                        self.q_list()
                        temp = "t" + str(self.t)
                        self.t += 1
                        c2 = temp
                    else:
                        c2 = int(c2) * 4
                    self.wlist.append(str(self.q) + "    disp         " + c1[0] + "        " + str(c2) + "        t" + str(self.t))
                    self.q_list()
                    temp = "t" + str(self.t)
                    self.t += 1
                    y = temp
                self.wlist.append(str(self.q) + "    mult         " + x + "        " + y + "        t" + str(self.t))

            elif self.inifq == 1:
                if "(" in x:
                        pc = 0
                        c1 = self.parr_part(x)
                        c2 = self.par_part(x)
                        if ',' in c1:
                            c1 = c1.split(',')
                        for h in c1:
                            pc += 1
                            self.listq.append(str(self.q) + "    arg                                 " + h)
                            self.q_list()

                        self.listq.append(str(self.q) + "    call         " + c2[0] + "        " + str(pc) + "        t" + str(self.t))
                        self.q_list()
                        temp = "t" + str(self.t)
                        self.t += 1
                        x = temp

                if "(" in y:
                        pc = 0
                        c1 = self.parr_part(y)
                        c2 = self.par_part(y)
                        if ',' in c1:
                            c1 = c1.split(',')
                        for h in c1:
                            pc += 1
                            self.listq.append(str(self.q) + "    arg                                 " + h)
                            self.q_list()

                        self.listq.append(str(self.q) + "    call         " + c2[0] + "        " + str(pc) + "        t" + str(self.t))
                        self.q_list()
                        temp = "t" + str(self.t)
                        self.t += 1
                        y = temp

                if "[" in x:
                    c1 = self.cb_part(x)
                    c2 = self.cbr_part(x)
                    if self.number(c2) == False:
                        self.listq.append(str(self.q) + "    mult         " + c2 + "        4           t" + str(self.t))
                        self.q_list()
                        temp = "t" + str(self.t)
                        self.t += 1
                        c2 = temp
                    else:
                        c2 = int(c2) * 4
                    self.listq.append(str(self.q) + "    disp         " + c1[0] + "        " + str(c2) + "        t" + str(self.t))
                    self.q_list()
                    temp = "t" + str(self.t)
                    self.t += 1
                    x = temp

                if "[" in y:
                    c1 = self.cb_part(y)
                    c2 = self.cbr_part(y)
                    if self.number(c2) == False:
                        self.listq.append(str(self.q) + "    mult         " + c2 + "        4           t" + str(self.t))
                        self.q_list()
                        temp = "t" + str(self.t)
                        self.t += 1
                        c2 = temp
                    else:
                        c2 = int(c2) * 4
                    self.listq.append(str(self.q) + "    disp         " + c1[0] + "        " + str(c2) + "        t" + str(self.t))
                    self.q_list()
                    temp = "t" + str(self.t)
                    self.t += 1
                    y = temp
                self.listq.append(str(self.q) + "    mult         " + x + "        " + y + "        t" + str(self.t))

            else:
                if "(" in x:
                        pc = 0
                        c1 = self.parr_part(x)
                        c2 = self.par_part(x)
                        if ',' in c1:
                            c1 = c1.split(',')
                        for h in c1:
                            pc += 1
                            print(str(self.q) + "    arg                                 " + h)
                            self.q_list()

                        print(str(self.q) + "    call         " + c2[0] + "        " + str(pc) + "        t" + str(self.t))
                        self.q_list()
                        temp = "t" + str(self.t)
                        self.t += 1
                        x = temp

                if "(" in y:
                        pc = 0
                        c1 = self.parr_part(y)
                        c2 = self.par_part(y)
                        if ',' in c1:
                            c1 = c1.split(',')
                        for h in c1:
                            pc += 1
                            print(str(self.q) + "    arg                                 " + h)
                            self.q_list()

                        print(str(self.q) + "    call         " + c2[0] + "        " + str(pc) + "        t" + str(self.t))
                        self.q_list()
                        temp = "t" + str(self.t)
                        self.t += 1
                        y = temp

                if "[" in x:
                    c1 = self.cb_part(x)
                    c2 = self.cbr_part(x)
                    if self.number(c2) == False:
                        print(str(self.q) + "    mult         " + c2 + "        4           t" + str(self.t))
                        self.q_list()
                        temp = "t" + str(self.t)
                        self.t += 1
                        c2 = temp
                    else:
                        c2 = int(c2) * 4
                    print(str(self.q) + "    disp         " + c1[0] + "        " + str(c2) + "        t" + str(self.t))
                    self.q_list()
                    temp = "t" + str(self.t)
                    self.t += 1
                    x = temp

                if "[" in y:
                    c1 = self.cb_part(y)
                    c2 = self.cbr_part(y)
                    if self.number(c2) == False:
                        print(str(self.q) + "    mult         " + c2 + "        4           t" + str(self.t))
                        self.q_list()
                        temp = "t" + str(self.t)
                        self.t += 1
                        c2 = temp
                    else:
                        c2 = int(c2) * 4
                    print(str(self.q) + "    disp         " + c1[0] + "        " + str(c2) + "        t" + str(self.t))
                    self.q_list()
                    temp = "t" + str(self.t)
                    self.t += 1
                    y = temp
                print(str(self.q) + "    mult         " + x + "        " + y + "        t" + str(self.t))
            self.q_list()
            temp = "t" + str(self.t)
            self.t += 1
            return temp

        elif m == "/":
            if self.inwq == 1:
                if "(" in x:
                        pc = 0
                        c1 = self.parr_part(x)
                        c2 = self.par_part(x)
                        if ',' in c1:
                            c1 = c1.split(',')
                        for h in c1:
                            pc += 1
                            self.wlist.append(str(self.q) + "    arg                                 " + h)
                            self.q_list()

                        self.wlist.append(str(self.q) + "    call         " + c2[0] + "        " + str(pc) + "        t" + str(self.t))
                        self.q_list()
                        temp = "t" + str(self.t)
                        self.t += 1
                        x = temp

                if "(" in y:
                        pc = 0
                        c1 = self.parr_part(y)
                        c2 = self.par_part(y)
                        if ',' in c1:
                            c1 = c1.split(',')
                        for h in c1:
                            pc += 1
                            self.wlist.append(str(self.q) + "    arg                                 " + h)
                            self.q_list()

                        self.wlist.append(str(self.q) + "    call         " + c2[0] + "        " + str(pc) + "        t" + str(self.t))
                        self.q_list()
                        temp = "t" + str(self.t)
                        self.t += 1
                        y = temp

                if "[" in x:
                    c1 = self.cb_part(x)
                    c2 = self.cbr_part(x)
                    if self.number(c2) == False:
                        self.wlist.append(str(self.q) + "    mult         " + c2 + "        4           t" + str(self.t))
                        self.q_list()
                        temp = "t" + str(self.t)
                        self.t += 1
                        c2 = temp
                    else:
                        c2 = int(c2) * 4
                    self.wlist.append(str(self.q) + "    disp         " + c1[0] + "        " + str(c2) + "        t" + str(self.t))
                    self.q_list()
                    temp = "t" + str(self.t)
                    self.t += 1
                    x = temp

                if "[" in y:
                    c1 = self.cb_part(y)
                    c2 = self.cbr_part(y)
                    if self.number(c2) == False:
                        self.wlist.append(str(self.q) + "    mult         " + c2 + "        4           t" + str(self.t))
                        self.q_list()
                        temp = "t" + str(self.t)
                        self.t += 1
                        c2 = temp
                    else:
                        c2 = int(c2) * 4
                    self.wlist.append(str(self.q) + "    disp         " + c1[0] + "        " + str(c2) + "        t" + str(self.t))
                    self.q_list()
                    temp = "t" + str(self.t)
                    self.t += 1
                    y = temp
                self.wlist.append(str(self.q) + "    div          " + x + "        " + y + "        t" + str(self.t))

            elif self.inifq == 1:
                if "(" in x:
                        pc = 0
                        c1 = self.parr_part(x)
                        c2 = self.par_part(x)
                        if ',' in c1:
                            c1 = c1.split(',')
                        for h in c1:
                            pc += 1
                            self.listq.append(str(self.q) + "    arg                                 " + h)
                            self.q_list()

                        self.listq.append(str(self.q) + "    call         " + c2[0] + "        " + str(pc) + "        t" + str(self.t))
                        self.q_list()
                        temp = "t" + str(self.t)
                        self.t += 1
                        x = temp

                if "(" in y:
                        pc = 0
                        c1 = self.parr_part(y)
                        c2 = self.par_part(y)
                        if ',' in c1:
                            c1 = c1.split(',')
                        for h in c1:
                            pc += 1
                            self.listq.append(str(self.q) + "    arg                                 " + h)
                            self.q_list()

                        self.listq.append(str(self.q) + "    call         " + c2[0] + "        " + str(pc) + "        t" + str(self.t))
                        self.q_list()
                        temp = "t" + str(self.t)
                        self.t += 1
                        y = temp

                if "[" in x:
                    c1 = self.cb_part(x)
                    c2 = self.cbr_part(x)
                    if self.number(c2) == False:
                        self.listq.append(str(self.q) + "    mult         " + c2 + "        4           t" + str(self.t))
                        self.q_list()
                        temp = "t" + str(self.t)
                        self.t += 1
                        c2 = temp
                    else:
                        c2 = int(c2) * 4
                    self.listq.append(str(self.q) + "    disp         " + c1[0] + "        " + str(c2) + "        t" + str(self.t))
                    self.q_list()
                    temp = "t" + str(self.t)
                    self.t += 1
                    x = temp

                if "[" in y:
                    c1 = self.cb_part(y)
                    c2 = self.cbr_part(y)
                    if self.number(c2) == False:
                        self.listq.append(str(self.q) + "    mult         " + c2 + "        4           t" + str(self.t))
                        self.q_list()
                        temp = "t" + str(self.t)
                        self.t += 1
                        c2 = temp
                    else:
                        c2 = int(c2) * 4
                    self.listq.append(str(self.q) + "    disp         " + c1[0] + "        " + str(c2) + "        t" + str(self.t))
                    self.q_list()
                    temp = "t" + str(self.t)
                    self.t += 1
                    y = temp
                self.listq.append(str(self.q) + "    div          " + x + "        " + y + "        t" + str(self.t))

            else:
                if "(" in x:
                        pc = 0
                        c1 = self.parr_part(x)
                        c2 = self.par_part(x)
                        if ',' in c1:
                            c1 = c1.split(',')
                        for h in c1:
                            pc += 1
                            print(str(self.q) + "    arg                                 " + h)
                            self.q_list()

                        print(str(self.q) + "    call         " + c2[0] + "        " + str(pc) + "        t" + str(self.t))
                        self.q_list()
                        temp = "t" + str(self.t)
                        self.t += 1
                        x = temp

                if "(" in y:
                        pc = 0
                        c1 = self.parr_part(y)
                        c2 = self.par_part(y)
                        if ',' in c1:
                            c1 = c1.split(',')
                        for h in c1:
                            pc += 1
                            print(str(self.q) + "    arg                                 " + h)
                            self.q_list()

                        print(str(self.q) + "    call         " + c2[0] + "        " + str(pc) + "        t" + str(self.t))
                        self.q_list()
                        temp = "t" + str(self.t)
                        self.t += 1
                        y = temp

                if "[" in x:
                    c1 = self.cb_part(x)
                    c2 = self.cbr_part(x)
                    if self.number(c2) == False:
                        print(str(self.q) + "    mult         " + c2 + "        4           t" + str(self.t))
                        self.q_list()
                        temp = "t" + str(self.t)
                        self.t += 1
                        c2 = temp
                    else:
                        c2 = int(c2) * 4
                    print(str(self.q) + "    disp         " + c1[0] + "        " + str(c2) + "        t" + str(self.t))
                    self.q_list()
                    temp = "t" + str(self.t)
                    self.t += 1
                    x = temp

                if "[" in y:
                    c1 = self.cb_part(y)
                    c2 = self.cbr_part(y)
                    if self.number(c2) == False:
                        print(str(self.q) + "    mult         " + c2 + "        4           t" + str(self.t))
                        self.q_list()
                        temp = "t" + str(self.t)
                        self.t += 1
                        c2 = temp
                    else:
                        c2 = int(c2) * 4
                    print(str(self.q) + "    disp         " + c1[0] + "        " + str(c2) + "        t" + str(self.t))
                    self.q_list()
                    temp = "t" + str(self.t)
                    self.t += 1
                    y = temp
                print(str(self.q) + "    div          " + x + "        " + y + "        t" + str(self.t))
            self.q_list()
            temp = "t" + str(self.t)
            self.t += 1
            return temp

        elif m == "+":
            if self.inwq == 1:
                if "(" in x:
                        pc = 0
                        c1 = self.parr_part(x)
                        c2 = self.par_part(x)
                        if ',' in c1:
                            c1 = c1.split(',')
                        for h in c1:
                            pc += 1
                            self.wlist.append(str(self.q) + "    arg                                 " + h)
                            self.q_list()

                        self.wlist.append(str(self.q) + "    call         " + c2[0] + "        " + str(pc) + "        t" + str(self.t))
                        self.q_list()
                        temp = "t" + str(self.t)
                        self.t += 1
                        x = temp

                if "(" in y:
                        pc = 0
                        c1 = self.parr_part(y)
                        c2 = self.par_part(y)
                        if ',' in c1:
                            c1 = c1.split(',')
                        for h in c1:
                            pc += 1
                            self.wlist.append(str(self.q) + "    arg                                 " + h)
                            self.q_list()

                        self.wlist.append(str(self.q) + "    call         " + c2[0] + "        " + str(pc) + "        t" + str(self.t))
                        self.q_list()
                        temp = "t" + str(self.t)
                        self.t += 1
                        y = temp

                if "[" in x:
                    c1 = self.cb_part(x)
                    c2 = self.cbr_part(x)
                    if self.number(c2) == False:
                        self.wlist.append(str(self.q) + "    mult         " + c2 + "        4           t" + str(self.t))
                        self.q_list()
                        temp = "t" + str(self.t)
                        self.t += 1
                        c2 = temp
                    else:
                        c2 = int(c2) * 4
                    self.wlist.append(str(self.q) + "    disp         " + c1[0] + "        " + str(c2) + "        t" + str(self.t))
                    self.q_list()
                    temp = "t" + str(self.t)
                    self.t += 1
                    x = temp

                if "[" in y:
                    c1 = self.cb_part(y)
                    c2 = self.cbr_part(y)
                    if self.number(c2) == False:
                        self.wlist.append(str(self.q) + "    mult         " + c2 + "        4           t" + str(self.t))
                        self.q_list()
                        temp = "t" + str(self.t)
                        self.t += 1
                        c2 = temp
                    else:
                        c2 = int(c2) * 4
                    self.wlist.append(str(self.q) + "    disp         " + c1[0] + "        " + str(c2) + "        t" + str(self.t))
                    self.q_list()
                    temp = "t" + str(self.t)
                    self.t += 1
                    y = temp

                self.wlist.append(str(self.q) + "    add          " + x + "        " + y + "        t" + str(self.t))

            elif self.inifq == 1:
                if "(" in x:
                        pc = 0
                        c1 = self.parr_part(x)
                        c2 = self.par_part(x)
                        if ',' in c1:
                            c1 = c1.split(',')
                        for h in c1:
                            pc += 1
                            self.listq.append(str(self.q) + "    arg                                 " + h)
                            self.q_list()

                        self.listq.append(str(self.q) + "    call         " + c2[0] + "        " + str(pc) + "        t" + str(self.t))
                        self.q_list()
                        temp = "t" + str(self.t)
                        self.t += 1
                        x = temp

                if "(" in y:
                        pc = 0
                        c1 = self.parr_part(y)
                        c2 = self.par_part(y)
                        if ',' in c1:
                            c1 = c1.split(',')
                        for h in c1:
                            pc += 1
                            self.listq.append(str(self.q) + "    arg                                 " + h)
                            self.q_list()

                        self.listq.append(str(self.q) + "    call         " + c2[0] + "        " + str(pc) + "        t" + str(self.t))
                        self.q_list()
                        temp = "t" + str(self.t)
                        self.t += 1
                        y = temp

                if "[" in x:
                    c1 = self.cb_part(x)
                    c2 = self.cbr_part(x)
                    if self.number(c2) == False:
                        self.listq.append(str(self.q) + "    mult         " + c2 + "        4           t" + str(self.t))
                        self.q_list()
                        temp = "t" + str(self.t)
                        self.t += 1
                        c2 = temp
                    else:
                        c2 = int(c2) * 4
                    self.listq.append(str(self.q) + "    disp         " + c1[0] + "        " + str(c2) + "        t" + str(self.t))
                    self.q_list()
                    temp = "t" + str(self.t)
                    self.t += 1
                    x = temp

                if "[" in y:
                    c1 = self.cb_part(y)
                    c2 = self.cbr_part(y)
                    if self.number(c2) == False:
                        self.listq.append(str(self.q) + "    mult         " + c2 + "        4           t" + str(self.t))
                        self.q_list()
                        temp = "t" + str(self.t)
                        self.t += 1
                        c2 = temp
                    else:
                        c2 = int(c2) * 4
                    self.listq.append(str(self.q) + "    disp         " + c1[0] + "        " + str(c2) + "        t" + str(self.t))
                    self.q_list()
                    temp = "t" + str(self.t)
                    self.t += 1
                    y = temp

                self.listq.append(str(self.q) + "    add          " + x + "        " + y + "        t" + str(self.t))

            else:
                if "(" in x:
                        pc = 0
                        c1 = self.parr_part(x)
                        c2 = self.par_part(x)
                        if ',' in c1:
                            c1 = c1.split(',')
                        for h in c1:
                            pc += 1
                            print(str(self.q) + "    arg                                 " + h)
                            self.q_list()

                        print(str(self.q) + "    call         " + c2[0] + "        " + str(pc) + "        t" + str(self.t))
                        self.q_list()
                        temp = "t" + str(self.t)
                        self.t += 1
                        x = temp

                if "(" in y:
                        pc = 0
                        c1 = self.parr_part(y)
                        c2 = self.par_part(y)
                        if ',' in c1:
                            c1 = c1.split(',')
                        for h in c1:
                            pc += 1
                            print(str(self.q) + "    arg                                 " + h)
                            self.q_list()

                        print(str(self.q) + "    call         " + c2[0] + "        " + str(pc) + "        t" + str(self.t))
                        self.q_list()
                        temp = "t" + str(self.t)
                        self.t += 1
                        y = temp

                if "[" in x:
                    c1 = self.cb_part(x)
                    c2 = self.cbr_part(x)
                    if self.number(c2) == False:
                        print(str(self.q) + "    mult         " + c2 + "        4           t" + str(self.t))
                        self.q_list()
                        temp = "t" + str(self.t)
                        self.t += 1
                        c2 = temp
                    else:
                        c2 = int(c2) * 4
                    print(str(self.q) + "    disp         " + c1[0] + "        " + str(c2) + "        t" + str(self.t))
                    self.q_list()
                    temp = "t" + str(self.t)
                    self.t += 1
                    x = temp

                if "[" in y:
                    c1 = self.cb_part(y)
                    c2 = self.cbr_part(y)
                    if self.number(c2) == False:
                        print(str(self.q) + "    mult         " + c2 + "        4           t" + str(self.t))
                        self.q_list()
                        temp = "t" + str(self.t)
                        self.t += 1
                        c2 = temp
                    else:
                        c2 = int(c2) * 4
                    print(str(self.q) + "    disp         " + c1[0] + "        " + str(c2) + "        t" + str(self.t))
                    self.q_list()
                    temp = "t" + str(self.t)
                    self.t += 1
                    y = temp

                print(str(self.q) + "    add          " + x + "        " + y + "        t" + str(self.t))
            self.q_list()
            temp = "t" + str(self.t)
            self.t += 1
            return temp

        else:  # if m == "-"
            if self.inwq == 1:
                if "(" in x:
                        pc = 0
                        c1 = self.parr_part(x)
                        c2 = self.par_part(x)
                        if ',' in c1:
                            c1 = c1.split(',')
                        for h in c1:
                            pc += 1
                            self.wlist.append(str(self.q) + "    arg                                 " + h)
                            self.q_list()

                        self.wlist.append(str(self.q) + "    call         " + c2[0] + "        " + str(pc) + "        t" + str(self.t))
                        self.q_list()
                        temp = "t" + str(self.t)
                        self.t += 1
                        x = temp

                if "(" in y:
                        pc = 0
                        c1 = self.parr_part(y)
                        c2 = self.par_part(y)
                        if ',' in c1:
                            c1 = c1.split(',')
                        for h in c1:
                            pc += 1
                            self.wlist.append(str(self.q) + "    arg                                 " + h)
                            self.q_list()

                        self.wlist.append(str(self.q) + "    call         " + c2[0] + "        " + str(pc) + "        t" + str(self.t))
                        self.q_list()
                        temp = "t" + str(self.t)
                        self.t += 1
                        y = temp

                if "[" in x:
                    c1 = self.cb_part(x)
                    c2 = self.cbr_part(x)
                    if self.number(c2) == False:
                        self.wlist.append(str(self.q) + "    mult         " + c2 + "        4           t" + str(self.t))
                        self.q_list()
                        temp = "t" + str(self.t)
                        self.t += 1
                        c2 = temp
                    else:
                        c2 = int(c2) * 4
                    self.wlist.append(str(self.q) + "    disp         " + c1[0] + "        " + str(c2) + "        t" + str(self.t))
                    self.q_list()
                    temp = "t" + str(self.t)
                    self.t += 1
                    x = temp

                if "[" in y:
                    c1 = self.cb_part(y)
                    c2 = self.cbr_part(y)
                    if self.number(c2) == False:
                        self.wlist.append(str(self.q) + "    mult         " + c2 + "        4           t" + str(self.t))
                        self.q_list()
                        temp = "t" + str(self.t)
                        self.t += 1
                        c2 = temp
                    else:
                        c2 = int(c2) * 4
                    self.wlist.append(str(self.q) + "    disp         " + c1[0] + "        " + str(c2) + "        t" + str(self.t))
                    self.q_list()
                    temp = "t" + str(self.t)
                    self.t += 1
                    y = temp
                self.wlist.append(str(self.q) + "    sub          " + x + "        " + y + "        t" + str(self.t))

            elif self.inifq == 1:
                if "(" in x:
                        pc = 0
                        c1 = self.parr_part(x)
                        c2 = self.par_part(x)
                        if ',' in c1:
                            c1 = c1.split(',')
                        for h in c1:
                            pc += 1
                            self.listq.append(str(self.q) + "    arg                                 " + h)
                            self.q_list()

                        self.listq.append(str(self.q) + "    call         " + c2[0] + "        " + str(pc) + "        t" + str(self.t))
                        self.q_list()
                        temp = "t" + str(self.t)
                        self.t += 1
                        x = temp

                if "(" in y:
                        pc = 0
                        c1 = self.parr_part(y)
                        c2 = self.par_part(y)
                        if ',' in c1:
                            c1 = c1.split(',')
                        for h in c1:
                            pc += 1
                            self.listq.append(str(self.q) + "    arg                                 " + h)
                            self.q_list()

                        self.listq.append(str(self.q) + "    call         " + c2[0] + "        " + str(pc) + "        t" + str(self.t))
                        self.q_list()
                        temp = "t" + str(self.t)
                        self.t += 1
                        y = temp

                if "[" in x:
                    c1 = self.cb_part(x)
                    c2 = self.cbr_part(x)
                    if self.number(c2) == False:
                        self.listq.append(str(self.q) + "    mult         " + c2 + "        4           t" + str(self.t))
                        self.q_list()
                        temp = "t" + str(self.t)
                        self.t += 1
                        c2 = temp
                    else:
                        c2 = int(c2) * 4
                    self.listq.append(str(self.q) + "    disp         " + c1[0] + "        " + str(c2) + "        t" + str(self.t))
                    self.q_list()
                    temp = "t" + str(self.t)
                    self.t += 1
                    x = temp

                if "[" in y:
                    c1 = self.cb_part(y)
                    c2 = self.cbr_part(y)
                    if self.number(c2) == False:
                        self.listq.append(str(self.q) + "    mult         " + c2 + "        4           t" + str(self.t))
                        self.q_list()
                        temp = "t" + str(self.t)
                        self.t += 1
                        c2 = temp
                    else:
                        c2 = int(c2) * 4
                    self.listq.append(str(self.q) + "    disp         " + c1[0] + "        " + str(c2) + "        t" + str(self.t))
                    self.q_list()
                    temp = "t" + str(self.t)
                    self.t += 1
                    y = temp
                self.listq.append(str(self.q) + "    sub          " + x + "        " + y + "        t" + str(self.t))

            else:
                if "(" in x:
                        pc = 0
                        c1 = self.parr_part(x)
                        c2 = self.par_part(x)
                        if ',' in c1:
                            c1 = c1.split(',')
                        for h in c1:
                            pc += 1
                            print(str(self.q) + "    arg                                 " + h)
                            self.q_list()

                        print(str(self.q) + "    call         " + c2[0] + "        " + str(pc) + "        t" + str(self.t))
                        self.q_list()
                        temp = "t" + str(self.t)
                        self.t += 1
                        x = temp

                if "(" in y:
                        pc = 0
                        c1 = self.parr_part(y)
                        c2 = self.par_part(y)
                        if ',' in c1:
                            c1 = c1.split(',')
                        for h in c1:
                            pc += 1
                            print(str(self.q) + "    arg                                 " + h)
                            self.q_list()

                        print(str(self.q) + "    call         " + c2[0] + "        " + str(pc) + "        t" + str(self.t))
                        self.q_list()
                        temp = "t" + str(self.t)
                        self.t += 1
                        y = temp

                if "[" in x:
                    c1 = self.cb_part(x)
                    c2 = self.cbr_part(x)
                    if self.number(c2) == False:
                        print(str(self.q) + "    mult         " + c2 + "        4           t" + str(self.t))
                        self.q_list()
                        temp = "t" + str(self.t)
                        self.t += 1
                        c2 = temp
                    else:
                        c2 = int(c2) * 4
                    print(str(self.q) + "    disp         " + c1[0] + "        " + str(c2) + "        t" + str(self.t))
                    self.q_list()
                    temp = "t" + str(self.t)
                    self.t += 1
                    x = temp

                if "[" in y:
                    c1 = self.cb_part(y)
                    c2 = self.cbr_part(y)
                    if self.number(c2) == False:
                        print(str(self.q) + "    mult         " + c2 + "        4           t" + str(self.t))
                        self.q_list()
                        temp = "t" + str(self.t)
                        self.t += 1
                        c2 = temp
                    else:
                        c2 = int(c2) * 4
                    print(str(self.q) + "    disp         " + c1[0] + "        " + str(c2) + "        t" + str(self.t))
                    self.q_list()
                    temp = "t" + str(self.t)
                    self.t += 1
                    y = temp
                print(str(self.q) + "    sub          " + x + "        " + y + "        t" + str(self.t))
            self.q_list()
            temp = "t" + str(self.t)
            self.t += 1
            return temp

#-------------------------------------------------------------------------

class Stack:
    def __init__(self):
        self.case = []

    def isEmpty(self):
        return self.case == []

    def push(self, j):
        self.case.append(j)

    def pop(self):
        return self.case.pop()

    def peek(self):
        return self.case[len(self.case)-1]

    def size(self):
        return len(self.case)

#---------------------------------------------------

# Start of script
l = Lexer(sys.argv[1])
l.get_file_lines()
l.get_tokens()
#print(l.tokens)
l.program()

