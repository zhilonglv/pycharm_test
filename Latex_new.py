
class Operator():
    def __init__(self,priority):
        self.priority = priority
    def calculate(self):
        raise NotImplementedError("Each operator type needs to specify how its calculate")

class No_opt(Operator):
    def __init__(self,priority = -1):
        self.priority = priority
    def calculate(self):
        x1 = num.pop()
        x2 = num.pop()
        return 0, None, 0
#123
class Plus(Operator):
    def __init__(self,priority = 10):
        self.priority = priority
        self.value = '+'
    def calculate(self, num:list, next_pos):
        x1 = num.pop()
        x2 = num.pop()
        return x1 + x2, None, next_pos

class Subtraction(Operator):
    def __init__(self,priority = 10):
        self.priority = priority
        self.value = '-'
    def calculate(self, num:list, next_pos):
        x1 = num.pop()
        x2 = num.pop()
        return x2 - x1, None, next_pos

class Multiplication(Operator):
    def __init__(self,priority = 15):
        self.priority = priority
        self.value = '*'
    def calculate(self, num:list, next_pos):
        x1 = num.pop()
        x2 = num.pop()
        return x1 * x2, None, next_pos

def choose_opt(temp):
    if temp == '+':
        return Plus()
    elif temp == '-':
        return Subtraction()
    elif temp == '*':
        return Multiplication()
def pre_process(formula):
    ans = ['start']
    for i in range(len(formula)):
        temp = formula[i]
        if temp in ['+','-','*','{','}','(',')','^']:
            ans.append(choose_opt(temp))
        elif temp == '\\':
            if formula[i:i+4] in ['\\sin']:
                ans.append('sin')
            elif formula[i:i+5] in ['\\frac','\\sqrt']:
                ans.append( formula[i+1:i+5] )
        elif temp.isdigit():
            if isinstance(ans[-1],int):
                ans.append(ans.pop()*10 + int(temp))
            else:
                ans.append(int(temp))
    #ans.append('end')
    print(ans)
    return ans
def get_next_priority(next_char):
    try:
        ans = next_char.priority
    except:
        ans = 0
    return ans
if __name__ == '__main__':
    #str = '\\sqrt{(\\sqrt{3^2}+3)*(2+1)*{6}}+5*3-15'
    str = '1+2-3+5*5'
    Formula = pre_process(str)
    num = []
    opt = [No_opt()]
    i = 1
    current = Formula[i]
    while (True):
        if isinstance(current, int) or isinstance(current, float):
            num.append(current)
            if opt[-1].priority >= get_next_priority(Formula[i + 1].priority):  # 可计算
                current,push_opt,next_pos = opt[-1].calculate(num, i)
                if push_opt == None:
                    opt.pop()
                current = temp if next_pos == 0 else Formula[next_pos]
                i = i if next_pos == 0 else next_pos
            else:
                i = i + 1
                current = Formula[i]
        else:
            if current == 'end':
                break
            if current == '}' or current == ')':
                opt.append(')')
                temp, _ = calculate(opt, num, i)
                current = temp
            else:
                opt.append(current)
                i = i + 1
                current = Formula[i]
        if i + 1 == len(Formula):
            break
        print(num)
    print('num: ',num)
    print('opt: ',opt)
    print('-------------------------------------')