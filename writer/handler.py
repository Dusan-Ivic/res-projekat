import subprocess
from subprocess import Popen

print("        WRITER HANDLER")
print("------------------------------")

user_choice = ''
user_shutdown_choice = ''
writer_counter = -1
list_of_writers = []

while True:
    print("Open Writer                    - Input= open")
    print("Close last open Writer         - Input= close")
    print("Chose which Writer to close    - Input= chose")

    user_choice = input("Input = ")
    print("\n")

    if(user_choice.lower() == 'open'):
        try:
            var = subprocess.Popen('python writer.py', stdout=subprocess.PIPE)
            list_of_writers.insert(writer_counter,var)
            writer_counter += 1
            print(f"Writer No.{writer_counter+1} is up and running.")
        except:
            print("ERR: Writer failed to open.")

    elif(user_choice.lower() == 'close'):
        try:
            list_of_writers[writer_counter].terminate()
            writer_counter -= 1
            print(f"Closing of Writer No.{writer_counter+1} was succesful.")
        except:
            print("ERR Writer failed to close.")

    elif(user_choice.lower() == 'chose'):
        print("ACTIVE WRITERS")
        print("--------------")

        for x in range(writer_counter + 1):
            print(f"Writer {x+1} is active. Shutdown key: {x+1}.")

        print("To shutdown Input: Shutdown key num")
        print("To skip Input: x")

        user_shutdown_choice = input("Input: ")
        print("\n")

        if(user_shutdown_choice.lower() == 'x'):
            continue
        else:
            try:
                list_of_writers[int(user_shutdown_choice)-1].terminate()
                del list_of_writers[int(user_shutdown_choice)-1]
                writer_counter -= 1
                print(f"Closing of Writer No.{user_shutdown_choice} was succesful.")  
            except:
                print("ERR: Writer failed to close or it doesnt exist!")    
    else:
        print("ERR: Operation aborted.Incorrect Input.")