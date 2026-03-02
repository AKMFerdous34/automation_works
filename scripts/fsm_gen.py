import argparse

def parse_argument ():
  '''
  Take the arguments of the fsm states and return them as list
  '''
  parser = argparse.ArgumentParser()   
  parser.add_argument("--state", nargs="+",required=True,help="Add the FSM states as a list for example: \"[state1 state2 state3]\"")
  args = parser.parse_args()  
  states = args.state  
  return states
  #for state_name in states:
  #  print (state_name)



def assign_binary_encoding (state_list):
    '''
    The state lists are taken to generate the corresponding binary state value and also the width of binary. A dictionary relating states to binaries and binary width is returned
    '''
    number_of_states = len(state_list)
    assigned_states = {}
    #print (number_of_states)
    width = max(1,(number_of_states-1).bit_length())
    #print (width)
    for binary,state_name in zip(range (number_of_states+1),state_list):
        #print (state_name + ": " + f"{binary:0{width}b}")
        binary_val = f"{binary:0{width}b}"
        assigned_states[state_name]= binary_val
    #print (assigned_states)
    return assigned_states,width


def gen_fsm_template (assigned_state_list,bin_width):
    '''
    This is the main generation of the template in a Sverilog file.
    '''
    state_list = []
    output_state_list = []
    count = 0
    for states in assigned_state_list.keys():
        state_list.append(states)

    with open ("template_fsm.sv","w") as file: # creates a template file if not present
        file.write("  // Variable declaration \n")
        for state in state_list:
            output_state_list.append (state.lower() + "_state") 
            file.write("  logic " + state.lower() + "_state; \n") # declare variables to be used as output logic to represent the states

        file.write("\n  //State Defintion\n  typedef enum logic [" + str(bin_width-1) + " : 0] {\n")
        for state_name in assigned_state_list:
            if (count < len(state_list)-1):
              file.write(" "*4 + "p" + state_name + " = " + str(bin_width) + "'b" + assigned_state_list.get(state_name) + ",\n") # Declare the states with their binary values
              count = count + 1
            else:
              file.write(" "*4 + "p" + state_name + " = " + str(bin_width) + "'b" + assigned_state_list.get(state_name) + "\n  } all_states;\n\n") # this is the last state.


        file.write("  all_states pstate,nstate;\n\n  //PSR \n  always_ff @ (posedge clk,negedge rst_n) begin //manually set clk and rst to the actual port name \n    if (!rst_n) \n      pstate <= p" + state_list[0] + ";\n    else\n      pstate <= nstate; \n  end \n\n") # PSR generation

        file.write ("  //NSL \n  always_comb begin \n    case (pstate) \n") #NSL Generation
        for state_name in assigned_state_list:
            file.write("      p" +  state_name + ": nstate = ;\n")
        file.write ("      default: nstate = all_states'('bx);\n    endcase\n  end\n\n")


        file.write ("  //State Assignments\n")
        for output_states,state in zip(output_state_list,state_list):
            file.write ("  assign " + output_states + " = (pstate == p" + state + ");\n")
        file.write ("\n  // OL")


                                                                  #######################
                                                                  ##  MAIN FUNCTION    ##
                                                                  #######################
state_list = parse_argument()
assigned_states,bin_width = assign_binary_encoding (state_list)
gen_fsm_template (assigned_states,bin_width)
