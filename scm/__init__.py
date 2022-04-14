"""Root directory for the scm package"""
# scm/__init__.py

__app__name__ = "scm"
__version__ = "0.1.0"

(
 SUCCESS, 
 DIR_ERROR, 
 FILE_ERROR, 
 IO_ERROR, 
 VALIDATION_ERROR, 
 OS_ERROR    
) = range(6)

ERRORS = {
    DIR_ERROR: "Config directory error", 
    FILE_ERROR: "Config file error", 
    IO_ERROR: "Error during the IO Operation", 
    VALIDATION_ERROR: "Error during the validation",
    OS_ERROR: "Error from the OS system module"
    
}