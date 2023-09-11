"""TEST IMPLEMENTATION"""
from tkinter import Tk

class DailyDigestGUI:
    """
    The GUI should enable the admin to..
            1. configure which content sources to include in the email
            2. Add recipients
            3. Remove recipients
            4. Schedule Daily Time to Send Email
            5. Configure sender credentials
    """

    def __init__(self, _):
        pass

if __name__ == '__main__':
    root = Tk()
    app = DailyDigestGUI(root)
    root.mainloop()
 