## ----------------------------------------------------------------------------------------------------------
## DP-2 TEMPLATE
## Please DO NOT change the naming convention within this template. Some changes may
## lead to your program not functioning as intended.
import random
import sys
sys.path.append('../')

from Common_Libraries.p2_lib import *

import os
from Common_Libraries.repeat_timer_lib import repeating_timer

def update_sim ():
    try:
        arm.ping()
    except Exception as error_update_sim:
        print (error_update_sim)

arm = q_arm()

update_thread = repeating_timer(2, update_sim)


'''
IBEHS 1P10 - DP-2 Computer Program

Team Number: 45

 (Hydar Zartash, zartashh, 400332624):

Student 2 Details (Kevin Zhang, zhanj390, Student Number):

Date: DEC 01 2020

'''


## STUDENT CODE BEGINS
## ----------------------------------------------------------------------------------------------------------
## Example to rotate the base: arm.rotateBase(90)

#THIS IS PRELIMINARY CODE: WE HAVE YET TO FULLY COMMENT IT.
#ADDITIONALLY, THE TEST CASE MOVES THROUGH 1-6 IN ORDER AS OF RIGHT NOW. THIS WILL BE CHANGED IN THE FINAL VERSION

def move_end_effector(tup): #takes an tuple of (x, y, z) as float
    while True: #infinite loop waits for correct emg input
        time.sleep(1)
        if arm.emg_left() > 0.6 and arm.emg_right() >0.6: #both arms flexed
            arm.move_arm(0.4064, 0.0, 0.4826) #moves to the home position to avoid collision
            time.sleep(2) 
            arm.move_arm(tup[0], tup[1], tup[2]) #moves arm to correct coordinates
            break #only one execution, so leave the loop and function once executed
        else:
            time.sleep(1) #wait if conditions aren't met

def identify_autoclave_bin_location(code):
    #coordinates of each bin, corresponding to codes from project module
    dict = {
        1: (-0.565, 0.2244, 0.419), 
        2: (0.0, -0.6126, 0.4139),
        3: (0.0, 0.6102, 0.4139),
        4: (-0.3736, 0.145, 0.274),
        5: (0.0, -0.4137, 0.274),
        6: (0.0, 0.4137, 0.274)
        }
    return dict[code] #return tuple of float

def control_gripper(grip_angle): #takes an argument of how much to change the angle, (30 for big box and 35 for small)
    while True: #infinite loop waits for correct emg input
        time.sleep(1)
        if arm.emg_left() == 0.0 and arm.emg_right()> 0.6: #if only right arm flexed 
            if arm.g == 0: #checks g attribute of the arm object, (angle of grip in range -1 < g < 46)
                arm.control_gripper(grip_angle) # if grip is open, close it
                break #leave function and loop
            else:
                arm.control_gripper(-1*grip_angle) #if grip is closed, open it
                break #leave function and group
        else:
            pass #do nothing if the conditions aren't met

def open_autoclave(code, open_bin=True):
    while True:
        time.sleep(1)
        if arm.emg_left() > 0.6 and arm.emg_right() == 0.0: 
            if open_bin == True:
                if code == 4:
                    arm.open_red_autoclave(True)
                elif code == 5:
                    arm.open_green_autoclave(True)
                elif code == 6:
                    arm.open_blue_autoclave(True)
                else:
                    pass
                break
            else:
                if code == 4:
                    arm.open_red_autoclave(False)
                elif code == 5:
                    arm.open_green_autoclave(False)
                elif code == 6:
                    arm.open_blue_autoclave(False)
                else:
                    pass
                break
        else:
            pass

'''
To execute the program:
run
the pattern of commads from the user always repeats:
1) move arm (both arms flexed)
2) grip gripper (right arm only flexed)
3) if necessary, open bin (left arm only flexed)
as a user, cycling through these commands in order will complete the task fully
if you input the wrong command, nothing will happen until you put in the right one
'''
def main():
    counter = 0
    while counter <6:
        code = counter+1
        
        if counter > 3:
            grip_angle = 30
        else:
            grip_angle = 35
        arm.spawn_cages(code)
        
        move_end_effector((0.5, 0.0, 0.05))
        time.sleep(3)
        
        control_gripper(grip_angle)
        time.sleep(3)
        
        if code >3:
            open_autoclave(code)
            time.sleep(3)
        
        move_end_effector(identify_autoclave_bin_location(code))
        time.sleep(3)
        
        control_gripper(grip_angle)
        time.sleep(3)
        
        if code > 3:
            open_autoclave(code, False)
            time.sleep(3)

        counter += 1
            

main()
