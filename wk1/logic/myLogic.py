
class Statement:

    def formula(self):
        raise NotImplementedError('Implement to return String representation of Statement.')

    def symbols(self):
        raise NotImplementedError('Implement to return set() of symbols in given Statement')

    def evaluate(self, model):
        raise NotImplementedError('Implement to evaluate given statement for a certain model of T/F values.')

    @classmethod
    def validate(cls, statement):
        if not isinstance(statement, Statement):
            raise Exception(f"Not a logical'Statement': {statement}")

    @classmethod
    def parenthesize(cls, s):
        def balanced(s):
            count = 0
            for c in s:
                if c == '(':
                    count+=1
                elif c == ')':
                    count-=1
            return count==0

        if not len(s) > 0 or s.isalpha() or (s[0]=='(' and s[-1]==')' and balanced(s[1:-1])):
            return s
        else:
            return f'({s})'

class Symbol(Statement):

    def __init__(self, name):
        self.name = name

    def __eq__(self, other):
        return isinstance(other, Symbol) and other.name==self.name

    def __hash__(self) -> int:
        return hash(('Symbol', self.name))

    def __repr__(self):
        return self.name

    def evaluate(self, model):
        try:
            return bool(model[self.name])
        except KeyError:
            raise Exception(f'Symbol {self.name} not in model.')

    def formula(self):
        return self.name

    def symbols(self):
        symbols = set()
        symbols.add(self.name)
        return symbols

class Not(Statement):

    def __init__(self, operand):
        Statement.validate(operand) # Must be a propositional statement.
        self.operand = operand

    def __eq__(self, other):
        return isinstance(other, Not) and other.operand==self.operand

    def __hash__(self) -> int:
        return hash(('Not', hash(self.operand)))

    def __repr__(self) -> str:
        return f'Not({self.operand})'

    def evaluate(self, model):
        return not self.operand.evaluate(model)

    def formula(self):
        return f'!{Statement.parenthesize(self.operand.formula())}'

    def symbols(self):
        return self.operand.symbols()

class And(Statement):

    def __init__(self, *operands):
        self.operands = []

        for o in operands:
            Statement.validate(o) # Must be a propositional statement.
            self.operands.append(o)


    def __eq__(self, other):
        return isinstance(other, And) and other.operands==self.operands

    def __hash__(self) -> int:
        return hash(('Or', tuple(hash(operand) for operand in self.operands)) )     # tuple(iterable) creates ordered list from iterable as (e1, e2, e3, ...) ;)  

    def __repr__(self) -> str:
        conjucts = ', '.join( str(operand) for operand in self.operands)
        return f'And({conjucts})'

    def evaluate(self, model):
        return all(operand.evaluate(model) for operand in self.operands)

    def add(self, operand):
        Statement.validate(operand)
        self.operands.append(operand)

    def formula(self):
        if len(self.operands)==1:
            return self.operands[0].formula()
        return ' ∧ '.join(Statement.parenthesize(operand.formula()) for operand in self.operands)

    def symbols(self):
        symbols = set()
        for operand in self.operands:
            symbols = symbols.union(operand.symbols())
        return symbols

class Or(Statement):

    def __init__(self, *operands):
        self.operands = []

        for o in operands:
            Statement.validate(o) # Must be a propositional statement.
            self.operands.append(o)


    def __eq__(self, other):
        return isinstance(other, Or) and other.operands==self.operands

    def __hash__(self) -> int:
        return hash(('Or', tuple(hash(operand) for operand in self.operands)) )     # tuple(iterable) creates ordered list from iterable as (e1, e2, e3, ...) ;)  

    def __repr__(self) -> str:
        conjucts = ', '.join( str(operand) for operand in self.operands)
        return f'Or({conjucts})'

    def evaluate(self, model):
        return any(operand.evaluate(model) for operand in self.operands)

    def add(self, operand):
        Statement.validate(operand)
        self.operands.append(operand)

    def formula(self):
        if len(self.operands)==1:
            return self.operands[0].formula()
        return ' ∨ '.join(Statement.parenthesize(operand.formula()) for operand in self.operands)

    def symbols(self):
        symbols = set()
        for operand in self.operands:
            symbols = symbols.union(operand.symbols())
        return symbols

class Implication(Statement):

    def __init__(self, antecedent, consequent):
        Statement.validate(antecedent) # Must be a propositional statement.
        Statement.validate(consequent) 
        
        self.antecedent = antecedent
        self.consequent = consequent

    def __eq__(self, other):
        return isinstance(other, Implication) and other.antecedent==self.antecedent and other.consequent==self.consequent

    def __hash__(self) -> int:
        return hash(('Implication', hash(self.antecedent), hash(self.consequent) ) )

    def __repr__(self) -> str:
        return f'Implication({self.antecedent}, {self.consequent})'

    def evaluate(self, model):
        return not self.antecedent.evaluate(model) or self.consequent.evaluate(model)

    def formula(self):
        return f'{Statement.parenthesize(self.antecedent.formula())} -> {Statement.parenthesize(self.consequent.formula())}'

    def symbols(self):
        return set.union(self.antecedent.symbols(), self.consequent.symbols())    

class BiConditional(Statement):

    def __init__(self, left, right):
        Statement.validate(left) # Must be a propositional statement.
        Statement.validate(right) 
        
        self.left = left
        self.right = right

    def __eq__(self, other):
        return isinstance(other, BiConditional) and other.left==self.left and other.right==self.right

    def __hash__(self) -> int:
        return hash(('BiConditional', hash(self.left), hash(self.right) ) )

    def __repr__(self) -> str:
        return f'BiConditional({self.left}, {self.right})'

    def evaluate(self, model):
        left = self.left.evaluate(model)
        right = self.right.evaluate(model)
        return (not left or right) and (not right or left)  # left implies right AND right implies left

    def formula(self):
        return f'{Statement.parenthesize(self.left.formula())} <-> {Statement.parenthesize(self.right.formula())}'

    def symbols(self):
        return set.union(self.left.symbols(), self.right.symbols())    

def model_check(knowledge, query):
    # To Check if Knowledge *Base* entails query.

    def check_all(knowledge, query, symbols, model):
        # Checks if Knowledge entails query, given a particular model

        if len(symbols)==0:
            # If all symbols have T/F value, then return knowledge implies query.
            return not knowledge.evaluate(model) or query.evaluate(model)
        else:
            # Giving truth values to one of the remaining symbols
            remaining = symbols.copy()
            s = remaining.pop()

            model_true = model.copy()
            model_true[s] = True

            model_false = model.copy()
            model_false[s] = False

            # If knowledgebase truly entails query, it must be in all possible models
            return check_all(knowledge, query, remaining, model_true) and check_all(knowledge, query, remaining, model_false)

    # Collecting all symbols, using the helper function. 
    symbols = set.union(knowledge.symbols(), query.symbols())
    return check_all(knowledge, query, symbols, dict())
