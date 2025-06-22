# HLang Programming Language - Semantic Constraints and Error Types
**Static Semantic Analysis Reference**  
**Version 1.0 - June 2025**

## Overview

This document provides a comprehensive reference for all semantic constraints and error types that must be checked by the HLang static semantic analyzer. Each error type includes detailed rules, exception specifications, and extensive examples to guide implementation and testing.

## Error Types Summary

The HLang static semantic checker must detect and report the following error types:

1. **Redeclared** - Variables, constants, functions, or parameters declared multiple times in the same scope
2. **Undeclared** - Use of identifiers or functions that have not been declared
3. **TypeMismatchInExpression** - Type incompatibilities in expressions
4. **TypeMismatchInStatement** - Type incompatibilities in statements
5. **TypeCannotBeInferred** - Situations where type inference fails
6. **MustInLoop** - Break/continue statements outside of loop contexts
7. **NoEntryPoint** - Missing or invalid main function
8. **Function Parameter/Argument Mismatch** - Incorrect function call signatures
9. **Array Type Compatibility** - Array type and size mismatches

---

## Detailed Error Specifications

### 1. Redeclared Variable/Constant/Function

**Rule:** All declarations must be unique within their respective scopes as defined in the HLang specification.

**Exception:** `Redeclared(<kind>, <identifier>)`
- `<kind>`: Type of redeclared entity (`Variable`, `Constant`, `Function`, `Parameter`)
- `<identifier>`: Name of the redeclared identifier

**Scope-specific Rules:**
- **Global scope:** Constants and functions must have unique names
- **Function scope:** Parameters and local variables must have unique names
- **Block scope:** Variables within the same block must have unique names
- **Cross-scope:** Inner declarations can shadow outer ones (not an error)

**Examples:**
```hlang
// Error: Redeclared Variable in same scope
func example() -> void {
    let x = 10;
    let x = 20;  // Redeclared(Variable, x)
}

// Error: Redeclared Function in global scope
func calculate() -> int { return 42; }
func calculate() -> int { return 24; }  // Redeclared(Function, calculate)

// Error: Redeclared Constant in global scope
const PI = 3.14;
const PI = 3.14159;  // Redeclared(Constant, PI)

// Error: Redeclared Parameter
func process(x: int, y: float, x: bool) -> void {  // Redeclared(Parameter, x)
    print("Processing");
}

// Error: Variable redeclared as constant in same scope
func mixed() -> void {
    let value = 42;
    const value = 100;  // Redeclared(Constant, value)
}

// Error: Redeclared in nested block (same level)
func nested() -> void {
    if (true) {
        let temp = 1;
        let temp = 2;  // Redeclared(Variable, temp)
    }
}

// Valid: Shadowing (different scopes)
let globalVar = 100;
func shadowExample() -> void {
    let globalVar = 200;  // Valid: shadows global variable
    {
        let globalVar = 300;  // Valid: shadows function-scope variable
    }
}

// Error: Function parameter conflicts with local variable
func paramConflict(count: int) -> void {
    let count = 0;  // Redeclared(Variable, count) - conflicts with parameter
}
```

### 2. Undeclared Identifier/Function

**Rules:**
- Variables and constants must be declared before use
- Functions must be declared before being called
- Identifiers must be accessible in the current scope

**Exceptions:**
- `Undeclared(Identifier(), <identifier-name>)`: For undeclared variables/constants
- `Undeclared(Function(), <function-name>)`: For undeclared functions

**Scope Resolution Rules:**
- Search order: Current block → Function scope → Global scope
- Shadowed identifiers are not accessible from inner scopes
- Function calls require the function to be declared in accessible scope

**Examples:**
```hlang
// Error: Undeclared variable
func main() -> void {
    print(str(undeclaredVar));  // Undeclared(Identifier(), undeclaredVar)
}

// Error: Undeclared function
func main() -> void {
    undeclaredFunc();           // Undeclared(Function(), undeclaredFunc)
}

// Error: Variable used before declaration
func beforeDeclaration() -> void {
    let result = x + 10;  // Undeclared(Identifier(), x)
    let x = 5;
}

// Error: Out of scope variable
func scopeError() -> void {
    if (true) {
        let localVar = 42;
    }
    print(str(localVar));  // Undeclared(Identifier(), localVar)
}

// Error: Shadowed variable not accessible
func shadowError() -> void {
    let x = 10;
    {
        let x = 20;  // Shadows outer x
        {
            let y = x + 5;  // Uses inner x (20)
        }
        let z = y + 1;  // Undeclared(Identifier(), y) - y is out of scope
    }
}

// Error: Function not yet declared
func earlyCall() -> void {
    laterFunc();  // Undeclared(Function(), laterFunc)
}

func laterFunc() -> void {
    print("Called later");
}

// Error: Function declared but not accessible
func main() -> void {
    {
        func localFunc() -> void { print("local"); }
    }
    localFunc();  // Undeclared(Function(), localFunc) - out of scope
}

// Valid: Forward reference to global function
func validCall() -> void {
    globalFunc();  // Valid: globalFunc declared later but in global scope
}

func globalFunc() -> void {
    print("Global function");
}

// Error: Constant used before declaration
func constError() -> void {
    let value = MAX_VALUE + 1;  // Undeclared(Identifier(), MAX_VALUE)
}

const MAX_VALUE = 100;
```

### 3. Type Mismatch in Expression

**Rule:** All expressions must conform to HLang's type system rules.

**Exception:** `TypeMismatchInExpression(<expression>)`

**Detailed Type Rules:**

**Array Access Rules:**
- Array expression must be of array type `[T; N]`
- Index expression must be of type `int`
- Result type is the element type `T`

**Binary Operation Rules:**
- **Arithmetic (`+`, `-`, `*`, `/`, `%`):**
  - Both operands must be `int` or `float`
  - If both are `int`, result is `int`
  - If either is `float`, result is `float`
  - Special case: `string + string` is valid (concatenation)
- **Comparison (`<`, `<=`, `>`, `>=`):**
  - Both operands must be `int` or `float`
  - Result is always `bool`
- **Equality (`==`, `!=`):**
  - Both operands must have the same type
  - Result is always `bool`
- **Logical (`&&`, `||`):**
  - Both operands must be `bool`
  - Result is always `bool`

**Unary Operation Rules:**
- **Negation (`-`):** Operand must be `int` or `float`, result has same type
- **Positive (`+`):** Operand must be `int` or `float`, result has same type
- **Logical NOT (`!`):** Operand must be `bool`, result is `bool`

**Function Call Rules:**
- Function expression must be callable (function type)
- Number of arguments must match parameter count exactly
- Each argument type must match corresponding parameter type exactly
- Function must have non-void return type for use in expressions

**Examples:**
```hlang
func main() -> void {
    // Array access errors
    let numbers = [1, 2, 3];
    let result1 = numbers["invalid"];     // TypeMismatchInExpression - string index
    let result2 = numbers[3.14];          // TypeMismatchInExpression - float index
    let result3 = numbers[true];          // TypeMismatchInExpression - bool index
    
    // Binary operation errors
    let x = 5;
    let y = true;
    let sum = x + y;                      // TypeMismatchInExpression - int + bool
    let comparison = x < "hello";         // TypeMismatchInExpression - int < string
    let equality = x == 5.0;              // TypeMismatchInExpression - int == float
    let logical = x && y;                 // TypeMismatchInExpression - int && bool
    
    // Unary operation errors
    let condition = !42;                  // TypeMismatchInExpression - !int
    let negative = -true;                 // TypeMismatchInExpression - -bool
    let positive = +"text";               // TypeMismatchInExpression - +string
    
    // Function call errors
    let voidResult = printMessage("hi");  // TypeMismatchInExpression - void function in expression
    let wrongArgs = add(5, "hello");      // TypeMismatchInExpression - int, string to int, int
    let tooFewArgs = multiply(5);         // TypeMismatchInExpression - 1 arg to 2-param function
    let tooManyArgs = getValue(1, 2);     // TypeMismatchInExpression - 2 args to 0-param function
}

func add(a: int, b: int) -> int {
    return a + b;
}

func multiply(a: int, b: int) -> int {
    return a * b;
}

func getValue() -> int {
    return 42;
}

func printMessage(msg: string) -> void {
    print(msg);
}

// Array type mismatches
func arrayErrors() -> void {
    let intArray: [int; 3] = [1, 2, 3];
    let floatArray: [float; 3] = [1.0, 2.0, 3.0];
    let stringArray: [string; 2] = ["a", "b"];
    
    // Type mismatch in array access
    let result1 = intArray[floatArray[0]];    // TypeMismatchInExpression - float index
    let result2 = stringArray[intArray];      // TypeMismatchInExpression - array index
    
    // Mixed type operations
    let mixed1 = intArray[0] + floatArray[0]; // Valid - int + float = float
    let mixed2 = intArray[0] + stringArray[0]; // TypeMismatchInExpression - int + string
}

// Nested expression errors
func nestedErrors() -> void {
    let arr = [1, 2, 3];
    let result = arr[arr[true]];              // TypeMismatchInExpression - bool index in inner access
    let complex = (5 + 3) * ("hello" + 2);   // TypeMismatchInExpression - string + int
}
```

### 4. Type Cannot Be Inferred

**Rule:** HLang supports limited type inference, but some types must be explicitly inferrable from context.

**Exception:** `TypeCannotBeInferred(<statement>)`

**Inference Rules:**
- Variable types are inferred from initialization expressions only
- Function return types must be explicitly declared (no inference)
- Array types are inferred from element types and count
- Type inference follows a single-pass, top-to-bottom approach
- If a type cannot be determined from available context, an error is raised

**Scenarios where inference fails:**
1. Function declared without explicit return type annotation
2. Empty array literals without type annotation
3. Circular type dependencies in variable initialization
4. Complex expressions where type cannot be resolved unambiguously
5. Generic or ambiguous expressions without sufficient context

**Examples:**
```hlang
// Error: Function without return type annotation
func noReturnType() {                   // TypeCannotBeInferred - missing return type annotation
    return 42;                          // Cannot infer return type from declaration
}

// Error: Empty array without type annotation
func emptyArray() -> void {
    let arr = [];                       // TypeCannotBeInferred - empty array literal
    arr[0] = 5;                         // Cannot determine element type
}

// Error: Circular type dependencies
func circularDependency() -> void {
    let a = b + 1;                      // TypeCannotBeInferred - b not yet declared
    let b = a * 2;                      // Creates circular dependency
}

// Error: Forward reference in initialization
func forwardRef() -> void {
    let result = processValue(undefined); // TypeCannotBeInferred - undefined not declared
    let undefined = getValue();
}

// Error: Complex expression without sufficient context
func ambiguousContext() -> void {
    let result = getGenericValue();     // TypeCannotBeInferred - function return type unknown
    print(str(result));
}

// Error: Mixed array elements without clear type
func mixedArrayElements() -> void {
    let mixed = [getValue(), getOtherValue()]; // TypeCannotBeInferred - unclear element type
    print(str(len(mixed)));
}

// Valid: Proper type inference from initializers
func validInference() -> void {
    let x = 42;                         // Inferred as int from literal
    let y = 3.14;                       // Inferred as float from literal
    let z = true;                       // Inferred as bool from literal
    let s = "hello";                    // Inferred as string from literal
    let arr = [1, 2, 3];               // Inferred as [int; 3] from array literal
    let mixed = x + y;                  // Inferred as float (int + float promotion)
}

// Valid: Explicit type annotations where needed
func explicitTypes() -> void {
    let emptyArray: [int; 0] = [];      // Valid - explicit type for empty array
    let typed: int = getValue();        // Valid - explicit type annotation
}

// Note: Function parameters must have explicit type annotations
func explicitParams(x: int) -> int {    // Valid - explicit parameter type
    return x + 1;
}

// Valid: Proper conditional with clear inference
func conditionalValid(condition: bool) -> void {
    let value = condition ? "yes" : "no"; // Valid - type inferred from ternary expression
    print(value);
}

func getValue() -> int {
    return 10;
}

func getOtherValue() -> float {
    return 3.14;
}

// This function would cause TypeCannotBeInferred in ambiguousContext
// func getGenericValue() {             // Missing return type
//     return someValue;
// }
```

### 5. Type Mismatch in Statement

**Rule:** Statements must follow HLang's type rules for control flow and assignments.

**Exception:** `TypeMismatchInStatement(<statement>)`

**Detailed Statement Type Rules:**

**Conditional Statements (`if`, `else if`):**
- Condition expression must evaluate to `bool` type
- No implicit type conversion (unlike C/C++)
- Parentheses around condition are mandatory

**Loop Statements:**
- **While loops:** Condition must be `bool` type
- **For loops:** Collection must be array type, loop variable automatically typed

**Assignment Statements:**
- Left-hand side must be a mutable lvalue
- Right-hand side type must be compatible with left-hand side type
- Array element assignments require matching element types

**Return Statements:**
- Return value type must match declared function return type exactly
- Void functions can use `return;` or implicit return
- Non-void functions must return a value of correct type

**Function Call Statements:**
- Function must return `void` type for statement context
- All arguments must match parameter types exactly
- Number of arguments must match parameter count

**Examples:**
```hlang
// Conditional statement errors
func conditionalErrors() -> void {
    let x = 10;
    let message = "hello";
    
    if (x) {                            // TypeMismatchInStatement - int condition
        print("Invalid");
    }
    
    if (message) {                      // TypeMismatchInStatement - string condition
        print("Also invalid");
    }
    
    if (x > 5 && message) {             // TypeMismatchInStatement - string in logical expression
        print("Mixed error");
    }
}

// Loop statement errors
func loopErrors() -> void {
    let x = 5;
    let message = "test";
    
    while (x) {                         // TypeMismatchInStatement - int condition
        x = x - 1;
    }
    
    while (message) {                   // TypeMismatchInStatement - string condition
        break;
    }
    
    // For loop errors
    for (item in x) {                   // TypeMismatchInStatement - int is not iterable
        print(str(item));
    }
    
    for (item in message) {             // TypeMismatchInStatement - string is not iterable
        print(item);
    }
}

// Assignment statement errors
func assignmentErrors() -> void {
    let x: int = 10;
    let y: float = 3.14;
    let flag: bool = true;
    let text: string = "hello";
    let numbers: [int; 3] = [1, 2, 3];
    
    x = "invalid";                      // TypeMismatchInStatement - string to int
    y = flag;                           // TypeMismatchInStatement - bool to float
    flag = x;                           // TypeMismatchInStatement - int to bool
    text = y;                           // TypeMismatchInStatement - float to string
    
    // Array assignment errors
    numbers = [1.0, 2.0, 3.0];         // TypeMismatchInStatement - float array to int array
    numbers[0] = 3.14;                  // TypeMismatchInStatement - float to int element
    numbers[1] = "text";                // TypeMismatchInStatement - string to int element
    
    // Constant assignment error
    const PI = 3.14159;
    PI = 2.71828;                       // TypeMismatchInStatement - cannot assign to constant
}

// Return statement errors
func returnInt() -> int {
    return true;                        // TypeMismatchInStatement - bool to int
}

func returnFloat() -> float {
    return "3.14";                      // TypeMismatchInStatement - string to float
}

func returnBool() -> bool {
    return 1;                           // TypeMismatchInStatement - int to bool
}

func returnString() -> string {
    return 42;                          // TypeMismatchInStatement - int to string
}

func returnArray() -> [int; 3] {
    return [1.0, 2.0, 3.0];            // TypeMismatchInStatement - float array to int array
}

func returnVoid() -> void {
    return 42;                          // TypeMismatchInStatement - int to void
}

// Function call statement errors
func callErrors() -> void {
    let result = printMessage("hi");    // TypeMismatchInStatement - void function assigned to variable
    
    // Wrong argument types
    addNumbers("5", "10");              // TypeMismatchInStatement - string args to int params
    addNumbers(5, 10, 15);              // TypeMismatchInStatement - too many arguments
    addNumbers(5);                      // TypeMismatchInStatement - too few arguments
}

func printMessage(msg: string) -> void {
    print(msg);
}

func addNumbers(a: int, b: int) -> int {
    return a + b;
}

// Complex type mismatch errors
func complexErrors() -> void {
    let matrix: [[int; 2]; 2] = [[1, 2], [3, 4]];
    let floatMatrix: [[float; 2]; 2] = [[1.0, 2.0], [3.0, 4.0]];
    
    matrix = floatMatrix;               // TypeMismatchInStatement - different element types
    matrix[0] = [1.0, 2.0];            // TypeMismatchInStatement - float array to int array row
    
    // Nested array assignment
    matrix[0][0] = 3.14;               // TypeMismatchInStatement - float to int element
}

// Array size mismatch
func arraySizeErrors() -> void {
    let small: [int; 2] = [1, 2];
    let large: [int; 5] = [1, 2, 3, 4, 5];
    
    small = large;                      // TypeMismatchInStatement - different array sizes
    large = small;                      // TypeMismatchInStatement - different array sizes
}
```

### 6. Break/Continue Not In Loop

**Rule:** `break` and `continue` statements must appear within loop constructs (`while` or `for` loops).

**Exception:** `MustInLoop(<statement>)`

**Loop Context Rules:**
- `break` and `continue` are only valid inside loop bodies
- Nested loops: `break`/`continue` applies to the innermost loop
- Function boundaries: `break`/`continue` cannot cross function boundaries
- Conditional blocks: `break`/`continue` inside `if` statements must still be within a loop

**Invalid Contexts:**
- Global scope
- Function scope (outside loops)
- Conditional blocks (if/else) that are not inside loops
- Any block that is not a loop body

**Examples:**
```hlang
// Error: Break/continue in global scope
break;                                   // MustInLoop(break)
continue;                                // MustInLoop(continue)

// Error: Break/continue in function scope
func main() -> void {
    break;                               // MustInLoop(break)
    continue;                            // MustInLoop(continue)
}

// Error: Break/continue in conditional blocks
func conditionalError() -> void {
    if (true) {
        break;                           // MustInLoop(break)
        continue;                        // MustInLoop(continue)
    }
    
    if (someCondition()) {
        print("Processing");
        break;                           // MustInLoop(break)
    } else {
        continue;                        // MustInLoop(continue)
    }
}

// Error: Break/continue in nested blocks
func nestedError() -> void {
    {
        let x = 10;
        if (x > 5) {
            break;                       // MustInLoop(break)
        }
        continue;                        // MustInLoop(continue)
    }
}

// Valid: Break/continue in while loops
func validWhile() -> void {
    let i = 0;
    while (i < 10) {
        if (i == 5) {
            break;                       // Valid - inside while loop
        }
        if (i % 2 == 0) {
            i = i + 1;
            continue;                    // Valid - inside while loop
        }
        i = i + 1;
    }
}

// Valid: Break/continue in for loops
func validFor() -> void {
    let numbers = [1, 2, 3, 4, 5];
    for (num in numbers) {
        if (num == 3) {
            break;                       // Valid - inside for loop
        }
        if (num % 2 == 0) {
            continue;                    // Valid - inside for loop
        }
        print(str(num));
    }
}

// Valid: Break/continue in nested loops
func nestedLoops() -> void {
    let i = 0;
    while (i < 5) {
        let j = 0;
        while (j < 5) {
            if (i == j) {
                break;                   // Valid - breaks inner loop
            }
            if (j == 2) {
                j = j + 1;
                continue;                // Valid - continues inner loop
            }
            j = j + 1;
        }
        i = i + 1;
    }
}

// Valid: Break/continue in conditional blocks inside loops
func conditionalInLoop() -> void {
    let i = 0;
    while (i < 10) {
        if (i == 5) {
            break;                       // Valid - conditional inside loop
        }
        if (i % 2 == 0) {
            i = i + 1;
            continue;                    // Valid - conditional inside loop
        }
        print(str(i));
        i = i + 1;
    }
}

// Error: Break/continue after loop
func afterLoop() -> void {
    let i = 0;
    while (i < 5) {
        i = i + 1;
    }
    break;                               // MustInLoop(break) - after loop ends
    continue;                            // MustInLoop(continue) - after loop ends
}

// Error: Break/continue in function called from loop
func helperFunction() -> void {
    break;                               // MustInLoop(break) - different function scope
    continue;                            // MustInLoop(continue) - different function scope
}

func loopWithFunction() -> void {
    let i = 0;
    while (i < 5) {
        helperFunction();                // Function call doesn't transfer loop context
        i = i + 1;
    }
}

func someCondition() -> bool {
    return true;
}
```

### 7. No Entry Point

**Rule:** Every HLang program must contain a `main` function with signature `func main() -> void`.

**Exception:** `NoEntryPoint()`

**Requirements for main function:**
- Name must be exactly `main` (case-sensitive)
- Must take no parameters (empty parameter list)
- Must return `void` type
- Must have a function body (definition, not just declaration)
- Must be declared at global scope

**Invalid main function scenarios:**
1. No main function at all
2. main function with wrong name (case-sensitive)
3. main function with parameters
4. main function with non-void return type
5. main function declared but not defined
6. Multiple main functions (redeclaration)

**Examples:**
```hlang
// Error: No main function at all
func helper() -> void {
    print("Helper function");           // NoEntryPoint() - no main function
}

func calculate(x: int) -> int {
    return x * 2;
}

// Error: Wrong function name (case-sensitive)
func Main() -> void {                   // NoEntryPoint() - capital M
    print("Wrong case");
}

func MAIN() -> void {                   // NoEntryPoint() - all caps
    print("All caps");
}

func main_function() -> void {          // NoEntryPoint() - underscore
    print("Wrong name");
}

// Error: main function with parameters
func main(args: [string; 5]) -> void { // NoEntryPoint() - has parameters
    print("With arguments");
}

func main(argc: int, argv: string) -> void { // NoEntryPoint() - multiple parameters
    print("Command line args");
}

// Error: main function with wrong return type
func main() -> int {                    // NoEntryPoint() - returns int
    print("Returns integer");
    return 0;
}

func main() -> string {                 // NoEntryPoint() - returns string
    print("Returns string");
    return "done";
}

func main() -> bool {                   // NoEntryPoint() - returns bool
    print("Returns boolean");
    return true;
}

func main() -> [int; 3] {              // NoEntryPoint() - returns array
    return [1, 2, 3];
}

// Error: main function declared but not defined
func main() -> void;                    // NoEntryPoint() - declaration only

func otherFunction() -> void {
    print("Other function");
}

// Error: Multiple main functions (this would be caught as Redeclared first)
func main() -> void {
    print("First main");
}

func main() -> void {                   // Redeclared(Function, main) - not NoEntryPoint
    print("Second main");
}

// Valid: Correct main function
func main() -> void {
    print("Hello, World!");
}

// Valid: main function with other functions
func helper() -> int {
    return 42;
}

func main() -> void {                   // Valid main function
    let value = helper();
    print(str(value));
}

// Error: main function in wrong scope (if HLang allowed nested functions)
func container() -> void {
    func main() -> void {               // NoEntryPoint() - not at global scope
        print("Nested main");
    }
}

// Error: Complex scenarios
const MAIN_NAME = "main";
func getMainName() -> string {
    return MAIN_NAME;
}

// Still need actual main function
func process() -> void {                // NoEntryPoint() - no actual main
    print("Processing");
}

// Valid: main can call other functions
func initialize() -> void {
    print("Initializing...");
}

func cleanup() -> void {
    print("Cleaning up...");
}

func main() -> void {                   // Valid
    initialize();
    print("Main execution");
    cleanup();
}
```

### 8. Function Parameter/Argument Mismatch

**Rule:** Function calls must match the exact number and types of parameters.

**Exception:** `TypeMismatchInExpression(<function-call>)` or `TypeMismatchInStatement(<call-statement>)`

**Parameter Matching Rules:**
1. **Argument Count:** Must match parameter count exactly
2. **Argument Types:** Each argument type must match corresponding parameter type exactly
3. **Parameter Order:** Arguments are matched positionally (first argument to first parameter, etc.)
4. **No Default Parameters:** HLang doesn't support default parameter values
5. **No Variadic Functions:** HLang doesn't support variable argument counts

**Type Compatibility Rules:**
- Exact type match required (no implicit conversions)
- `int` and `float` are not interchangeable
- Array types must match exactly in both element type and size
- Function types must match signature exactly

**Examples:**
```hlang
// Function definitions for testing
func add(a: int, b: int) -> int {
    return a + b;
}

func multiply(x: float, y: float) -> float {
    return x * y;
}

func processArray(arr: [int; 5]) -> void {
    print("Processing array");
}

func greet(name: string, age: int, isStudent: bool) -> void {
    print("Hello " + name);
}

func noParams() -> string {
    return "No parameters";
}

func voidFunction(msg: string) -> void {
    print(msg);
}

// Argument count errors
func countErrors() -> void {
    // Too few arguments
    let result1 = add(5);               // TypeMismatchInExpression - 1 arg, expects 2
    let result2 = multiply(3.14);       // TypeMismatchInExpression - 1 arg, expects 2
    greet("Alice");                     // TypeMismatchInStatement - 1 arg, expects 3
    greet("Bob", 25);                   // TypeMismatchInStatement - 2 args, expects 3
    
    // Too many arguments
    let result3 = add(5, 10, 15);       // TypeMismatchInExpression - 3 args, expects 2
    let result4 = noParams(42);         // TypeMismatchInExpression - 1 arg, expects 0
    let result5 = noParams("extra", 5); // TypeMismatchInExpression - 2 args, expects 0
    voidFunction("msg", "extra");       // TypeMismatchInStatement - 2 args, expects 1
}

// Argument type errors
func typeErrors() -> void {
    // Wrong single argument types
    let result1 = add(5, "hello");      // TypeMismatchInExpression - int, string to int, int
    let result2 = add(true, false);     // TypeMismatchInExpression - bool, bool to int, int
    let result3 = multiply(5, 10);      // TypeMismatchInExpression - int, int to float, float
    
    // Mixed type errors
    greet(25, "Alice", true);           // TypeMismatchInStatement - wrong order and types
    greet("Alice", 25.5, "yes");        // TypeMismatchInStatement - float and string instead of int and bool
    
    // Array type errors
    let intArray: [int; 5] = [1, 2, 3, 4, 5];
    let floatArray: [float; 5] = [1.0, 2.0, 3.0, 4.0, 5.0];
    let smallArray: [int; 3] = [1, 2, 3];
    
    processArray(floatArray);           // TypeMismatchInStatement - float array to int array
    processArray(smallArray);           // TypeMismatchInStatement - size 3 to size 5
    processArray(42);                   // TypeMismatchInStatement - int to array
}

// Complex mismatch scenarios
func complexErrors() -> void {
    // Nested function call errors
    let result1 = add(multiply(2.0, 3.0), 5); // TypeMismatchInExpression - float result to int parameter
    let result2 = multiply(add(2, 3), 4.0);   // TypeMismatchInExpression - int result to float parameter
    
    // Expression context vs statement context
    let value = voidFunction("test");    // TypeMismatchInExpression - void function in expression
    add(1, 2);                          // Valid - non-void function as statement (return value ignored)
}

// Function pointer/reference errors (if supported)
func functionRefErrors() -> void {
    // These would be errors if HLang supported function references
    // let funcRef = add;
    // funcRef(1, 2, 3);                // Too many arguments through reference
}

// Valid function calls
func validCalls() -> void {
    // Correct argument counts and types
    let sum = add(10, 20);              // Valid
    let product = multiply(3.14, 2.71); // Valid
    let message = noParams();           // Valid
    
    greet("Alice", 25, true);           // Valid
    voidFunction("Hello World");        // Valid
    
    let numbers: [int; 5] = [1, 2, 3, 4, 5];
    processArray(numbers);              // Valid
    
    // Nested valid calls
    let nested = add(add(1, 2), add(3, 4)); // Valid
    voidFunction(noParams());           // Valid - string return to string parameter
}

// Edge cases
func edgeCases() -> void {
    // Empty arrays (if supported in function parameters)
    // processEmptyArray([]);           // Would depend on array type inference
    
    // Literal arguments
    add(5 + 3, 10 - 2);                // Valid - expressions as arguments
    multiply(3.14159, 2.0);            // Valid - float literals
    greet("Literal", 18 + 7, !false);  // Valid - mixed expressions
}
```

### 9. Array Type Compatibility

**Rule:** Array operations must respect size and element type compatibility.

**Exception:** `TypeMismatchInExpression(<expression>)` or `TypeMismatchInStatement(<statement>)`

**Array Type Rules:**
1. **Size Compatibility:** Arrays of different sizes are incompatible types
2. **Element Type Compatibility:** Element types must match exactly
3. **Literal Assignment:** Array literals must match declared array type
4. **Indexing:** Array indices must be `int` type
5. **Multi-dimensional Arrays:** Each dimension must match exactly

**Array Type Notation:**
- `[T; N]` where `T` is element type and `N` is size
- Examples: `[int; 5]`, `[float; 3]`, `[string; 10]`
- Multi-dimensional: `[[int; 3]; 2]` (2 rows of 3 integers each)

**Examples:**
```hlang
// Size mismatch errors
func sizeMismatchErrors() -> void {
    let arr1: [int; 3] = [1, 2, 3];
    let arr2: [int; 5] = [1, 2, 3, 4, 5];
    let arr3: [int; 1] = [42];
    
    arr1 = arr2;                        // TypeMismatchInStatement - size 5 to size 3
    arr2 = arr1;                        // TypeMismatchInStatement - size 3 to size 5
    arr1 = arr3;                        // TypeMismatchInStatement - size 1 to size 3
    
    // Function parameter size mismatches
    processThreeInts(arr2);             // TypeMismatchInStatement - size 5 to size 3
    processFiveInts(arr1);              // TypeMismatchInStatement - size 3 to size 5
}

// Element type mismatch errors
func elementTypeMismatchErrors() -> void {
    let intArray: [int; 3] = [1, 2, 3];
    let floatArray: [float; 3] = [1.0, 2.0, 3.0];
    let stringArray: [string; 3] = ["a", "b", "c"];
    let boolArray: [bool; 3] = [true, false, true];
    
    intArray = floatArray;              // TypeMismatchInStatement - float array to int array
    floatArray = intArray;              // TypeMismatchInStatement - int array to float array
    stringArray = intArray;             // TypeMismatchInStatement - int array to string array
    boolArray = stringArray;            // TypeMismatchInStatement - string array to bool array
}

// Array literal type errors
func literalTypeErrors() -> void {
    let intArray: [int; 3] = [1, 2.5, 3];      // TypeMismatchInStatement - float in int array
    let floatArray: [float; 3] = [1.0, 2, "3"]; // TypeMismatchInStatement - int and string in float array
    let stringArray: [string; 2] = ["hello", 42]; // TypeMismatchInStatement - int in string array
    let boolArray: [bool; 2] = [true, 1];      // TypeMismatchInStatement - int in bool array
    
    // Size mismatch in literals
    let arr1: [int; 3] = [1, 2];               // TypeMismatchInStatement - 2 elements for size 3
    let arr2: [int; 2] = [1, 2, 3, 4];         // TypeMismatchInStatement - 4 elements for size 2
}

// Array indexing errors
func indexingErrors() -> void {
    let numbers: [int; 5] = [1, 2, 3, 4, 5];
    let floats: [float; 3] = [1.0, 2.0, 3.0];
    let text: [string; 2] = ["hello", "world"];
    
    // Wrong index types
    let result1 = numbers["invalid"];   // TypeMismatchInExpression - string index
    let result2 = numbers[3.14];        // TypeMismatchInExpression - float index
    let result3 = numbers[true];        // TypeMismatchInExpression - bool index
    let result4 = numbers[floats];      // TypeMismatchInExpression - array index
    
    // Assignment to wrong index types
    numbers["0"] = 10;                  // TypeMismatchInStatement - string index in assignment
    floats[2.5] = 1.5;                  // TypeMismatchInStatement - float index in assignment
}

// Multi-dimensional array errors
func multiDimensionalErrors() -> void {
    let matrix2x3: [[int; 3]; 2] = [[1, 2, 3], [4, 5, 6]];
    let matrix3x2: [[int; 2]; 3] = [[1, 2], [3, 4], [5, 6]];
    let floatMatrix: [[float; 3]; 2] = [[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]];
    
    // Dimension size mismatches
    matrix2x3 = matrix3x2;              // TypeMismatchInStatement - different dimensions
    
    // Element type mismatches
    matrix2x3 = floatMatrix;            // TypeMismatchInStatement - float to int elements
    
    // Row assignment errors
    matrix2x3[0] = [1, 2];              // TypeMismatchInStatement - size 2 row to size 3
    matrix2x3[0] = [1.0, 2.0, 3.0];     // TypeMismatchInStatement - float row to int row
    
    // Element assignment errors
    matrix2x3[0][0] = 3.14;             // TypeMismatchInStatement - float to int element
    matrix2x3[0][0] = "text";           // TypeMismatchInStatement - string to int element
}

// Function parameter array errors
func functionParameterErrors() -> void {
    let small: [int; 2] = [1, 2];
    let large: [int; 10] = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
    let floatArr: [float; 5] = [1.0, 2.0, 3.0, 4.0, 5.0];
    
    processFiveInts(small);             // TypeMismatchInStatement - size 2 to size 5
    processFiveInts(large);             // TypeMismatchInStatement - size 10 to size 5
    processFiveInts(floatArr);          // TypeMismatchInStatement - float array to int array
}

// Array return type errors
func returnTypeErrors() -> void {
    let result1: [int; 3] = getFloatArray();    // TypeMismatchInStatement - float array to int array
    let result2: [int; 5] = getThreeInts();     // TypeMismatchInStatement - size 3 to size 5
}

// Complex array compatibility errors
func complexErrors() -> void {
    let matrix: [[int; 2]; 3] = [[1, 2], [3, 4], [5, 6]];
    let differentMatrix: [[int; 3]; 2] = [[1, 2, 3], [4, 5, 6]];
    let floatMatrix: [[float; 2]; 3] = [[1.0, 2.0], [3.0, 4.0], [5.0, 6.0]];
    
    // Nested array assignments
    matrix = differentMatrix;           // TypeMismatchInStatement - different inner dimensions
    matrix = floatMatrix;               // TypeMismatchInStatement - different element types
    
    // Mixed array operations
    let mixed = matrix[0] + differentMatrix[0]; // TypeMismatchInExpression - different array types in operation
}

// Helper functions for testing
func processThreeInts(arr: [int; 3]) -> void {
    print("Processing 3 integers");
}

func processFiveInts(arr: [int; 5]) -> void {
    print("Processing 5 integers");
}

func getFloatArray() -> [float; 3] {
    return [1.0, 2.0, 3.0];
}

func getThreeInts() -> [int; 3] {
    return [1, 2, 3];
}

// Valid array operations
func validOperations() -> void {
    let arr1: [int; 3] = [1, 2, 3];
    let arr2: [int; 3] = [4, 5, 6];
    
    arr1 = arr2;                        // Valid - same type
    arr1[0] = 10;                       // Valid - int to int element
    arr1[1] = arr2[2];                  // Valid - int element to int element
    
    processFiveInts([1, 2, 3, 4, 5]);   // Valid - literal array
    let result = getThreeInts();        // Valid - matching return type
}
```

---

## Implementation Guidelines

### Error Detection Order
When multiple errors could be detected, report the **first** error encountered in **program order** (top-to-bottom, left-to-right).

### Scope Management
- **Global scope:** Constants and functions
- **Function scope:** Parameters and local variables  
- **Block scope:** Variables declared within `{}`
- **Shadowing:** Inner declarations hide outer ones with the same name

### Type System Integration
- **Static typing:** All types must be determined at compile time
- **Type inference:** Limited to obvious cases (literal assignments)
- **Type coercion:** Minimal - only `int` to `float` in arithmetic contexts
- **Array types:** Must match exactly in size and element type


---

*Document prepared for HLang Assignment 3 - Static Semantic Analysis*  
*Last updated: June 2025*