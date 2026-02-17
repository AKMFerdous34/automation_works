import sys

def define_template(module_name):
  full_module_definition = "module " + module_name + " #(\n //parameter pPARAM_EX \n )\n"
  full_module_definition = full_module_definition + " (\n   input  logic\n  ,input  logic\n  ,output logic\n );\n\n\nendmodule"
  #full_module_definition.append("module " + module_name + " (")
  return full_module_definition
  

  #print(full_module_definition)


def gen_template(module_name):
  full_module_definition = define_template(module_name)
  print (full_module_definition)
  with open(module_name+".sv","w") as file:
    file.write(full_module_definition)


#MAIN PROGRAM:

#define_template("dff")
module_name = sys.argv[1]
gen_template(module_name)

    
