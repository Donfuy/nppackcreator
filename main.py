from definitions import *
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from creator import Creator
from PIL import ImageTk, Image
import os


# TODO: Replace current metanet tabs with empty ones
# TODO: Replace current nprofiles with empty, gamified ones
# TODO: Add descriptions inside each label frame
class MainWindow(ttk.Frame):
    def __init__(self, root, **kwargs):
        super().__init__(root, **kwargs)
        self.content = ttk.Frame(root, padding=(5, 5, 5, 5))
        self.content.grid(column=0, row=0, sticky=(N, W, E, S))
        self.content.grid_columnconfigure(0, weight=1)
        self.content.grid_columnconfigure(1, weight=1)
        self.content.grid_columnconfigure(2, weight=1)
        self.content.grid_columnconfigure(3, weight=1)
        self.content.grid_rowconfigure(0, weight=1)
        self.content.grid_rowconfigure(1, weight=100)
        self.content.grid_rowconfigure(2, weight=1)
        self.content.grid_rowconfigure(3, weight=1)

        self.logic = Creator()
        ######
        # NAME
        #
        # LABEL FRAME
        self.names_lframe = ttk.Labelframe(self.content, text='Name', padding=(10, 10, 10, 10))
        self.names_lframe.grid_columnconfigure(0, weight=1)
        # ENTRY
        self.pack_name = StringVar()
        self_pack_name_entry = ttk.Entry(self.names_lframe, textvariable=self.pack_name)
        self.pack_name.trace_add("write", self.name_has_been_written)
        # NAME GRID
        self_pack_name_entry.grid(column=0, row=0, columnspan=1, sticky=(N, W, E))

        # TODO: Make tab list items bigger in every way
        ######
        # TABS
        #
        # LABEL FRAME
        self.tabs_lframe = ttk.Labelframe(self.content, text='Tabs & Codes', padding=(10, 10, 10, 10))
        self.tabs_lframe.grid_rowconfigure(0, weight=1)
        self.tabs_lframe.grid_columnconfigure(0, weight=1)
        # ADD BUTTON
        self.add_tabs_btn = ttk.Button(self.tabs_lframe, text="Add", command=self.on_add_tabs_btn_click)
        # REMOVE BUTTON
        self.remove_tabs_btn = ttk.Button(self.tabs_lframe, text="Remove", command=self.on_remove_tab_btn_click)
        # TABS LISTBOX
        self.tab_list = StringVar(value=self.logic.tabs)
        self.tabs_lbox = Listbox(self.tabs_lframe, listvariable=self.tab_list, selectmode='extended')
        # TABS GRID
        self.tabs_lbox.grid(column=0, columnspan=2, row=0, rowspan=2, sticky=(N, S, W, E))
        self.add_tabs_btn.grid(column=0, columnspan=1, row=2, sticky=(S, W))
        self.remove_tabs_btn.grid(column=1, columnspan=1, row=2, sticky=(S, E))

        ######
        # BANNER
        #
        # LABEL FRAME
        self.banner_lframe = ttk.Labelframe(self.content, text='Banner (optional)', padding=(10, 10, 10, 10))
        # ADD BUTTON
        self.choose_banner_btn = ttk.Button(self.banner_lframe, text='Choose Banner', command=self.on_choose_banner_click)
        # REMOVE BUTTON
        self.remove_banner_btn = ttk.Button(self.banner_lframe, text='Remove Banner', command=self.on_remove_banner_click)
        # IMAGE
        self.banner_image = ImageTk.PhotoImage(Image.open(EMPTY_BANNER))
        self.banner_image_label = ttk.Label(self.banner_lframe, image=self.banner_image)
        # BANNER GRID
        self.banner_image_label.grid(column=0, row=1)
        self.choose_banner_btn.grid(column=0, row=0, sticky=W)
        self.banner_image_label.lower(self.choose_banner_btn)
        self.remove_banner_btn.grid(column=0, row=0, sticky=E)

        ######
        # ATTRACT
        #
        # LABEL FRAME
        self.attract_lframe = ttk.Labelframe(self.content, text='Attract (optional)', padding=(10, 10, 10, 10))
        # ENTRY
        self.attract_location = StringVar()
        self.attract_entry = ttk.Entry(self.attract_lframe, textvariable=self.attract_location)
        # CHOOSE ATTRACT BUTTON
        self.choose_attract_button = ttk.Button(self.attract_lframe, text='Choose', command=self.on_choose_attract_click)
        # ATTRACT GRID
        self.choose_attract_button.grid(column=1, row=0)
        self.attract_entry.grid(column=0, row=0)

        ######
        # NPROFILE
        #
        # LABEL FRAME
        self.nprofile_lframe = ttk.Labelframe(self.content, text='nprofile (optional)', padding=(10, 10, 10, 10))
        self.nprofile_location = StringVar()
        self.nprofile_entry = ttk.Entry(self.nprofile_lframe, textvariable=self.nprofile_location)
        # CHOOSE ATTRACT BUTTON
        self.choose_nprofile_button = ttk.Button(self.nprofile_lframe, text='Choose', command=self.on_choose_nprofile_click)
        # ATTRACT GRID
        self.choose_nprofile_button.grid(column=1, row=0)
        self.nprofile_entry.grid(column=0, row=0)

        ######
        # SEPARATOR
        #
        # self.separator = ttk.Separator(self.content, orient=HORIZONTAL)
        ######
        # CREATE PACK BUTTON
        self.create_pack_btn = ttk.Button(self.content, text='Save pack', command=self.on_create_pack_click)

        # ROOT GRID
        self.names_lframe.grid(column=0, columnspan=2, row=0, rowspan=1, padx=5, pady=5, sticky=(N, E, W))
        self.tabs_lframe.grid(column=0, columnspan=2, row=1, rowspan=2, padx=5, pady=5, sticky=(N, S, E, W))
        self.banner_lframe.grid(column=2, columnspan=2, row=0, rowspan=3, padx=5, pady=5, sticky=(N, S, E, W))
        self.attract_lframe.grid(column=0, columnspan=2, row=3, rowspan=1, padx=5, pady=5, sticky=(N, E, W))
        self.nprofile_lframe.grid(column=2, columnspan=2, row=3, rowspan=1, padx=5, pady=5, sticky=(N, E, W))
        # self.separator.grid(column=0, columnspan=4, row=4, rowspan=1, padx=5, pady=5)
        self.create_pack_btn.grid(column=3, columnspan=1, row=5, rowspan=1, padx=5, pady=5, sticky=E)

    def on_add_tabs_btn_click(self):
        new_tabs = filedialog.askopenfilenames()
        tabs_exist = []
        temp_tabs = self.logic.tabs.copy()

        # Check if those tabs have already been added
        for tab in new_tabs:
            if not self.logic.has_tab(tab):
                temp_tabs.append(tab)
            else:
                tabs_exist.append(tab)
        self.logic.tabs = temp_tabs.copy()

        # If some tabs had already been added, ask if they want to replace them
        if not len(tabs_exist) == 0:
            existing_tabs_str = ''
            for tab in tabs_exist:
                existing_tabs_str = existing_tabs_str + os.path.basename(tab) + '\n'
            tabs_exist_question = TABS_EXIST_WARNING_MESSAGE + existing_tabs_str + TABS_EXIST_WARNING_QUESTION

            if messagebox.askyesno(WARNING_TITLE, tabs_exist_question):
                print("Replace")
                for replacing_tab in tabs_exist:
                    # TODO: Verify if the created pack has the correct tabs
                    for tab in self.logic.tabs:
                        if self.logic.has_tab(replacing_tab):
                            print("Replacing tab:", replacing_tab)
                            print("Tab:", tab)
                            self.logic.tabs.remove(tab)
                            self.logic.tabs.append(replacing_tab)
                    tabs_exist.remove(replacing_tab)
            else:
                print("Do not replace")
        self.update_tab_list()

    def on_remove_tab_btn_click(self):
        tabs_to_remove = []
        for tab in self.tabs_lbox.curselection():
            tabs_to_remove.append(self.logic.tabs[tab])
        for tab in tabs_to_remove:
            self.logic.tabs.remove(tab)
        self.update_tab_list()

    def update_tab_list(self):
        tabs_basenames = []
        for tab in self.logic.tabs:
            tabs_basenames.append(os.path.basename(tab))
        self.tab_list.set(tabs_basenames)

    def on_choose_banner_click(self):
        banner = filedialog.askopenfilename()
        self.logic.banner = banner
        if self.logic.has_banner():
            if self.logic.validate_banner():
                # Hide add banner button
                self.banner_image = ImageTk.PhotoImage(Image.open(self.logic.banner).resize((277, 480)))
                self.banner_image_label.configure(image=self.banner_image)
            else:
                messagebox.showerror("Error loading banner", "Chosen file isn't an image! Currently it NEEDS to be a 900x1300 file btw it's gonna change eventually kthxbai")
                self.logic.banner = ''

    def on_remove_banner_click(self):
        self.logic.remove_banner()
        self.banner_image = ImageTk.PhotoImage(Image.open(EMPTY_BANNER))
        self.banner_image_label.configure(image=self.banner_image)

    def on_choose_attract_click(self):
        attract = filedialog.askopenfilename()
        if not attract == '':
            self.logic.remove_attracts()
            self.logic.attracts.append(attract)
            self.attract_location.set(os.path.basename(self.logic.attracts[0]))

    def on_choose_nprofile_click(self):
        # TODO all the checks
        nprofile = filedialog.askopenfilename()
        self.logic.nprofile = nprofile
        self.nprofile_location.set(self.logic.nprofile)

    def on_create_pack_click(self):
        if not self.logic.has_name():
            messagebox.showerror("Error creating pack", "A pack name is required!")
        elif not self.logic.has_tabs():
            messagebox.showerror("Error creating pack", "Tab files are required!")
        else:
            self.logic.create_pack()

    # DO NOT REMOVE *ARGS, they ARE needed
    def name_has_been_written(self, *args):
        self.logic.name = self.pack_name.get()


def main():
    app = Tk()
    app.title("N++ Mappack Creator")
    app.resizable(FALSE, FALSE)
    MainWindow(app)
    app.mainloop()


if __name__ == '__main__':
    main()
