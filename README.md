# CSC321_PHY_Phase1
This is the first part of creating the PHY language for Principle of Programming Languages. This is including Tokenization, Parsing, and making test functions for our program.

PHY is a languge to try and help make physics calculations easier for anyone. Since physics has many different variables and formulas this languge it to help make sure to keep track of everything and calculate for the user.

Running Lexer/Parser:
 1. In your CML want to navigate where the Project/PHY-Language is at
 2. Once you are there you want to type: py src/phy.py test/valid1.phy (The tests are named valid1-10.phy OR invalid1-5.phy; You can change the test name to whichever you want to try)

Grammar:
  The grammar for PHY is represented in a way that makes sense with how physics problems are traditionally appraoched.
   <br> &nbsp;&nbsp;&nbsp; program       ::= header? statement*
   <br> &nbsp;&nbsp;&nbsp; header        ::= "givens" "{" assignment* "}"
   <br> &nbsp;&nbsp;&nbsp; statement     ::= assignment | print_stmt
   <br> &nbsp;&nbsp;&nbsp; assignment    ::= ("given" | "let")? type_kw? IDENTIFIER "=" expression ";"
   <br> &nbsp;&nbsp;&nbsp; type_kw       ::= "mass" | "accel" | "velocity" | "length" | "power" | "temp" | "force"
   <br> &nbsp;&nbsp;&nbsp; print_stmt    ::= "print" expression ";"
   <br> &nbsp;&nbsp;&nbsp; expression    ::= term (("+" | "-") term)*
   <br> &nbsp;&nbsp;&nbsp; term          ::= factor (("*" | "/") factor)*
   <br> &nbsp;&nbsp;&nbsp; factor        ::= (NUMBER | TIME) UNIT? | IDENTIFIER | "(" expression ")"

How It Should Look:
  <br> &nbsp;&nbsp;&nbsp; Valid: <br> &nbsp;&nbsp;&nbsp; <img width="389" height="108" alt="image" src="https://github.com/user-attachments/assets/36342121-e493-4202-8062-64060fba47fd" />
  
  <br> &nbsp;&nbsp;&nbsp; Invalid:  &nbsp;&nbsp;&nbsp; <img width="1059" height="52" alt="image" src="https://github.com/user-attachments/assets/f440dd09-eaea-44c8-82af-ac1bcd288b2c" />

