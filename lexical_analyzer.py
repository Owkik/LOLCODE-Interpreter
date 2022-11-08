from collections import deque
import re


def process(string):
    a = re.split('(\")', string)

    for i in range(len(a)):
        if a[i] == '\"':
            try:
                a[i+1] = a[i]+a[i+1]
                a[i+1] = a[i+1]+a[i+2]
                a[i] = ''
                a[i+2] = ''
            except:
                return ("ERROR")
        elif a[i] != '' and a[i][0] != '\"':
            a[i] = " ".join(a[i].split())

    for i in range(len(a)):
        if a[i] != '':
            a[i] = a[i]+" "

    newSTR = ''
    for token in a:
        newSTR += token

    return newSTR


def tokenize(string):
    lexTable = deque()

    oneKeyWords = {
        "HAI": "Code Delimiter",
        "KTHXBYE": "Code Delimiter",
        "BTW": "Comment Delimiter",
        "OBTW": "Comment Delimiter",
        "TLDR": "Comment Delimiter",
        "ITZ": "Variable Assignment",
        "R": "Assignment Operation",
        "NOT": "Boolean Operator",
        "DIFFRINT": "Comparison Operator",
        "SMOOSH": "Concatenation Keyword",
        "MAEK": "Typecast Keyword",
        'A': "Typecast Keyword",
        'NOOB': "Data Type",
        'TROOF': "Data Type",
        'NUMBR': "Data Type",
        'NUMBAR': "Data Type",
        'YARN': "Data Type",
        "VISIBLE": "Output Keyword",
        "GIMMEH": "Input Keyword",
        "MEBBE": "Else-if Keyword",
        "OIC": "If-then Delimiter",
        "WTF?": "Switch-case Delimiter",
        "OMG": "Case Delimiter",
        "OMGWTF": "Case Default Keyword",
        "UPPIN": "Loop Operator",
        "NERFIN": "Loop Operator",
        "YR": "Loop Operator-Variable Delimiter",
        "TIL": "Loop Repeat Clause Keyword",
        "WILE": "Loop Repeat Clause Keyword",
        "AN": "Operator Delimiter"
    }

    twoKeyWords = {
        "SUM OF": "Arithmetic Operator",
        "DIFF OF": "Arithmetic Operator",
        "PRODUKT OF": "Arithmetic Operator",
        "QUOSHUNT OF": "Arithmetic Operator",
        "MOD OF": "Arithmetic Operator",
        "BIGGR OF": "Arithmetic Operator",
        "SMALLR OF": "Arithmetic Operator",
        "BOTH OF": "Boolean Operator",
        "EITHER OF": "Boolean Operator",
        "WON OF": "Boolean Operator",
        "ANY OF": "Boolean Operator",
        "ALL OF": "Boolean Operator",
        "BOTH SAEM": "Relational Operator",
        "O RLY?": "If-then Delimiter",
        "YA RLY": "If Keyword",
        "NO WAI": "Else Keyword",
        'A NOOB': "Typecast Keyword",
        'A TROOF': "Typecast Keyword",
        'A NUMBR': "Typecast Keyword",
        'A NUMBAR': "Typecast Keyword",
        'A YARN': "Typecast Keyword",
    }

    threeKeywords = {
        "I HAS A": "Variable Declaration",
        "IS NOW A": "Typecast Keyword",
        "IM IN YR": "Loop Delimiter",
        "IM OUTTA YR": "Loop Delimiter"
    }

    first = [
        'I', "SUM", "DIFF",
        "PRODUKT", "QUOSHUNT", "MOD",
        "BIGGR", "SMALLR", "BOTH",
        "EITHER", "WON", "ANY", "ALL",
        "BOTH", "IS", "O", "YA",
                "NO", "IM"
    ]

    second = [
        "HAS", "OF", "SAEM",
        "NOW", "RLY?", "RLY",
        "WAI", "IN", "OUTTA",
        'A', "YR"
    ]

    lineNum = 1
    commentDetected = False
    for line in string.split("\n"):
        token = ""
        if line == "" or line.isspace():
            lineNum += 1
            continue
        line = process(line)
        for word in line.strip().split(' '):
            if word == "TLDR":
                commentDetected = False
            if (commentDetected or word.isspace() or word == '') and token == "":
                continue
            if token == "":
                if word in oneKeyWords.keys():
                    lexTable.append((word, oneKeyWords[word]))
                elif word in first:
                    token += word
                else:
                    if word == "WIN" or word == "FAIL":
                        lexTable.append((word, "Literal"))
                    elif bool(re.match("^-?([0-9]*[.])?[0-9]+$", word)):
                        lexTable.append((word, "Literal"))
                    elif bool(re.match("\".*\"", word)):
                        lexTable.append((word[0], "String Delimiter"))
                        lexTable.append((word[1:(len(word)-1)], "Literal"))
                        lexTable.append(
                            (word[len(word)-1], "String Delimiter"))
                    elif bool(re.match("\"\.*", word)):
                        token += word
                        token += ' '
                    elif bool(re.match("^[a-zA-Z][a-zA-Z0-9_]*$", word)):
                        lexTable.append((word, "Variable Identifier"))
                    elif word.isspace() == False and word != '':
                        print("word")
                        return ("Line "+str(lineNum)+": unidentified token "+word)
            elif token[0] == '\"':
                token += word
                if token[len(token)-1] == '\"':
                    lexTable.append((token[0], "String Delimiter"))
                    lexTable.append((token[1:len(token)-1], "Literal"))
                    lexTable.append(
                        (token[len(token)-1], "String Delimiter"))
                    token = ''
                else:
                    token += ' '
            else:
                if word in second:
                    token += " "
                    token += word
                    if token in twoKeyWords.keys():
                        lexTable.append((token, twoKeyWords[token]))
                        token = ""
                    elif token in threeKeywords.keys():
                        lexTable.append((token, threeKeywords[token]))
                        token = ""
                elif bool(re.match("^[a-zA-Z][a-zA-Z0-9_]*$", word)):
                    if len(token.split(' ')) == 2:
                        lexTable.append((token.split(' ')[0], "identifier"))
                        lexTable.append((token.split(' ')[1], "identifier"))
                    else:
                        lexTable.append((token, "identifier"))
                    lexTable.append((word, "identifier"))
                    token = ''
                else:
                    print("token")
                    return ("Line "+str(lineNum)+": unidentified token "+token)
                    token = ''
            if word == "OBTW":
                commentDetected = True
            elif word == "BTW":
                break
        lineNum += 1
        if token != "":
            if len(token.split(' ')) == 2:
                lexTable.append((token.split(' ')[0], "identifier"))
                lexTable.append((token.split(' ')[1], "identifier"))
            else:
                lexTable.append((token, "identifier"))
            token = ''
    return lexTable
