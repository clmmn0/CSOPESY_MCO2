import threading
import random


"""
A class used to define a thread

Attributes:
color (string) - contains color of the thread ("Blue" or "Green")
thread_id (int) - contains the id of the thread
thread (Thread) - contains the actual thread
"""
class colored_thread():
    def __init__(self, color, thread_id):
        self.color = color
        self.thread_id = int(thread_id)
        self.thread = threading.Thread(target=print_threads, args=(self.color, self.thread_id))


"""
A method for printing the color and their corresponding thread id.

Parameters:
color (string) - contains color of the thread ("Blue" or "Green")
thread_id (int) - contains the id of the thread
"""
def print_threads(color, thread_id):
    maxThreads.acquire()
    print(color + " ID #" + str(thread_id))
    maxThreads.release()


"""
A method for executing blue threads.

Parameters:
blue_threads (list) - contains Blue colored_threads
"""
def blue_threading(blue_threads):
    global n, b, g
    global bReady, gReady
    global nInside, gCounter, bCounter
    global currColor
    thread_id = blue_threads[0].thread_id

    # Checks if the blue thread with a specific ID number is ready to execute
    if bReady[thread_id] == True:
        blue.acquire()
        if nInside == 0:
            print("Blue only")

        # Thread starts executing here
        for i in range(n):
            if b > 0:
                blue_threads[0].thread.start()
                blue_threads.pop(0)
                b -= 1
                nInside += 1

        # Checks if the fitting room has maxed its capacity and there are still green threads remaining. If true, green threads will be allowed to enter next
        if nInside == n and g > 0:
            for i in range(n):
                if i + gCounter < len(gReady):
                    gReady[i + gCounter] = True

            nInside = 0
            currColor = "Green"
            gCounter += n
            print("Empty fitting room\n")


        # Checks if the fitting room has maxed its capacity, and only blue threads are remaining. If true, blue threads will be allowed to enter again
        elif nInside == n and g <= 0 and b > 0:
            for i in range(n):
                if i + bCounter < len(bReady):
                    bReady[i + bCounter] = True

            nInside = 0
            currColor = "Blue"
            bCounter += n
            print("Empty fitting room\n")

        # Checks if blue threads are finished and there are still remaining green threads. If true, green threads will be allowed to enter next
        elif b <= 0 and g > 0:
            for i in range(g):
                if i + gCounter < len(gReady):
                    gReady[i + gCounter] = True

            nInside = 0
            currColor = "Green"
            gCounter += g
            print("Empty fitting room\n")

        # Checks if both threads have ended
        elif b <= 0 and g <= 0:
            nInside = 0
            currColor = "END"
            print("Empty fitting room\n")

        blue.release()


"""
A method for executing green threads.

Parameters:
green_threads (list) - contains Green colored_threads
"""
def green_threading(green_threads):
    global n, b, g
    global bReady, gReady
    global nInside, gCounter, bCounter
    global currColor
    thread_id = green_threads[0].thread_id

    # Checks if the green thread with a specific ID number is ready to execute
    if gReady[thread_id] == True:
        green.acquire()
        if nInside == 0:
            print("Green only")

        # Thread starts executing here
        for i in range(n):
            if g > 0:
                green_threads[0].thread.start()
                green_threads.pop(0)
                g -= 1
                nInside += 1

        # Checks if the fitting room has maxed its capacity and there are still blue threads remaining. If true, blue threads will be allowed to enter next
        if nInside == n and b > 0:
            for i in range(n):
                if i + bCounter < len(bReady):
                    bReady[i + bCounter] = True

            nInside = 0
            currColor = "Blue"
            bCounter += n
            print("Empty fitting room\n")

        # Checks if the fitting room has maxed its capacity and only green threads are remaining. If true, green threads will be allowed to enter again
        elif nInside == n and b <= 0 and g > 0:
            for i in range(n):
                if i + gCounter < len(gReady):
                    gReady[i + gCounter] = True

            nInside = 0
            currColor = "Green"
            gCounter += n
            print("Empty fitting room\n")

        # Checks if green threads are finished and there are still remaining blue threads. If true, blue threads will be allowed to enter next
        elif g <= 0 and b > 0:
            for i in range(b):
                if i + bCounter < len(bReady):
                    bReady[i + bCounter] = True

            nInside = 0
            currColor = "Blue"
            bCounter += b
            print("Empty fitting room\n")

        # Checks if both threads have ended
        elif g <= 0 and b <= 0:
            nInside = 0
            currColor = "END"
            print("Empty fitting room\n")

        green.release()


def main():
    global n, b, g, nInside
    nInside = 0

    # Accepts input from user
    n = int(input('Enter the number of slots inside the fitting room: '))
    b = int(input('Enter the number of blue threads: '))
    g = int(input('Enter the number of green threads: '))

    # Initializes the semaphores
    global maxThreads, blue, green
    maxThreads = threading.BoundedSemaphore(n)
    blue = threading.Semaphore()
    green = threading.Semaphore()

    global bReady, gReady
    bReady = []
    gReady = []

    # Sets all values of bReady and gReady to "False" to ensure that no threads will enter the critical section unless it is their turn
    for i in range(b):
        bReady.append(False)
    for i in range(g):
        gReady.append(False)


    # Randomly sets the first color to enter the thread
    random_color = random.randint(0, 1)

    global bCounter, gCounter
    global currColor

    # Prepares all threads that will enter the critical section depending on which color was picked on the randomizer above
    if (random_color == 0 and b > 0) or (random_color == 1 and g <= 0):
        currColor = "Blue"
        bCounter = n
        gCounter = 0
        for i in range(n):
            if i < b:
                bReady[i] = True
    elif (random_color == 1 and g > 0) or (random_color == 0 and b <= 0):
        currColor = "Green"
        gCounter = n
        bCounter = 0
        for i in range(n):
            if i < g:
                gReady[i] = True

    # Initializes the threads
    global blue_threads, green_threads
    blue_threads = []
    green_threads = []

    for i in range(b):
        blue_threads.append(colored_thread("Blue", i))
    for i in range(g):
        green_threads.append(colored_thread("Green", i))


    # Processing of the blue and green threads happens here
    while b > 0 or g > 0:
        if currColor == "Blue":
            blue_threading(blue_threads)
        elif currColor == "Green":
            green_threading(green_threads)


if __name__ == "__main__":
    main()