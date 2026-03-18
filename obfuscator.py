"""
obfuscator
Description: A basic python script to aid in the obfuscation of c and c++ source code files
Authors: Sam "Alice" Blair, Winston Howard, Chance Sweetser
Created Date: 05/04/20
"""

import os
import re
import math
import random
import string




def variable_renamer(given_string):
    """
    Función mejorada para EDK2 y nombres tipo Il1
    """
    variable_dictionary = {}
    
    # LISTA DE EXCEPCIONES PARA QUE EDK2 NO EXPLOTE
    special_cases = {
        # --- C Estándar (Fundamentales) ---
        "struct", "typedef", "static", "const", "unsigned", "void", "int", 
        "char", "float", "double", "long", "short", "signed", "sizeof", 
        "NULL", "return", "if", "else", "for", "while", "do", "switch", 
        "case", "default", "break", "continue", "goto", "enum", "union", "extern",

        # --- EDK2 / TianoCore (Tipos de datos) ---
        "EFIAPI", "EFI_STATUS", "EFI_HANDLE", "EFI_SYSTEM_TABLE", "EFI_EVENT",
        "EFI_GUID", "EFI_SUCCESS", "IN", "OUT", "OPTIONAL", "CONST", "BOOLEAN", 
        "TRUE", "FALSE", "UINT8", "UINT16", "UINT32", "UINT64", "UINTN", 
        "INT8", "INT16", "INT32", "INT64", "INTN", "VOID", "CHAR8", "CHAR16",

        # --- EDK2 (Funciones y Protocolos Comunes) ---
        "UefiMain", "Print", "gBS", "gST", "gRT", "DEBUG", "ASSERT", 
        "CopyMem", "SetMem", "ZeroMem", "FreePool", "AllocatePool",
        "LocateProtocol", "HandleProtocol", "OpenProtocol", "CloseProtocol"
    }
    
    index = 0
    new_string = ""
    split_code = re.split('\"', given_string)
    
    # Buscamos nombres de funciones y variables
    filtered_code = re.findall(
        r"(?:\w+\s+)(?!main)(?:\*)*([a-zA-Z_][a-zA-Z0-9_]*)", given_string)

    for found_example in filtered_code:
        # Solo ofuscamos si NO está en la lista de excepciones
        if(found_example not in special_cases and len(found_example) > 2):
            if(found_example not in variable_dictionary):
                # Generamos el nombre tipo Il11lI
                variable_dictionary[found_example] = random_string(14)

    for section in split_code:
        if(index % 2 == 0):  
            for entry in variable_dictionary:   
                re_string = r"\W{}\W".format(entry)
                while True:
                    first_found_entry = re.search(re_string, section)
                    if(not first_found_entry):
                        break
                    start = first_found_entry.start(0)
                    end = first_found_entry.end(0)
                    section = section[:start+1] + variable_dictionary[entry] + section[end-1:]
        
        if(index >= 1):
            new_string = new_string + "\"" + section  
        else:
            new_string = new_string + section
        index += 1
    
    return new_string


def random_string(stringLength=14):
    # La primera letra SIEMPRE es una "I" o "l" o "i" (no números)
    first_letter = random.choice("Ili")
    # El resto puede ser lo que quieras
    letters = "Il1i"
    return first_letter + ''.join(random.choice(letters) for i in range(stringLength - 1))




def whitespace_remover(a):
    """
    Function to remove all whitespace, except for after functions, variables, and imports
    """
    splits = re.split('\"',a)
    code_string = "((\w+\s+)[a-zA-Z_*][|a-zA-Z0-9_]*|#.*|return [a-zA-Z0-9_]*| [[.].]|else)"
    index = 0
    a = ""
    for s in splits:
            # If its not the contents of a string, remove spaces of everything but code
            if(index%2==0):                
              s_spaceless = re.sub("[\s]", "", s)          # Create a spaceless version of s
              s_code = re.findall(code_string,s)           # find all spaced code blocks in s

              for code in s_code:
               old = re.sub("[\s]", "", code[0])
               new = code[0]

               if(code[0][0] == '#'):
                 new = code[0] + "\n"                      # Adding a newline for preprocesser commands
               elif("unsigned" in code[0] or "else" in code[0]):
                 new = code[0] + " "
               s_spaceless = s_spaceless.replace(old,new) # Replace the spaceless code blocks in s with their spaced equivilents                
            else:
              s_spaceless = s

            if(index >= 1):
             a = a + "\"" + s_spaceless
            else:
             a = a + s_spaceless
            index+=1
    return a

def comment_remover(given_string):
    """
    Function to (currently) remove C++ style comments 
    given_string is a string of C/C++ code
    """

    #This does not take into account if a C++ style comment happens within a string
    # i.e. "Normal String // With a C++ comment embedded inside"
    cpp_filtered_code = re.findall(
        r"\/\/.*", given_string)
    for entry in cpp_filtered_code:
        given_string = given_string.replace(entry, "")
    
    # This is a barebones start for C style block comments
    # Current issue is it is only single line C style comments
    # It also finds C style comments in strings
    c_filtered_code= re.findall(
        r"\/\*.*\*\/", given_string)
    for entry in c_filtered_code:
        given_string = given_string.replace(entry, "")
    
    return given_string

def main():
    """
    Versión para ofuscar un solo archivo específico
    """
    # Pedimos el nombre del archivo directamente
    target_file = input('Nombre del archivo a ofuscar (ej. R.c): ')

    if os.path.exists(target_file):
        print(f"\nProcesando {target_file}...")
        
        if target_file.endswith(".c") or target_file.endswith(".h") or target_file.endswith(".cpp"):
            with open(target_file, 'r') as f:
                file_string = f.read()
            
            # Ejecutamos la limpieza y ofuscación
            file_string = comment_remover(file_string)
            file_string = variable_renamer(file_string)
            file_string = whitespace_remover(file_string)
            
            # Guardamos el resultado con el prefijo 'obf_'
            output_name = "obf_" + target_file
            with open(output_name, "w") as f_out:
                f_out.write(file_string)
            
            print(f"[OK] Archivo guardado como: {output_name}")
            print("-" * 30)
            print(file_string) # Muestra el resultado en pantalla
            print("-" * 30)
        else:
            print("[ERROR] El archivo debe ser .c, .h o .cpp")
    else:
        print(f"[ERROR] No se encuentra el archivo '{target_file}' en esta carpeta.")

if __name__ == "__main__":
    main()
