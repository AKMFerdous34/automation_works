import re
from pathlib import Path
import readline
import glob
import sys

# Generates a basic testbench that runs clk at 100MHz and starts a basic init
# test

#FUNCTIONS:

# Enable tab completion for file names within the current directory
def complete_path(text, state):
    expanded = os.path.expanduser(os.path.expandvars(text))

    matches = glob.glob(expanded + '*')

    # restore original typed prefix rather than expanded path
    matches = [
        os.path.join(text, os.path.basename(m)) if not m.startswith(text) else m
        for m in matches
    ]

    return matches[state] if state < len(matches) else None
    

    #matches = glob.glob(text + '*')
    #    return matches[state] if state < len(matches) else None

def read_file (file_name):
    '''
    This function will read the file and extract the module name, input and output 
    names using regex, store them in input_names and output_names list.
    '''
    input_vectored_names = []
    output_vectored_names = []
    input_only_names = []
    output_only_names = []
    
    with open(file_name,"r") as file: 
      for line in file:
        # Using regex to detect various patterns
        clock_detect = re.search(r"\b[a-zA-Z_]*clk[a-zA-Z0-9_]*\b", line) # clk
        module_name_detect = re.search(r"module\s+([^\s(]+)",line) # module name
        input_detect = re.search(r"\binput\b(?:\s+(?:logic|wire|reg)\b)?\s+(\[[^\]]+\]\s*[A-Za-z_][A-Za-z0-9_]*|[A-Za-z_][A-Za-z0-9_]*)\b(?=[\s,;]|//|$)",line)#r"input\s*(.*)",line) # inputs
        output_detect = re.search(r"\boutput\b(?:\s+(?:logic|wire|reg)\b)?\s+(\[[^\]]+\]\s*[A-Za-z_][A-Za-z0-9_]*|[A-Za-z_][A-Za-z0-9_]*)\b(?=[\s,;]|//|$)",line) # outputs
        
        # append everything to the lists to be used later in the generation of tb
        if (input_detect):
          input_vectored_names.append(input_detect.group(1).replace(",",""))
          input_only_names.append(re.sub(r"\s*\[[^\]]*\]\s*","",input_detect.group(1)).strip().rstrip(","))
        if(output_detect):
          output_vectored_names.append(output_detect.group(1).replace(",",""))
          output_only_names.append(re.sub(r"\s*\[[^\]]*\]\s*","",output_detect.group(1)).strip().rstrip(","))
        if(module_name_detect):
          module_name = module_name_detect.group(1).replace("(","")
    # extract the clock name from the input list
    for input_components in input_only_names:
        if "clk" in input_components:
          clock_name = input_components

    return input_vectored_names,input_only_names,output_vectored_names,output_only_names,module_name,clock_name


def setup_io (input_names,output_names,module_name):
    '''
    write the module name and IO declaration to the tb file
    '''
    with open (module_name+"_tb.sv","w") as file:
      file.write("module "+module_name+"_tb; \n \n")
      for inputs in input_names:
          file.write("  logic " + str(inputs) + ";\n") # Made a dumb mistake here
      for outputs in output_names:
          file.write("  logic " + str(outputs) + ";\n")

def setup_clock (module_name,clk_speed,clk_name):
    '''
    Setup the clock at desired half period to toggle, to change speed, set in argument in main function
    '''
    with open (module_name+"_tb.sv","a") as file:
        file.write("\n  initial forever #" + str(clk_speed) + " " + str(clk_name) + " = ~" + str(clk_name) + "; \n\n")

def instantiate_module (inputs,outputs,module_name):
    '''
    take an instance of the module
    '''
    all_io = inputs + outputs
    with open (module_name+"_tb.sv","a") as file:
       file.write("  " + module_name + " DUT (\n")
       for ios in all_io:
           if (ios == all_io[-1]):
             file.write(" " * 12 + "." + ios + " ("+ ios + "));\n")
           else:
             file.write(" " * 12 + "." + ios + " (" + ios + ")" ",\n")

def reset_init_seq (input_names,module_name,clk):
    '''
    This function generates a basic reset initialization sequence
    setting all inputs to 0 and running a single posedge clk
    '''
    with open (module_name+"_tb.sv","a") as file:
        file.write("\n  initial begin\n")
        for init_var in input_names:
            file.write("    "+init_var + " <= 'b0;\n")

        file.write(
                   f"    @(posedge " + clk +");"
                   f"\n    // rst_n <= 1'b1;"
                   f"\n    repeat (20) @(posedge " + clk +");"
                   f"\n    $finish;"
                   f"\n  end"
                   f"\n\nendmodule"
                  )



# MAIN PROGRAM:
if __name__ == "__main__":
    #readline.set_completer_delims(' \t\n"\'`@$><=;|&{(')
  #readline.set_completer(complete_path)
  #readline.parse_and_bind("tab: complete")
  #file_path = Path(input("enter file path and name: \n"))
  file_path = sys.argv[1]
  inputs_vec,inputs,outputs_vec,outputs,module_name,clk_name = read_file (file_path)
  setup_io(inputs_vec,outputs_vec,module_name)
  setup_clock(module_name,5,clk_name)
  instantiate_module(inputs,outputs,module_name)
  reset_init_seq(inputs,module_name,clk_name)
