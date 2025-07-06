import threading
import time
import os

FILE_PATH = "file_changes.txt"

def show_changes(old, new):
    old_lines = old.splitlines()
    new_lines = new.splitlines()

    for i, line in enumerate(new_lines):
        if i>=len(old_lines) or line != old_lines[i]:
            print(f"Line {i+1} changed or added : {line}")
        if len(old_lines) > len(new_lines):
            print("Lines were removed.")

def watch_file(file_path):
    print(f"Wactching {file_path} for changes.....")
    last_modified = os.path.getmtime(file_path)

    with open(file_path, 'r') as file:
        old_content = file.read()

    while True:
        time.sleep(5)
        try:
            current_modified = os.path.getmtime(file_path)
            if current_modified != last_modified:
                last_modified = current_modified
                with open(file_path, 'r') as file:
                    new_content = file.read()
                print("File changed!!!")

                show_changes(old_content, new_content)
                old_content = new_content

        except Exception as e:
            print(f"Issue : {e}")

# function 1
watcher_thread = threading.Thread(target=watch_file, args=(FILE_PATH,), daemon=True)
watcher_thread.start()
# function 3

try :
      while True:
        print("Main Thread is running....")
        a = int(input("Please enter value : "))
        print(a + 100)
        time.sleep(5)
        
        
except Exception as e :    
    print(f"Exception occured : {e}")
    print("Exiting gracefully.")