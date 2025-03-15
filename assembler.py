##Name: Anthony Eryan
##Pledge: I pledge my honor that I have abided by the Stevens Honor System. 
import os

def parse_register(reg_str): 
    reg = reg_str.strip().upper()
    if not reg.startswith('X') or not reg[1:].isdigit() or int(reg[1:]) > 3:
        raise ValueError(f"Invalid register: {reg_str}")
    return reg

def parse_immediate(imm_str):
    if not imm_str.isdigit():
        raise ValueError(f"Invalid immediate value: {imm_str}")
    return int(imm_str)

def generate_binary(instruction):
    try:
        opcode = ""
        write_reg = ""
        read_reg1 = ""
        read_reg2 = ""
        immediate = None
        
        instruction = instruction.strip().upper()
        
        opcodes = {
            "ADD": "00",
            "SUB": "01",
            "LDR": "10",
            "STR": "11"
        }
        
        reg_codes = {
            "X0": "00",
            "X1": "01",
            "X2": "10",
            "X3": "11"
        }

        #parse ADD/SUB format:
        if instruction.startswith('ADD') or instruction.startswith('SUB'):
            parts = instruction.replace('=', ' ').replace(',', ' ').split()
            if len(parts) != 4:
                raise ValueError("Invalid ADD/SUB format. Example case: ADD X0 = X1,X2")
            
            opcode = opcodes[parts[0]]
            write_reg = reg_codes[parse_register(parts[1])]  #X0
            read_reg1 = reg_codes[parse_register(parts[2])]  #X1
            read_reg2 = reg_codes[parse_register(parts[3])]  #X2

        #parse LDR/STR format:
        elif instruction.startswith('LDR') or instruction.startswith('STR'):
            parts = instruction.replace('=', ' ').replace('[', ' ').replace(']', ' ').split(':')
            if len(parts) != 2:
                raise ValueError("Invalid LDR/STR format. Example cases:\nLDR X1 = [X2:4] \n LDR X1 = [X2:X3]")
            
            #parse first part (before colon)
            first_parts = parts[0].split()
            opcode = opcodes[first_parts[0]]
            write_reg = reg_codes[parse_register(first_parts[1])]
            base_reg = reg_codes[parse_register(first_parts[-1])]
            
            #parse second part (after colon)
            offset = parts[1].strip().strip(']')
            if offset.startswith('X'):  # Register offset
                read_reg1 = base_reg
                read_reg2 = reg_codes[parse_register(offset)]
            else:  #immediate offset
                read_reg1 = base_reg
                read_reg2 = "00"  # Use X0 for immediate
                immediate = parse_immediate(offset)
        else:
            raise ValueError(f"Unknown instruction: {instruction}")
        
        binary = opcode + write_reg + read_reg1 + read_reg2
        return binary, immediate
        
    except Exception as e:
        raise ValueError(f"Error parsing instruction: {str(e)}")

def main():
    current_dir = os.getcwd()
    inst_file_path = os.path.join(current_dir, 'instruction_memory.txt')
    data_file_path = os.path.join(current_dir, 'data_memory.txt')
    
    print(f"Creating files in: {current_dir}")
    print("\nInstruction Format Examples:")
    print("  ADD X0 = X1,X2     (Add X1 and X2, store in X0)")
    print("  SUB X3 = X1,X0     (Subtract X0 from X1, store in X3)")
    print("  LDR X1 = [X2:4]    (Load into X1 from address X2+4)")
    print("  LDR X1 = [X2:X3]   (Load into X1 from address X2+X3)")
    print("  STR X1 = [X2:4]    (Store X1 to address X2+4)")
    print("  STR X1 = [X2:X3]   (Store X1 to address X2+X3)\n")
    
    try:
        instructions = []
        immediates = []
        
        while True:
            try:
                instruction = input("\nEnter instruction (or 'q'/'quit' to exit):\n").strip()
                if instruction.lower() == 'quit' or instruction.lower() == 'q':
                    break
                if not instruction:
                    continue
                    
                binary, immediate = generate_binary(instruction)
                hex_code = hex(int(binary, 2))[2:].zfill(2)
                instructions.append(hex_code)
                
                if immediate is not None:
                    immediates.append(immediate)
                
                print(f"Binary: {binary}")
                print(f"Hex: {hex_code}")
                
            except ValueError as e:
                print(f"Error: {str(e)}")
                print("Please try again.")
            except Exception as e:
                print(f"Unexpected error: {str(e)}")
                print("Please try again.")
        
        #write instruction memory file
        with open(inst_file_path, 'w') as inst_file:
            inst_file.write("v2.0 raw\n")
            inst_file.write(" ".join(instructions))
            inst_file.write("\n")
            print(f"\nInstructions written to {inst_file_path}")
        
        #only create data memory file if there are immediates
        if immediates:
            with open(data_file_path, 'w') as data_file:
                data_file.write("v2.0 raw\n")
                data_file.write(" ".join(hex(x)[2:].zfill(2) for x in immediates))
                data_file.write("\n")
                print(f"Immediates written to {data_file_path}")
        
    except IOError as e:
        print(f"Error creating/writing to files: {str(e)}")

if __name__ == "__main__":
    print("Welcome to the OffBrandARM assembler!")
    main()
    print("\nAssembler successfuly terminated.")