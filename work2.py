# Хэш-значения:
# 1115dd800feaacefdf481f1f9070374a2a81e27880f187396db67958b207cbad - zyzzx
# 3a7bd3e2360a3d29eea436fcfb7e44c735d117c42d1c1835420b6b9942dd4f1b - apple
# 74e1bb62f8dabb8125a58852b63bdf6eaef667cb56ac7f7cdba6d7305c50a22f - mmmmm

import hashlib
import itertools
import string
import time
import threading


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def brute_force_passwords(target_hashes, alphabet, password_length, num_threads, stop_flag):
    start_time = time.time()
    found_passwords = []

    def worker(thread_id):
        nonlocal stop_flag
        total_combinations = len(alphabet) ** password_length
        chunk_size = total_combinations // num_threads
        start_index = thread_id * chunk_size
        end_index = (thread_id + 1) * chunk_size

        for i, password in enumerate(itertools.product(alphabet, repeat=password_length)):
            if i < start_index:
                continue
            if i >= end_index:
                break

            password_str = ''.join(password)
            hashed_password = hash_password(password_str)
            if hashed_password in target_hashes:
                found_passwords.append(password_str)
                print(f"Поток-{thread_id} пароль: {password_str}")
                stop_flag.set()
                break

            if stop_flag.is_set():
                break

    threads = []
    stop_flag = threading.Event()
    for i in range(num_threads):
        thread = threading.Thread(target=worker, args=(i,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Затраченное время: {elapsed_time} секунд")

    return found_passwords


def main():
    alphabet = string.ascii_lowercase
    password_length = 5
    num_threads = int(input("Введите количество потоков: "))
    target_hashes = input("Введите хеш-значение: ")

    found_passwords = brute_force_passwords(target_hashes, alphabet, password_length, num_threads, threading.Event())
    print("Найденные пароли:")
    for password in found_passwords:
        print(password)

    while True:
        qw = input("Начать заново? (Y/N): ")
        if qw == 'N':
            break
        elif qw != 'Y' and 'N':
            print('Введены некорректные символы!')
        elif qw == 'Y':
            main()

if __name__ == "__main__":
    main()