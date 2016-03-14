# //////////////////////////////////////////////////////////////////////////////////
# // Company: University of Edinburgh
# // Engineer: Qisong Wang (s1364207)
# // 
# // Create Date: 01.03.2016 17:58:47
# // Design Name: Mouse_Processor_Demo_Assembly_Program
# // Project Name: Mouse_Processor_Demo
# // Target Devices: Basys3
# // Tool Versions: Self-written Assembler
# // Description: This is the assmebly program that makes a mouse and processor
# //		  demo. It can display (MouseX, MouseY) through 4 7-Seg displays,
# //		  MouseStatus (3 buttons) through rightmost LEDs and NouseZ (scrolling
# //		  wheel) through rightmost 8 LEDs (flowing LEDs)
# // 
# // Dependencies: - Mouse_ISR
# // 
# // Revision:
# // Revision 0.01 - File Created
# // Additional Comments: "python assembler.py" will process this file.
# // 
# //////////////////////////////////////////////////////////////////////////////////

# Main Inifinite Loop
MAIN:

GOTO MAIN



# Mouse Interrupt Service Routine
MOUSE_ISR:

# Connect MouseStatus to Rightmost 3 LEDs
LOAD A, A0	# Load MouseStatus to A
LOAD B, $07	# Load mask 00000111 to B
OR A	        # Save filtered results to A
STORE C0, A	# Store A to Right LEDS


# Connect MouseX to  First 2 7-Seg Displays
LOAD A, A1	# Load MouseX to A
STORE D0, A	# Save A to First 2 7-Seg Displays


# Connect MouseY to Second 2 7-Seg Displays
LOAD A, A2	# Load MouseY to A	
STORE D1, A	# Save A to Second 2 7-Seg Displays


# Connect MouseZ to Leftmost 8 LEDs
# A software implemention of 3-to-8 decoding (flowing leds)
LOAD A, A3	# Load MouseZ to A
LOAD B, $E0	# Load mask 11100000 to B
AND A		# Save the masked result to A
# If A equals 001(00000)
LOAD B, $20
BREQ LED1
# else compare A with 010(00000)
LOAD B, $40
BREQ LED2
# else compare A with 011(00000)
LOAD B, $60
BREQ LED2
# else compare A with 100(00000)
LOAD B, $80
BREQ LED2
# else compare A with 101(00000)
LOAD B, $A0
BREQ LED2
# else compare A with 110(00000)
LOAD B, $C0
BREQ LED2
# else compare A with 111(00000)
LOAD B, $E0
BREQ LED2
# else turn off LED C1
LOAD A, $00
STORE C1, A
GOTO END_MouseISR

LED1:	# Turn on LED 1 of C1
LOAD A, $01
STORE C1, A
GOTO END_MouseISR

LED2:	# Turn on LED 2 of C1
LOAD A, $02
STORE C1, A
GOTO END_MouseISR

LED3:	# Turn on LED 3 of C1
LOAD A, $04
STORE C1, A
GOTO END_MouseISR

LED4:	# Turn on LED 4 of C1
LOAD A, $08
STORE C1, A
GOTO END_MouseISR

LED5:	# Turn on LED 5 of C1
LOAD A, $10
STORE C1, A
GOTO END_MouseISR

LED6:	# Turn on LED 6 of C1
LOAD A, $20
STORE C1, A
GOTO END_MouseISR

LED7:	# Turn on LED 7 of C1
LOAD A, $40
STORE C1, A
GOTO END_MouseISR

LED8:	# Turn on LED 8 of C1
LOAD A, $80
STORE C1, A
GOTO END_MouseISR


END_MouseISR:
RETURN		# Return to where left (Main)


# Timer ISR, not useful in this demo, so blank
TIMER_ISR:
RETURN
