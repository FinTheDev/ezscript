# EZScript Language Specification (v0.1 Draft)

## 1. Overview

EZScript is a lightweight interpreted programming language designed for integration with NoobOS.
It emphasizes simplicity, readability, and tight system-level integration.

Programs execute from top to bottom.

## 2. Basic Example

```ez
print("Hello, NoobOS!")
```

## 3. Data Types (v0.1)

EZScript supports the following primitive types:

- int — integer numbers
- string — text values
- bool — boolean values (true or false)

Example:

```ez
x = 10
name = "fin"
active = true
```

## 4. Variables

Syntax:

```ez
<identifier> = <expression>
```

Example:

```ez
score = 42
```

## 5. Expressions

Supported arithmetic operators:

```ez
+  -  *  /
```

Comparison operators:

```ez
==  !=  <  >  <=  >=
```

Example:

```ez
result = 5 + 3 * 2
```

## 6. Built-in Functions (v0.1)

```ez
print(value)
```

Outputs a value to standard output.

Example:

```ez
print("Hello")
```

## 7. Comments

Single-line comments use the # symbol.

```ez
# This is a comment
x = 5
```

## 8. Execution Model (Planned)

EZScript will compile to bytecode executed by a virtual machine integrated into NoobOS.
