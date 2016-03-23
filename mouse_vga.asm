# //////////////////////////////////////////////////////////////////////////////////
# // Company: University of Edinburgh
# // Engineer: Qisong Wang (s1364207)
# //
# // Create Date: 01.03.2016 17:58:47
# // Design Name: Mouse_VGA_Demo_Assembly_Program
# // Project Name: Mouse_VGA_Demo
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

# //////////////////////////////////////////////////////////////////////////////////
# Label inputs and outputs
# //////////////////////////////////////////////////////////////////////////////////
# Mouse Inputs
IN  A0 MOUSE_STATUS
IN  A1 MOUSE_X
IN  A2 MOUSE_Y
IN  A3 MOUSE_Z

# LED Outputs
OUT C0 LED_RIGHT
OUT C1 LED_LEFT

# SEVEN SEGMENT DISPLAYS
OUT D0 SEG_LEFT
OUT D1 SEG_RIGHT

# VGA outputs
OUT B0 VGA_X
OUT B1 VGA_Y
OUT B2 COLOUR1
OUT B3 COLOUR2


# //////////////////////////////////////////////////////////////////////////////////
# Main Program: Inifinite idle loop
# //////////////////////////////////////////////////////////////////////////////////
MAIN:

GOTO MAIN

# //////////////////////////////////////////////////////////////////////////////////
# Mouse Interrupt Service Routine
# //////////////////////////////////////////////////////////////////////////////////
MOUSE_ISR: # Connect MouseStatus to Rightmost 3 LEDs
LOAD  A, MOUSE_STATUS	# Load MouseStatus to A
LOAD  B, $07		# Load mask 00000111 to B
AND   A	    		# Save filtered results to A
WRITE A, LED_RIGHT	# WRITE A to Right LEDS


# Load MouseX and MouseY to register A and B
LOAD  A, MOUSE_X	# Load MouseX to A
LOAD  B, MOUSE_Y	# Load MouseY to B

# Connect MouseX and MouseY to 7-Seg Displays
WRITE A, SEG_LEFT	# Save A to First 2 7-Seg Displays
WRITE B, SEG_RIGHT	# Save B to Second 2 7-Seg Displays
# Connect MouseX to MouseY to VGA Display
WRITE A, VGA_X	# Save A to First 2 7-Seg Displays
WRITE B, VGA_Y	# Save B to Second 2 7-Seg Displays

# Set mouse and background colour
LOAD A, $00
WRITE A, COLOUR1
LOAD A, $FF
WRITE A, COLOUR2


# Connect MouseZ to Leftmost 8 LEDs
# A software implemention of 3-to-8 decoding (flowing leds)
LOAD  A, MOUSE_Z	# Load MouseZ to A
LOAD  B, $E0		# Load mask 11100000 to B
AND   A			# Save the masked result to A
# If A equals 000(00000)
LOAD  B, $00
BREQ  LED1
# else compare A with 001(00000)
LOAD  B, $20
BREQ  LED2
# else compare A with 010(00000)
LOAD  B, $40
BREQ  LED3
# else compare A with 011(00000)
LOAD  B, $60
BREQ  LED4
# else compare A with 100(00000)
LOAD  B, $80
BREQ  LED5
# else compare A with 101(00000)
LOAD  B, $A0
BREQ LED6
# else compare A with 110(00000)
LOAD  B, $C0
BREQ  LED7
# else compare A with 111(00000)
LOAD  B, $E0
BREQ  LED8
# else turn off LED C1
LOAD  A, $00
WRITE A, LED_LEFT
GOTO  END_MouseISR

LED1:	# Turn on LED 1 of C1
LOAD  A, $01
WRITE A, LED_LEFT
GOTO  END_MouseISR

LED2:	# Turn on LED 2 of C1
LOAD  A, $02
WRITE A, LED_LEFT
GOTO  END_MouseISR

LED3:	# Turn on LED 3 of C1
LOAD  A, $04
WRITE A, LED_LEFT
GOTO  END_MouseISR

LED4:	# Turn on LED 4 of C1
LOAD  A, $08
WRITE A, LED_LEFT
GOTO  END_MouseISR

LED5:	# Turn on LED 5 of C1
LOAD  A, $10
WRITE A, LED_LEFT
GOTO  END_MouseISR

LED6:	# Turn on LED 6 of C1
LOAD  A, $20
WRITE A, LED_LEFT
GOTO  END_MouseISR

LED7:	# Turn on LED 7 of C1
LOAD  A, $40
WRITE A, LED_LEFT
GOTO  END_MouseISR

LED8:	# Turn on LED 8 of C1
LOAD  A, $80
WRITE A, LED_LEFT
GOTO  END_MouseISR


END_MouseISR:
RETURN		# Return to where left (Main)


# Timer ISR, not useful in this demo, so blank
TIMER_ISR:
RETURN
