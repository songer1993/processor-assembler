# processor-assembler
# Use
###python assembler.py -i input_file -o output_file

# Instruction Table
#------------------------------------------------------
###Load R, M 		           -> 0000000r, mmmmmmmm
###STORE M, R 		          -> 0000001r, mmmmmmmm
###ADD R 		               -> 0000010r
###SUB R 		               -> 0001010r
###MUTIPLY R              -> 0010010r
### SHIFT_LEFT R          -> 0011010r
### SHIFT_RIGHT R         -> 0100010r
### INCREMENT R           -> 0101010r
### DECREMENT R           -> 0110010r
### IS_EQUAL R            -> 0111010r
### GREATER_THAN R        -> 1000010r
### LESS_THAN R           -> 1001010r
### AND R                 -> 1010010r
### OR R                  -> 1011010r
### XOR R                 -> 1100010r
### BREQ A                -> 10010110, aaaaaaaa
### BRTQ A                -> 10100110, aaaaaaaa
### BLTQ A                -> 10110110, aaaaaaaa
### GOTO A                -> 00000111, aaaaaaaa
### GOTO_IDLE             -> 00001000
### FUNCTION_CALL A       -> 00001001, aaaaaaaa
### RETURN                -> 00001010
### DEREFERENCE R         -> 00001011+r
