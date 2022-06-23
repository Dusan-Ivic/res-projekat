import subprocess
from subprocess import Popen

print("        WRITER HANDLER")
print("------------------------------")

user_choice = ''
user_shutdown_choice = ''
writer_counter = -1
list_of_writers = []

def check_input_data(input_value):
    input_value_formated = input_value.lower()
    if(input_value_formated != 'open' and input_value_formated != 'close' and input_value_formated != 'choose'):
        raise TypeError("Input not supported")
    return input_value_formated

def check_input_data_branching(input_value):
    if(isinstance(input_value,int)):
        if(int(input_value) < 0):
            raise TypeError("ERR negative number")
        if(int(input_value) > 400):
            raise TypeError("ERR number too large")
        if(int(input_value) == 0):
            return input_value
        if(int(input_value) > 0 and int(input_value) < 400 ):
            return input_value
    raise TypeError("Unknow input")

if __name__ == "__main__":  # pragma: no cover

    while True: 
        print("Open Writer                    - Input= open")
        print("Close last open Writer         - Input= close")
        print("Choose which Writer to close    - Input= choose")

        user_choice = (input("Input = ")) 
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
                del list_of_writers[int(writer_counter)]
                print(f"Closing of Writer No.{writer_counter+1} was succesful.")
                writer_counter -= 1
            except:
                print("ERR Writer failed to close.")

        elif(user_choice.lower() == 'choose'):
            print("ACTIVE WRITERS")
            print("--------------")

            for x in range(writer_counter + 1):
                print(f"Writer {x+1} is active. Shutdown key: {x+1}.")

            print("To shutdown Input: Shutdown key num")
            print("To skip Input: 0")

            user_shutdown_choice = (input("Input: "))
            print("\n")

            if(user_shutdown_choice.lower() == '0'):
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
    
