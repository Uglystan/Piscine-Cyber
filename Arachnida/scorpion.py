import sys
import os
from hachoir.parser import createParser
from hachoir.metadata import extractMetadata

def main():
    arguments = sys.argv
    arguments = arguments[1:]
    for argument in arguments:
        if os.path.exists(argument) == False or os.access(argument, os.R_OK) == False:
            print("Incorrect file :", argument)
            continue
        parser = createParser(argument)
        metadata = extractMetadata(parser)
        if metadata is not None:
            metadata: Dict[str, str] = metadata.exportDictionary()['Metadata']
            for key in metadata:
                print(f"{key} : {metadata[key]}")
        
          
    

if __name__ == "__main__":
    main()

#https://www.theparisphotographer.com/