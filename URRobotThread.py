import urx
import UI
import UartProtocolParseThread
from queue import Queue

from time import sleep
from threading import Thread, Lock

stateMachine = ""
task_num = 0
task_sub_step = 0


class URRobotThread(Thread):
    def __init__(self):
        print("URRobotThread.__init__")
        Thread.__init__(self)
        self.rob = urx.Robot("192.168.1.100")
        # UI.my_print(self.rob._dict)
        
    def run(self):
        print("URRobotThread.run")
        global stateMachine, task_num, task_sub_step

        task_list = [
            ["wait_start_btn", "move_z", "move_x", "move_y", "send_message", "wait_message","move_z", "send_message",
             "wait_message", "task_end"],

            ["move_x", "send_message", "wait_message", "send_message", "wait_message", "move_z", "send_message",
             "wait_message", "send_message", "wait_message", "move_z", "send_message", "wait_message", "move_x",
             "move_y", "task_end"],

            ["move_x", "send_message", "wait_message", "send_message", "wait_message", "move_z", "send_message",
             "wait_message", "send_message", "wait_message", "move_z", "send_message", "wait_message", "move_x",
             "move_y", "task_end"],

            ["move_x", "send_message", "wait_message", "move_y", "move_x", "move_y", "send_message", "wait_message",
             "send_message", "wait_message", "task_end"],

            ["move_x", "send_message", "wait_message", "move_z", "send_message", "wait_message", "move_y", "task_end"]]

        message_list = [
            ["", "", "", "", "StartDecline", "downReply_StartDecline", "", "CompleteDecline", "downSend_TaskComplete", ""],

            ["", "StartPrepare", "downSend_PrepareComplete", "StartGrab", "downSend_GrabComplete", "", "LiftComplete",
             "downSend_RequestDecline", "StartDecline", "downReply_StartDecline", "", "CompleteDecline", "downSend_TaskComplete",
             "", "", ""],

            ["", "StartPrepare", "downSend_PrepareComplete", "StartGrab", "downSend_GrabComplete", "", "LiftComplete",
             "downSend_RequestDecline", "StartDecline", "downReply_StartDecline", "", "CompleteDecline", "downSend_TaskComplete",
             "", "", ""],

            ["", "HandInteraction", "downSend_RequestDecline", "", "", "", "StartDecline", "downReply_StartDecline",
             "CompleteDecline", "downSend_TaskComplete",""],

            ["", "StartDecline", "downReply_StartDecline", "", "CompleteDecline", "downSend_TaskComplete", "", ""],
            ]

        position_list = [
            [[0, 0, 0, 0, 0, 0], [0, 0, 0.267, 0, 0, 0], [0.139, 0, 0, 2.234, -0.028, -2.232], [0, -0.319, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0], [0, 0, 0.117, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]],

            [[0.039, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0],
             [0, 0, 0.267, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0],
             [0, 0, 0.117, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0.139, 0, 0, 0, 0, 0], [0, -0.469, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0]],

            [[0.039, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0],
             [0, 0, 0.267, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0],
             [0, 0, 0.117, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0.139, 0, 0, 0, 0, 0], [0, -0.629, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0]],

            [[-0.120, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, -0.629, 0, 0, 0, 0], [0.139, 0, 0, 0, 0, 0],
             [0, -0.319, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]],

            [[0.139, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0.117, 0, 0, 0], [0, 0, 0, 0, 0, 0],
             [0, -0.469, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]],
                         ]

        hand_y_left_limit = -0.569
        hand_y_right_limit = -0.689
        y0 = -0.319
        y1 = -0.469
        y2 = -0.629
        task_num_break = 0

        a = 0.05
        v0 = 0.02
        v1 = 0.05
        v2 = 0.2
        direction = 0
        zMoveDirection = 0

        lastmoveSource = 0
        moveSource = 0
        enableMove = 0

        UI.stateMachine_Lock.acquire()
        stateMachine = task_list[task_num][task_sub_step]
        UI.stateMachine_Lock.release()
        
        current_point = self.rob.getl()
        target_point = [current_point[0],current_point[1],current_point[2],current_point[3],current_point[4],current_point[5]]
        source_point = [current_point[0],current_point[1],current_point[2],current_point[3],current_point[4],current_point[5]]

        while UI.quitApplication == 0:
            UI.stateMachine_Lock.acquire()
            status = stateMachine
            UI.stateMachine_Lock.release()

            this_message = ""
            UartProtocolParseThread.receiveMessageQueue_lock.acquire()
            if not UartProtocolParseThread.receiveMessageQueue.empty():
                this_message = UartProtocolParseThread.receiveMessageQueue.get()
            UartProtocolParseThread.receiveMessageQueue_lock.release()

            if this_message == "downSend_FallDown":
                if task_num == 1 or task_num == 2:
                    self.rob.stopl(acc=a)
                    if UartProtocolParseThread.someThing == 1:
                        UI.displayPictureName = "Dropped"
                    task_num_break = task_num
                    task_num = 4
                    task_sub_step = 0
                    status = task_list[task_num][task_sub_step]
                    UI.my_print("wait_message << downSend_FallDown_0")

            if status == "move_z":
                current_point = self.rob.getl()
                target_point = [current_point[0],current_point[1],current_point[2],current_point[3],current_point[4],current_point[5]]
                target_point[2] = position_list[task_num][task_sub_step][2]  # z change var
                
                if target_point[2] > current_point[2]:  # lift
                    v = 0.01 # v0                              # slow lift
                    zMoveDirection = 1
                    a = 0.1
                    source_point = current_point
                else:
                    a = 0.05
                    v = v1                              # fast down
                    zMoveDirection = -1

                self.rob.movel(target_point, acc=a, vel=v, wait=False)
                status = "wait_move_z"
                
            elif status == "wait_move_z":
                current_point = self.rob.getl()
                if zMoveDirection == 1:                             # lift
                    if current_point[2] - source_point[2] > 0.03:   # lift 2 cm
                        zMoveDirection = 0
                        self.rob.movel(target_point, acc=a, vel=v1, wait=False) # fast lift
                if abs(current_point[2] - target_point[2]) < 0.001:
                    task_sub_step += 1
                    status = task_list[task_num][task_sub_step]
                    a = 0.05
                             
            elif status == "change_pose":
                current_point = self.rob.getl()
                target_point = current_point
                target_point[2] = 0.117
                target_point[3] = position_list[task_num][task_sub_step][3]
                target_point[4] = position_list[task_num][task_sub_step][4]
                target_point[5] = position_list[task_num][task_sub_step][5]
                
                self.rob.movel(target_point, acc=a, vel=v1, wait=False)
                status = "wait_change_pose"

            elif status == "wait_change_pose":
                current_point = self.rob.getl()
                if abs(current_point[3] - target_point[3]) < 0.001 and abs(current_point[4] - target_point[4]) < 0.001 and abs(current_point[5] - target_point[5]) < 0.001:
                    task_sub_step += 1
                    status = task_list[task_num][task_sub_step]
            
            elif status == "move_x":
                current_point = self.rob.getl()
                target_point = current_point
                target_point[0] = position_list[task_num][task_sub_step][0]  # x change var

                #####################################################################
                if task_num == 0 and task_sub_step == 2:            # change pose
                    target_point[3] = position_list[task_num][task_sub_step][3]
                    target_point[4] = position_list[task_num][task_sub_step][4]
                    target_point[5] = position_list[task_num][task_sub_step][5]
                #####################################################################

                self.rob.movel(target_point, acc=a, vel=v2, wait=False)
                status = "wait_move_x"

            elif status == "wait_move_x":
                current_point = self.rob.getl()
                if abs(current_point[0] - target_point[0]) < 0.001:
                    task_sub_step += 1
                    status = task_list[task_num][task_sub_step]
            
            elif status == "move_y":
                current_point = self.rob.getl()
                target_point = current_point
                target_point[1] = position_list[task_num][task_sub_step][1]  # y change var
                if task_num_break == 1:
                    target_point[1] = y1
                if task_num_break == 2:
                    target_point[1] = y2
                
                self.rob.movel(target_point, acc=a, vel=v2, wait=False)
                status = "wait_move_y"

            elif status == "wait_move_y":
                current_point = self.rob.getl()
                if abs(current_point[1] - target_point[1]) < 0.001:
                    task_sub_step += 1
                    status = task_list[task_num][task_sub_step]

            elif status == "wait_start_btn":
                if UI.runState == 1:
                    current_point = self.rob.getl()
                    task_sub_step += 1
                    status = task_list[task_num][task_sub_step]
                    
            elif status == "UI_Stop":
                self.rob.stopl(acc = a)
                task_num = 0
                task_sub_step = 0
                status = task_list[task_num][task_sub_step]
                current_point = self.rob.getl()
                UI.my_print(status)

            elif status == "send_message":
                UI.send_lock.acquire()
                cmd = UI.sendMessageQueue.put(message_list[task_num][task_sub_step])
                UI.send_lock.release()

                task_sub_step += 1
                status = task_list[task_num][task_sub_step]

            elif status == "wait_message":

                if task_num == 3:
                    UartProtocolParseThread.moveSourceLock.acquire()
                    moveSource = UartProtocolParseThread.moveSource
                    UartProtocolParseThread.moveSource = 0
                    UartProtocolParseThread.moveSourceLock.release()
		                
                    current_point = self.rob.getl()
                    # UI.my_print(" lastmoveSource : " + str(lastmoveSource) + " moveSource : " + str(moveSource) + " enableMove: " + str(enableMove) + "  current_point[1] : " + str(current_point[1]))
		                
                    if lastmoveSource == 0 or lastmoveSource == 2:
                        enableMove = 1
                    else:
                        if moveSource == 1:
                            enableMove = 1
                        else:
                            enableMove = 0
                        current_point = self.rob.getl()
                        if direction == 1:
                            if abs(current_point[1] - hand_y_right_limit) < 0.001:
                                moveSource = 0
                        if direction == -1:
                            if abs(current_point[1] - hand_y_left_limit) < 0.001:
                                moveSource = 0

                    if lastmoveSource != moveSource:
                        lastmoveSource = moveSource           

                if this_message == message_list[task_num][task_sub_step]:
                    UI.my_print("wait_message << << " + message_list[task_num][task_sub_step])
                    task_sub_step += 1
                    status = task_list[task_num][task_sub_step]
                    if this_message == "downSend_GrabComplete":
                        UI.displayPictureName = "Stable"

                elif this_message == "downReply_StartPrepare":
                    UI.my_print("wait_message << downReply_StartPrepare")
                elif this_message == "downSend_PrepareGrabDemo":
                    UI.my_print("wait_message << downSend_PrepareGrabDemo")
                elif this_message == "downSend_PrepareComplete":
                    UI.displayPictureName = "Nothing"
                    UI.my_print("wait_message << downSend_PrepareComplete")
                elif this_message == "downReply_StartGrab":
                    UI.displayPictureName = "Grabbing"
                    UI.my_print("wait_message << downReply_StartGrab")
                elif this_message == "downSend_GripperState":
                    if UartProtocolParseThread.someThing == 1:  # gripperDistance
                        UI.displayPictureName = "Something"
                    else:  # gripperDistance
                        UI.displayPictureName = "Nothing"
                    UI.my_print("wait_message << downSend_GripperState")
                elif this_message == "downSend_GrabComplete":
                    UI.my_print("wait_message << downSend_GrabComplete")
                    UI.displayPictureName = "Stable"
                elif this_message == "downSend_Shrink":
                    #UI.displayPictureName = "Stable"
                    UI.my_print("wait_message << downSend_Shrink")
                elif this_message == "downSend_Stable":
                    #UI.displayPictureName = "Stable"
                    UI.my_print("wait_message << downSend_Stable")
                elif this_message == "downSend_loosen":
                    #UI.displayPictureName = "Stable"
                    UI.my_print("wait_message << downSend_loosen")
                elif this_message == "downSend_FallDown":
                    UI.my_print("wait_message << downSend_FallDown_1")
                elif this_message == "downSend_RequestDecline":
                    UI.my_print("wait_message << downSend_RequestDecline")
                elif this_message == "downReply_StartDecline":
                    UI.my_print("wait_message << downReply_StartDecline")
                elif this_message == "downReply_CompleteDecline":
                    UI.my_print("wait_message << downReply_CompleteDecline")
                elif this_message == "downSend_GripperOpenComplete":
                    UI.my_print("wait_message << downSend_GripperOpenComplete")
                # 没有物品时的任务结束
                elif this_message == "downSend_TaskComplete":   # exception complete
                    UI.my_print("wait_message << downSend_TaskComplete")
                    if task_num == 1 or task_num == 2:
                        task_sub_step = 13
                        status = task_list[task_num][task_sub_step]
                elif this_message == "downReply_UIStop":
                    UI.my_print("wait_message << downReply_UIStop")
                elif this_message == "downReply_HandInteraction":
                    UI.my_print("wait_message << downReply_HandInteraction")
                elif this_message == "downReply_MutualCapacitanceClean":
                    UI.my_print("wait_message << downReply_MutualCapacitanceClean")
                
                elif this_message == "downSend_MoveLeft":
                    if enableMove == 1:
                        if direction != -1:
                            direction = -1
                            current_point = self.rob.getl()
                            target_point = current_point
                            target_point[1] = hand_y_left_limit
                            self.rob.movel(target_point, acc=a, vel=v0, wait=False)
                            UI.my_print("wait_message << downSend_MoveLeft :: target " + stateMachine + " >> " + " ".join(map(str,target_point)))

                elif this_message == "downSend_MoveRight":
                    if enableMove == 1:
                        if direction != 1:
                            direction = 1
                            current_point = self.rob.getl()
                            target_point = current_point
                            target_point[1] = hand_y_right_limit  # y change var
                            self.rob.movel(target_point, acc=a, vel=v0, wait=False)
                            UI.my_print("wait_message << downSend_MoveRight :: target " + stateMachine + " >> " + " ".join(map(str,target_point)))

                elif this_message == "downSend_HandStop":
                    if enableMove == 1:
                        if direction != 0:
                            self.rob.stopl(acc=a)
                            direction = 0
                            current_point = self.rob.getl()
                            UI.my_print("wait_message << downSend_HandStop :: current " + stateMachine + " >> " + " ".join(map(str,target_point)))

                elif this_message == "downSend_NoHandStop":
                    if enableMove == 1:
                        if direction != 0:
                            self.rob.stopl(acc=a)
                            direction = 0
                            current_point = self.rob.getl()
                            UI.my_print("wait_message << downSend_NoHandStop :: current " + stateMachine + " >> " + " ".join(map(str,target_point)))

            elif status == "task_end":
                if task_num == 4:
                    task_num = task_num_break + 1
                else:
                    task_num += 1
                if task_num > 3:
                    task_num = 1
                task_sub_step = 0
                if task_num == 0:
                    task_sub_step = 1
                task_num_break = 0
                status = task_list[task_num][task_sub_step]
                current_point = self.rob.getl()
                UI.my_print("task_end " + status + " >> " + " ".join(map(str,target_point)))

            UI.stateMachine_Lock.acquire()
            if stateMachine == "Btn_UI_Stop":
                stateMachine = "UI_Stop"
            else:
                stateMachine = status
            UI.stateMachine_Lock.release()

            sleep(0.001)
        self.rob.close()
        print("UartReceiveThread quit")
        