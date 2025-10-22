import logging
from PySide6.QtGui import QTextCursor
from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QTextEdit

class TextHandler(logging.Handler): 

    """
    TextHandler - a class designed for a custom log handler that displays log records 
    in the Tkinter text widget. It is to be used as an addHandler when specifying your
    customer logger
    """

    # Initialising a handler and a formatter for the custom logger
    # Takes the text widget as text and a format for a formatter
    def __init__(self, text: QTextEdit, format):   
        logging.Handler.__init__(self)
        self.setFormatter(logging.Formatter(format))
        self.text = text
    
    # Emit method that takes the logRecord, format's it with the set format template,
    # and is inserted on instant schedule to the text widget
    def emit(self, record):
        message = self.format(record)   
        def append():
            self.text.setReadOnly(False)
            self.text_insert(f"{message}\n",line = 1,column = 0, at_end = True)
            self.text.setReadOnly(True)  
            self.text.moveCursor(QTextCursor.End)
        QTimer.singleShot(0, append)

    def text_insert(self, text, line = None, column = None, at_end = False):
        cursor = self.text.textCursor()
        if at_end:
            # Move cursor to the end and insert the text
            cursor.movePosition(QTextCursor.End)
        elif line is not None and column is not None:
            # Move the cursor to the specified line and column
            cursor.movePosition(QTextCursor.Start)  # Go to the start of the document
            cursor.movePosition(QTextCursor.Down, QTextCursor.MoveAnchor, line - 1)  # Move down to the correct line
            cursor.movePosition(QTextCursor.Right, QTextCursor.MoveAnchor, column)  # Move right to the correct column
        # Insert the text
        cursor.insertText(text)

def clear_logger(handler):
    """
    Clears the log from the TextHandler's text widget in Page 3:
    Checks if the handler parameter is an instance of TextHandler class
    Ensures that the function only attempts to clear the text widget provided
    """
    if isinstance(handler, TextHandler):
        # handler.text refers to the text widget associated with the Text Handler
        handler.text.setReadOnly(False)
        handler.text.clear()
        handler.text.moveCursor(QTextCursor.End)
        handler.text.setReadOnly(True)