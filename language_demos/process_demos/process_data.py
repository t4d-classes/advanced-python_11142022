""" process data """

# import threading
import multiprocessing as mp

counter = 0

def increment_counter() -> None:
    """ increment counter """

    global counter

    counter += 1
    print(counter)

def main() -> None:
    """ main """

    process_list = []

    for _ in range(8):
        # the_process = threading.Thread(target=increment_counter)
        the_process = mp.Process(target=increment_counter)
        the_process.start()
        process_list.append(the_process)

    for a_process in process_list:
        a_process.join()

    print(f"final counter: {counter}")

if __name__ == "__main__":
    main()
