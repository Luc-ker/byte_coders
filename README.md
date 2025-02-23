# No Cons Shopping Gen

# app.py
The main program to run containing all the tkinter UI. It connects to the other programs by passing input to them when processing is required, e.g. images.
It requires the csv library and the other files in the repo in order to run.

# ocr.py
The program containing the OCR scanner, requiring csv, pytesseract, tesseract and opencv-python (imported as cv2) to run.

# sqlMethod.py
The program containing all the sql commands in order for us to write to the database. Doesn't require any non-standard python libraries to run.

# get_reciept.py
Handles taking in an image as input from a live video feed. Requires opencv-python (imported as cv2) to run.

# example.db
Contains the database where all information required is stored.

# Potential Future Functionalities
Our next steps would be to add more multi-person functionality, such as a shared shopping list and being able to split the bill. We would also add in functionality such that, based on what the user has inputted in previously, the app would estimate when the user would finish with certain items.
