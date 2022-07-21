from pynput.mouse import Controller
import screeninfo
import random
import time

mouse = Controller()


class MouseMoveRandom:
    def __init__(self):
        monitor = screeninfo.get_monitors()[0]
        self.scale_x = monitor.width
        self.scale_y = monitor.height
        self.abort = False

    def move(self):
        if self.abort:
            return -1
        cur_x, cur_y = mouse.position
        trg_x, trg_y = random.random() * self.scale_x, random.random() * self.scale_y
        steps = max(abs(trg_x - cur_x), abs(trg_y - cur_y))
        step_x, step_y = (trg_x - cur_x) / steps, (trg_y - cur_y) / steps
        for _ in range(int(steps)):
            if self.abort:
                return -1
            temp_x, temp_y = cur_x + step_x, cur_y + step_y
            mouse.position = (int(temp_x), int(temp_y))
            cur_x, cur_y = temp_x, temp_y
            if random.random() > 0.5:
                time.sleep(0.001)
        return 1


if __name__ == '__main__':
    import threading
    import queue

    mm = MouseMoveRandom()
    q = queue.Queue()
    qq = queue.Queue()

    def input_thread():
        while True:
            key = input("Command? continue-[c], pause-p, start-s, quit-q")
            q.put(key)
            if key == "q":
                break

    def action():
        while True:
            try:
                key = q.get(timeout=0.1)
            except:
                key = None
            if key == "p":
                mm.abort = True
            if key == "s":
                mm.abort = False
            if key == "q":
                mm.abort = True
                qq.put(True)
                qq.put(True)
                break

    def move():
        while True:
            mm.move()
            try:
                toquit = qq.get(timeout=0.05)
            except:
                toquit = None
            if toquit is not None:
                break

    p0 = threading.Thread(target=input_thread)
    p1 = threading.Thread(target=action)
    p2 = threading.Thread(target=move)
    p0.start()
    p1.start()
    p2.start()
    qq.get()  # block here
    p0.join()
    p1.join()
    p2.join()
