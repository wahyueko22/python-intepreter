# Step 1: Lexer - Breaking the code into tokens (like separating words in a sentence)
def lexer(text):
    tokens = []
    i = 0
    
    while i < len(text):
        char = text[i]
        
        # Skip spaces
        if char.isspace():
            i += 1
            continue
            
        # If we find a number
        if char.isdigit():
            number = char
            i += 1
            # Continue collecting digits if there are more
            while i < len(text) and text[i].isdigit():
                number += text[i]
                i += 1
            tokens.append({"type": "NUMBER", "value": int(number)})
            continue
            
        # If we find an operator
        if char in "+-*/":
            tokens.append({"type": "OPERATOR", "value": char})
            i += 1
            continue
            
        # If we don't recognize the character
        raise Exception(f"I don't understand this character: {char}")
    
    return tokens

# Step 2: Parser - Understanding the structure (like understanding grammar)
def parser(tokens):
    # A very simple parser that just builds a tree of operations
    
    def parse_expression():
        left = parse_term()
        
        while tokens and tokens[0]["type"] == "OPERATOR" and tokens[0]["value"] in "+-":
            operator = tokens.pop(0)["value"]
            right = parse_term()
            left = {"type": "OPERATION", "operator": operator, "left": left, "right": right}
            
        return left
    
    def parse_term():
        left = parse_factor()
        
        while tokens and tokens[0]["type"] == "OPERATOR" and tokens[0]["value"] in "*/":
            operator = tokens.pop(0)["value"]
            right = parse_factor()
            left = {"type": "OPERATION", "operator": operator, "left": left, "right": right}
            
        return left
    
    def parse_factor():
        token = tokens.pop(0)
        if token["type"] == "NUMBER":
            return {"type": "NUMBER", "value": token["value"]}
        
        raise Exception("I expected a number here!")
    
    result = parse_expression()
    return result

# Step 3: Interpreter - Actually running the code
def interpreter(tree):
    # For a number node, just return its value
    if tree["type"] == "NUMBER":
        return tree["value"]
    
    # For an operation node, interpret both sides and apply the operator
    if tree["type"] == "OPERATION":
        left_value = interpreter(tree["left"])
        right_value = interpreter(tree["right"])
        
        if tree["operator"] == "+":
            return left_value + right_value
        elif tree["operator"] == "-":
            return left_value - right_value
        elif tree["operator"] == "*":
            return left_value * right_value
        elif tree["operator"] == "/":
            return left_value / right_value

# Put it all together
def run_code(code):
    print(f"Running code: {code}")
    tokens = lexer(code)
    print(f"Tokens: {tokens}")
    tree = parser(tokens)
    print(f"Parse tree: {tree}")
    result = interpreter(tree)
    print(f"Result: {result}")
    return result

# Try it with a simple example
result = run_code("3 + 4 * 2")
print(f"Final answer: {result}")