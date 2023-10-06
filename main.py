from utils.read_file import read_from_file
import time

start_time = time.time()
if __name__ == "__main__":
    board = read_from_file("input1.txt")
    board.print()

end_time = time.time()
print("The time of execution of above program is :",
      (end_time - start_time) * 10 ** 3, "ms")