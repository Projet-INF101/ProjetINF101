from menus import menu_principal
try:
    from turtle import mainloop
except Exception:
    def mainloop():
        pass

if __name__ == "__main__":
    menu_principal()
    mainloop()
