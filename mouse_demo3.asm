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
AND A
