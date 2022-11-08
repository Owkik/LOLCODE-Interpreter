from collections import deque
from email.policy import default

toInsert = list()
toVisible = list()


# check if program has start and ending syntax
def program(lex, inputs):
    toInsert.clear()  # resets the variable toInsert
    toVisible.clear()
    newlex = _removeComments(lex)  # removes comments
    if newlex.popleft()[0] == "HAI" and newlex.pop()[0] == "KTHXBYE":
        if newlex[0][1] == "Literal":
            newlex.popleft()  # pop literal
        return _statements(newlex, inputs)
    else:
        error()


# main process
def _statements(lex, inputs):
    while lex:
        toMatch = lex.popleft()
        match toMatch[0]:
            case "VISIBLE":
                _print(lex)
            case "I HAS A":
                toInsert.append(_declaration(lex))
            case "GIMMEH":
                _setInput(lex.popleft(), inputs)
                toVisible.append(inputs.pop(0))
            case "MAEK":
                _setInput(["IT"], [_typeCast(lex, toMatch)])
            case "WTF?":
                _switchCase(lex, inputs)
            case "GTFO":
                break
            case "O RLY?":
                _ifThen(lex, inputs)
            case "IM IN YR":
                _loop(lex, inputs)
            case _:
                # catch R
                if lex and lex[0][0] == "R":
                    _assignment(lex, toMatch)
                # catch IT of Arithmetic Operator
                elif lex and toMatch[1] == "Arithmetic Operator":
                    _setInput(["IT"], [_mathOperations(lex, toMatch[0])])
                # catch IT of Boolean Operator
                elif lex and toMatch[1] == "Boolean Operator":
                    _setInput(["IT"], [_booleanOperations(lex, toMatch[0])])
                # catch IT of Relational and Comparison Operator
                elif lex and (toMatch[1] == "Relational Operator" or toMatch[1] == "Comparison Operator"):
                    _setInput(["IT"], [_compOperations(lex, toMatch[0])])
                elif lex and lex[0][0] == "IS NOW A":
                    _setInput(["IT"], [_typeCast(lex, toMatch)])
    return [toInsert, toVisible]


# VISIBLE with appending of variables and strings
def _print(lex):
    value = ""
    while (lex and lex[0][1] == "Variable Identifier") or (lex and lex[0][1] == "String Delimiter") or (lex and lex[0][1] == "Boolean Operator") or (lex and lex[0][1] == "Arithmetic Operator") or (lex and lex[0][1] == "Relational Operator") or (lex and lex[0][1] == "Comparison Operator"):
        # catches R
        if len(lex) != 1:
            if lex[1][0] == "R":
                _assignment(lex, lex.popleft())
        if lex[0][0] == '"':
            value += (_string(lex) + ' ')
        elif lex[0][1] == "Variable Identifier":
            value += (str(_checkVariableValue(lex.popleft()[0])) + ' ')
        elif lex[0][1] == "Boolean Operator":
            value += (str(_booleanOperations(lex, lex.popleft()[0])) + ' ')
        elif lex[0][1] == "Arithmetic Operator":
            value += (str(_mathOperations(lex, lex.popleft()[0])) + ' ')
        elif lex[0][1] == "Relational Operator" or lex[0][1] == "Comparison Operator":
            value += (str(_compOperations(lex, lex.popleft()[0])) + ' ')
        elif lex[0][1] == "Typecast Keyword" or lex[1][1] == "Typecast Keyword":
            value += (str(_typeCast(lex, lex.popleft()[0])) + ' ')
    toVisible.append(value)
    _setInput(["IT"], [value])


# gets a variables value
def _checkVariableValue(variableName):
    for i in toInsert:
        if i[0] == variableName:
            return i[1]
    # error()


# process double quotation marks
def _string(lex):
    toRet = ""

    if lex.popleft()[0] == '"':
        toRet += lex.popleft()[0] + ' '
        if lex.popleft()[0] != '"':
            error()

    return toRet


# I HAS A
def _declaration(lex):
    variableName = lex.popleft()[0]
    if lex[0][0] == "ITZ":
        lex.popleft()  # pop ITZ
        if lex[0][0] == '"':  # if string
            _str = _string(lex)
            return [variableName, _str]
        elif lex[0][1] == "Variable Identifier":  # if varible
            _value = _checkVariableValue(lex.popleft()[0])
            return [variableName, _value]
        elif lex[0][1] == "Literal":
            return [variableName, lex.popleft()[0]]
        elif lex[0][1] == "Arithmetic Operator":
            _value = _mathOperations(lex, lex.popleft()[0])
            return [variableName, _value]
        elif lex[0][1] == "Typecast Keyword" or lex[1][1] == "Typecast Keyword":
            _value = _typeCast(lex, lex.popleft()[0])
            return [variableName, _value]
    return [variableName, "NULL"]  # return unintialized variable


# main function of arithmetic operations
def _mathOperations(lex, op):
    operations = [op]
    while lex[0][1] == "Arithmetic Operator":
        operations.append(lex.popleft()[0])

    if lex[0][1] == "Literal":
        temp = lex.popleft()[0]
    elif lex[0][1] == "Variable Identifier":
        temp = _checkVariableValue(lex.popleft()[0])
    elif lex[0][1] == "Typecast Keyword" or lex[1][1] == "Typecast Keyword":
        temp = _typeCast(lex, lex.popleft()[0])
    # for nesting of arithmetic operators
    while operations:
        temp = _mathOperationsProcess(operations.pop(0), temp, _checkAn(lex))

    return temp


# solves the arithmetic code
def _mathOperationsProcess(oper, x, y):
    isInt = True
    if '.' in str(x) or '.' in str(y):
        isInt = False
        x = float(x)
        y = float(y)
    else:
        x = int(x)
        y = int(y)
    if oper == "SUM OF":
        return x+y
    elif oper == "DIFF OF":
        return x-y
    elif oper == "PRODUKT OF":
        return x*y
    elif oper == "QUOSHUNT OF":
        temp = x/y
        if isInt:
            return int(temp)
        return temp
    elif oper == "MOD OF":
        return x % y
    elif oper == "BIGGR OF":
        return _max(x, y)
    elif oper == "SMALLR OF":
        return _min(x, y)


# checks how many nests there are
def _checkAn(lex):
    if lex[0][0] != "AN":
        return
    else:
        lex.popleft()
    if lex[0][1] == "Variable Identifier":
        return _checkVariableValue(lex.popleft()[0])
    elif lex[0][1] == "Literal":
        return lex.popleft()[0]
    elif lex[0][1] == "Arithmetic Operator":
        return _mathOperations(lex, lex.popleft()[0])
    elif lex[0][1] == "Boolean Operator":
        return _booleanOperations(lex, lex.popleft()[0])
    elif lex[0][1] == "Relational Operator" or lex[0][1] == "Comparison Operator":
        return _compOperations(lex, lex.popleft()[0])
    elif lex[0][1] == "Typecast Keyword" or lex[1][1] == "Typecast Keyword":
        return _typeCast(lex, lex.popleft()[0])


# sets the values to the insertlist or changes it
def _setInput(variable, value):
    for i in toInsert:  # check if variable is existing
        if i[0] == variable[0]:
            i[1] = value[0]  # change variable value

            return
    toInsert.append([variable[0], value[0]])


# R = assignment of values
def _assignment(lex, var):
    lex.popleft()
    if lex[0][1] == "Arithmetic Operator":
        _setInput(var, [_mathOperations(lex, lex.popleft()[0])])
    elif lex[0][1] == "Boolean Operator":
        _setInput(var, [_booleanOperations(lex, lex.popleft()[0])])
    elif lex[0][1] == "Literal":
        _setInput(var, [lex.popleft()[0]])
    elif lex[0][1] == "Variable Identifier":
        _setInput(var, [_checkVariableValue(lex.popleft()[0])])
    elif lex[0][1] == "Relational Operator" or lex[0][1] == "Comparison Operator":
        _setInput(var, [_compOperations(lex, lex.popleft()[0])])
    elif lex[0][1] == "Typecast Keyword" or lex[1][1] == "Typecast Keyword":
        _setInput(var, [_typeCast(lex, lex.popleft()[0])])
    return


# max
def _max(a, b):
    if a >= b:
        return a
    else:
        return b


# min
def _min(a, b):
    if a <= b:
        return a
    else:
        return b


# main function of boolean operations
def _booleanOperations(lex, op):
    operations = [op]
    while lex[0][1] == "Boolean Operator":  # for nesting of boolean operators
        operations.append(lex.popleft()[0])
    if lex[0][1] == "Literal":
        temp = lex.popleft()[0]
    elif lex[0][1] == "Variable Identifier":
        temp = _checkVariableValue(lex.popleft()[0])
    elif lex[0][1] == "Relational Operator" or lex[0][1] == "Comparison Operator":
        temp = _compOperations(lex, lex.popleft()[0])
    elif lex[0][1] == "Typecast Keyword" or lex[1][1] == "Typecast Keyword":
        temp = _typeCast(lex, lex.popleft()[0])
    temp = _boolOperationsProcess(lex, operations, temp)

    return temp


# process of boolean operations
def _boolOperationsProcess(lex, oper, x):
    temp1 = x
    if temp1 == "WIN" or temp1 == "FAIL":
        temp1 = _boolConvert(temp1)
    if oper[0] == "ALL OF":
        while lex[0][0] == "AN":
            temp2 = _checkAn(lex)
            temp1 = temp1 and _boolConvert(temp2)
        return _boolRevert(temp1)
    elif oper[0] == "ANY OF":
        while lex[0][0] == "AN":
            temp2 = _checkAn(lex)
            temp1 = temp1 or _boolConvert(temp2)
        return _boolRevert(temp1)
    else:
        # for nesting of boolean operators
        while oper:
            op = oper.pop(0)
            temp2 = _checkAn(lex)
            if op == "BOTH OF":
                temp1 = temp1 and _boolConvert(temp2)
            elif op == "EITHER OF":
                temp1 = temp1 or _boolConvert(temp2)
            elif op == "WON OF":
                temp1 = temp1 ^ _boolConvert(temp2)
            elif op == "NOT":
                temp1 = not temp1
        return _boolRevert(temp1)

# converts WIN and FAIL to True and False


def _boolConvert(str):
    if str == "WIN":
        return True
    elif str == "FAIL":
        return False
    else:
        error()


# reverts the boolean values to LOL Code
def _boolRevert(b):
    if b == True:
        return "WIN"
    elif b == False:
        return "FAIL"
    else:
        error()


# compare operations
def _compOperations(lex, op):
    oper = [op]
    temp1 = ""
    while lex[0][1] == "Relational Operator" or lex[0][1] == "Comparison Operator":
        oper.append(lex.popleft()[0])
    temp = lex.popleft()
    if temp[1] == "Variable Identifier":
        temp1 = _checkVariableValue(temp[0])
    elif temp[1] == "Literal":
        temp1 = temp[0]
    elif temp[1] == "Boolean Operator":
        temp1 = _booleanOperations(lex, lex.popleft()[0])
    elif temp[1] == "Arithmetic Operator":
        temp1 = _mathOperations(lex, lex.popleft()[0])
    elif temp[1] == "Typecast Keyword" or lex[0][1] == "Typecast Keyword":
        temp1 = _typeCast(lex, lex.popleft())

    return _comOperationsProcess(lex, oper, temp1)


# process of both saem and diffrint
def _comOperationsProcess(lex, oper, temp1):
    temp = ""
    while oper:
        if oper[0] == "BOTH SAEM":
            temp = temp1 == _checkAn(lex)
        elif oper[0] == "DIFFRINT":
            temp = int(temp1) != int(_checkAn(lex))
        oper.pop(0)
    return _boolRevert(temp)


# processes typecasting in code
def _typeCast(lex, var):
    var1 = var

    if var == "MAEK":
        var1 = lex.popleft()

    if var1[1] == "Variable Identifier":
        var1 = _checkVariableValue(var1[0])
    elif var1[1] == "Literal":
        var1 = var[0]
    elif var1[1] == "Typecast Keyword":
        var = lex.popleft()
        var1 = _checkVariableValue(var1[0])

    if lex[0][0] == "IS NOW A" or lex[0][0] == "A":  # remove IS NOW A if it's used
        lex.popleft()

    if lex[0][0] == "NUMBR":
        lex.popleft()
        return int(var1)
    elif lex[0][0] == "NUMBAR":
        lex.popleft()
        return float(var1)
    elif lex[0][0] == "YARN":
        lex.popleft()
        return str(var1)
    elif lex[0][0] == "NOOB":
        lex.popleft()
        return "nice"
    elif lex[0][0] == "TROOF":
        lex.popleft()
        return bool(var1)


# main function of the switch case statement
def _switchCase(lex, inputs):
    toMatch = ""
    flag = False
    while lex[0][0] != "OIC":  # while not encountering OIC popleft until encounter
        if lex[0][0] == "OMG":
            lex.popleft()

            # get value to match IT
            if lex[0][1] == "Literal":
                toMatch = lex.popleft()[0]
            elif lex[0][1] == "Variable Identifier":
                toMatch = _checkVariableValue(lex.popleft()[0])

            # check if IT matches the value in  the case
            if str(toMatch) == str(_checkVariableValue("IT")):
                _switchCaseBlock(lex, inputs)
                flag = True

        elif lex[0][0] == "OMGWTF":
            _switchCaseBlock(lex, inputs)
            flag = True

        # if flag is true, it means that the switch case should be terminated
        if flag == True:
            while lex[0][0] != "OIC":
                lex.popleft()
            lex.popleft()
            break

        lex.popleft()


# isolates the block of code to execute and executes it
def _switchCaseBlock(lex, inputs):
    newList = list()  # list of syntax to process
    while lex:
        newList.append(lex.popleft())
        if lex[0][0] == "OMG" or lex[0][0] == "OMGWTF" or lex[0][0] == "OIC":
            break
    _statements(deque(newList), inputs)


# main process of the if-thn statement
def _ifThen(lex, inputs):
    flag = False
    while lex:
        if lex[0][0] == "YA RLY":
            lex.popleft()
            if str(_checkVariableValue("IT")) == "WIN":
                _ifThenBlock(lex, inputs)
                flag = True
            else:
                while lex:
                    print(lex.popleft()[0])
                    if lex[0][0] == "NO WAI" or lex[0][0] == "OIC":
                        break
        if lex[0][0] == "NO WAI" and flag == False:
            lex.popleft()
            _ifThenBlock(lex, inputs)
            flag = True

        if flag == True:
            while lex[0][0] != "OIC":
                lex.popleft()
            lex.popleft()
            break

        lex.popleft()


def _ifThenBlock(lex, inputs):
    newList = list()  # list of syntax to process
    while lex:
        newList.append(lex.popleft())
        if lex[0][0] == "NO WAI" or lex[0][0] == "OIC":
            break
    _statements(deque(newList), inputs)


# main function for the loops
def _loop(lex, inputs):
    lex.popleft()  # pop variable identifier
    operator = lex.popleft()[0]  # pop operator
    lex.popleft()  # pop YR
    if lex[0][1] == "Variable Identifier":
        var = lex.popleft()[0]
        varValue = _checkVariableValue(var)
        tilWile = lex.popleft()[0]
        oper = lex.popleft()[0]
        temp1 = int(_checkVariableValue(lex.popleft()[0]))
        lex.popleft()  # pop AN
        temp2 = 0
        if lex[0][1] == "Literal":
            temp2 = int(lex.popleft()[0])
        elif lex[0][1] == "Variable Identifier":
            temp2 = int(_checkVariableValue(lex.popleft()[0]))
        block = _loopBlock(lex, inputs)
        if tilWile == "TIL":
            if oper == "BOTH SAEM":
                while (temp1 == temp2) == False:
                    _statements(block.copy(), inputs)
                    if operator == "UPPIN":
                        temp1 = temp1 + 1
                    elif operator == "NERFIN:":
                        temp1 = temp1 - 1
                    else:
                        error()
            elif oper == "DIFFRINT":
                while (temp1 != temp2) == False:
                    _statements(block.copy(), inputs)
                    if operator == "UPPIN":
                        temp1 = temp1 + 1
                    elif operator == "NERFIN:":
                        temp1 = temp1 - 1
                    else:
                        error()
            else:
                error()
        elif tilWile == "WILE":
            if oper == "BOTH SAEM":
                while (temp1 == temp2) == True:
                    _statements(block.copy(), inputs)
                    if operator == "UPPIN":
                        temp1 = temp1 + 1
                    elif operator == "NERFIN:":
                        temp1 = temp1 - 1
                    else:
                        error()
            elif oper == "DIFFRINT":
                while (temp1 != temp2) == True:
                    _statements(block.copy(), inputs)
                    if operator == "UPPIN":
                        temp1 = temp1 + 1
                    elif operator == "NERFIN:":
                        temp1 = temp1 - 1
                    else:
                        error()
            else:
                error()
        else:
            error()


# creates the block of code for the loop
def _loopBlock(lex, inputs):
    newList = list()  # list of syntax to process
    while lex:
        newList.append(lex.popleft())
        if lex[0][0] == "IM OUTTA YR":
            lex.popleft()  # pop IM OUTTA YR
            lex.popleft()  # pop variable
            break
    return deque(newList)


# removes all comments
def _removeComments(lex):
    templist = list()
    for i in lex:
        if i[1] == "Comment Delimiter":
            continue
        else:
            templist.append(i)
    return deque(templist)


def error():
    print("Syntax Error")
    return
