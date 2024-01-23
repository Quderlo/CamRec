from main_window import RecognitionWindow

if __name__ == "__main__":
    root = RecognitionWindow()
    root.protocol("WM_DELETE_WINDOW", root.quit)
    root.mainloop()
