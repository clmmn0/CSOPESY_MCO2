# CSOPESY_MCO2

A Python-based program that uses Counting Semaphore to handle a synchronization problem that allows multiple instances of the same resource to access the critical section. In this project, the supposed task is to create a solution that will manage the number of people inside a fitting room of a department store.

**Project Constraints**
- There are only n slots inside the fitting room of a department store. Thus, there can only be at most n persons inside the fitting room at a time.
- There cannot be a mix of blue and green in the fitting room at the same time. Thus, there can only be at most n blue threads or at most n green threads inside the fitting room at a time.
- The solution should not result in deadlock.
- The solution should not result in starvation. For example, blue threads cannot forever be blocked from entering the fitting room if there are green threads lining up to enter as well.

**Input**
- `n`: number of slots inside the fitting room.
- `b`: number of blue threads
- `g`: number of green threads

To run the program, use the command prompt or use programs like Dev-C++ or Visual Studio Code.

