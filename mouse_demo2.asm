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
STORE C1, A

END_MouseISR:
RETURN		# Return to where left (Main)


# Timer ISR, not useful in this demo, so blank
#TIMER_ISR:
#RETURN
