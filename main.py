import subprocess
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os.path
import datetime
import threading


class GuiUtilities:
    def __init__(self):
        self.starbound_folder = None
        self.steamworkshop_folder = None
        self.unpack_folder = None
        self.mod_list = []
        self.metadata_list = []

        self.check_paths()

    def check_paths(self):
        self.starbound_folder_check()
        self.steamworkshop_folder_check()
        self.starbound_folder_check()
        self.unpack_folder_check()

    def starbound_folder_check(self):
        if os.path.isfile('starboundfolder.txt'):
            with open('starboundfolder.txt', 'r') as reader:
                file_content = reader.readlines()
        else:
            return
        if file_content:
            if os.path.isfile(file_content[0] + "/win32/asset_unpacker.exe") and \
                    os.path.isfile(file_content[0] + "/win32/asset_packer.exe"):
                self.starbound_folder = file_content[0]
            else:
                messagebox.showerror('starboundfolder.txt error',
                                     'asset unpacker and/or asset packer not found in starboundfolder.txt!')
                self.starbound_folder = None
                os.remove('starboundfolder.txt')
        else:
            self.starbound_folder = None
            messagebox.showerror('starboundfolder.txt error', 'starboundfolder.txt is an empty file!')
            os.remove('starboundfolder.txt')

    def steamworkshop_folder_check(self):
        if os.path.isfile('steamworkshopfolder.txt'):
            with open('steamworkshopfolder.txt', 'r') as reader:
                file_content = reader.readlines()
        else:
            return
        if file_content:
            if os.path.isdir(file_content[0]):
                if os.listdir(file_content[0]):
                    self.mod_list = []
                    for workshop_folder_item in os.listdir(file_content[0]):
                        if os.path.isdir(os.path.join(file_content[0], workshop_folder_item).replace("\\", "/")):
                            for workshop_mod_folder_item in os.listdir(
                                    os.path.join(file_content[0], workshop_folder_item).replace("\\", "/")):
                                if os.path.isfile(
                                        os.path.join(
                                            file_content[0],
                                            workshop_folder_item, workshop_mod_folder_item).replace("\\", "/")) and \
                                        workshop_mod_folder_item.endswith('.pak'):
                                    self.mod_list.append(os.path.join(
                                            file_content[0],
                                            workshop_folder_item, workshop_mod_folder_item).replace("\\", "/"))
                    if not self.mod_list:
                        messagebox.showerror('steamworkshopfolder.txt error',
                                             'there are no .pak files in folders of steamworkshopfolder.txt!')
                        self.steamworkshop_folder = None
                        os.remove('steamworkshopfolder.txt')
                    else:
                        self.steamworkshop_folder = file_content[0]
                else:
                    messagebox.showerror('steamworkshopfolder.txt error',
                                         'there are no mod sub-folders in steamworkshopfolder.txt!')
                    self.steamworkshop_folder = None
                    os.remove('steamworkshopfolder.txt')
            else:
                messagebox.showerror('steamworkshopfolder.txt error', 'steamworkshopfolder.txt is not a folder!')
                self.steamworkshop_folder = None
                os.remove('steamworkshopfolder.txt')
        else:
            messagebox.showerror('steamworkshopfolder.txt error', 'steamworkshopfolder.txt is an empty file!')
            self.steamworkshop_folder = None
            os.remove('steamworkshopfolder.txt')

    def unpack_folder_check(self):
        if os.path.isfile('unpackfolder.txt'):
            with open('unpackfolder.txt', 'r') as reader:
                file_content = reader.readlines()
        else:
            return
        if file_content:
            if os.path.isdir(file_content[0]):
                if os.listdir(file_content[0]):
                    self.metadata_list = []
                    for unpack_folder_item in os.listdir(file_content[0]):
                        if os.path.isdir(os.path.join(file_content[0], unpack_folder_item).replace("\\", "/")):
                            for unpack_mod_folder_item in os.listdir(
                                    os.path.join(file_content[0], unpack_folder_item).replace("\\", "/")):
                                if os.path.isfile(
                                        os.path.join(
                                            file_content[0],
                                            unpack_folder_item, unpack_mod_folder_item).replace("\\", "/")) and \
                                        'metadata' in unpack_mod_folder_item:
                                    self.metadata_list.append(os.path.join(
                                        file_content[0],
                                        unpack_folder_item, unpack_mod_folder_item).replace("\\", "/"))
                    if not self.metadata_list:
                        messagebox.showerror('unpackfolder.txt error',
                                             'there are no metadata files in folders of unpackfolder.txt!')
                        self.unpack_folder = None
                        os.remove('unpackfolder.txt')
                    else:
                        self.unpack_folder = file_content[0]
                else:
                    messagebox.showerror('unpackfolder.txt error',
                                         'there are no mod sub-folders in unpackfolder.txt!')
                    self.unpack_folder = None
                    os.remove('unpackfolder.txt')
            else:
                messagebox.showerror('unpackfolder.txt error', 'unpackfolder.txt is not a folder!')
                self.unpack_folder = None
                os.remove('unpackfolder.txt')
        else:
            messagebox.showerror('unpackfolder.txt error', 'unpackfolder.txt is an empty file!')
            self.unpack_folder = None
            os.remove('unpackfolder.txt')
        print(self.metadata_list)


class MainApplication(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        self.starbound_folder_select = StarboundFolder(self)
        self.steamworkshop_folder_select = SteamWorkshopFolder(self)
        self.unpack_folder_select = UnpackFolder(self)
        self.progress_bar = ProgressBar(self)
        self.mod_unpacker = ModUnpacker(self)

        self.starbound_folder_select.grid(row=0, column=0, sticky=tk.EW)
        self.steamworkshop_folder_select.grid(row=1, column=0, sticky=tk.EW)
        self.unpack_folder_select.grid(row=2, column=0, sticky=tk.EW)
        self.progress_bar.grid(row=3, column=0, sticky=tk.EW)
        self.mod_unpacker.grid(row=4, column=0, sticky=tk.EW)

        self.grid_columnconfigure(0, weight=1)


class StarboundFolder(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        self.starbound_folder_label = tk.Label(self, text='Starbound Directory:')
        self.starbound_folder_destination = tk.Text(self, state=tk.DISABLED, height=1)
        self.starbound_folder_button_image = tk.PhotoImage(file='FolderButtonImage.gif', height=16, width=16)
        self.starbound_folder_button = tk.Button(self, image=self.starbound_folder_button_image,
                                                 command=lambda: self.starbound_folder_button_click())
        self.update_starbound_folder_destination()

        self.starbound_folder_label.grid(row=0, column=0)
        self.starbound_folder_destination.grid(row=0, column=1, sticky=tk.EW)
        self.starbound_folder_button.grid(row=0, column=2)

        self.grid_columnconfigure(1, weight=1)

    def starbound_folder_button_click(self):
        starbound_folder = filedialog.askdirectory(title="Select your Starbound directory")
        if starbound_folder:
            with open('starboundfolder.txt', "w") as writer:
                writer.write(starbound_folder)
            gui_util.starbound_folder_check()
            self.update_starbound_folder_destination()

    def update_starbound_folder_destination(self):
        if gui_util.starbound_folder:
            self.starbound_folder_destination.configure(state=tk.NORMAL)
            self.starbound_folder_destination.delete("1.0", tk.END)
            self.starbound_folder_destination.insert(tk.END, gui_util.starbound_folder)
            self.starbound_folder_destination.configure(state=tk.DISABLED)
        else:
            self.starbound_folder_destination.configure(state=tk.NORMAL)
            self.starbound_folder_destination.delete("1.0", tk.END)
            self.starbound_folder_destination.configure(state=tk.DISABLED)


class SteamWorkshopFolder(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        self.steamworkshop_folder_label = tk.Label(self, text='Steam Workshop Directory:')
        self.steamworkshop_folder_destination = tk.Text(self, state=tk.DISABLED, height=1)
        self.steamworkshop_button_image = tk.PhotoImage(file='FolderButtonImage.gif', height=16, width=16)
        self.steamworkshop_folder_button = tk.Button(self, image=self.steamworkshop_button_image,
                                                     command=lambda: self.steamworkshop_folder_button_click())
        self.update_steamworkshop_folder_destination()

        self.steamworkshop_folder_label.grid(row=0, column=0)
        self.steamworkshop_folder_destination.grid(row=0, column=1, sticky=tk.EW)
        self.steamworkshop_folder_button.grid(row=0, column=2)

        self.grid_columnconfigure(1, weight=1)

    def steamworkshop_folder_button_click(self):
        steamworkshop_folder = filedialog.askdirectory(title="Select Starbound's Steam Workshop directory")
        if steamworkshop_folder:
            with open('steamworkshopfolder.txt', "w") as writer:
                writer.write(steamworkshop_folder)
            gui_util.steamworkshop_folder_check()
            self.update_steamworkshop_folder_destination()

    def update_steamworkshop_folder_destination(self):
        if gui_util.steamworkshop_folder:
            self.steamworkshop_folder_destination.configure(state=tk.NORMAL)
            self.steamworkshop_folder_destination.delete("1.0", tk.END)
            self.steamworkshop_folder_destination.insert(tk.END, gui_util.steamworkshop_folder)
            self.steamworkshop_folder_destination.configure(state=tk.DISABLED)
            print(gui_util.mod_list)
        else:
            self.steamworkshop_folder_destination.configure(state=tk.NORMAL)
            self.steamworkshop_folder_destination.delete("1.0", tk.END)
            self.steamworkshop_folder_destination.configure(state=tk.DISABLED)


class UnpackFolder(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        self.unpack_folder_label = tk.Label(self, text='Unpacked Mods Directory:')
        self.unpack_folder_destination = tk.Text(self, state=tk.DISABLED, height=1)
        self.unpack_button_image = tk.PhotoImage(file='FolderButtonImage.gif', height=16, width=16)
        self.unpack_folder_button = tk.Button(self, image=self.unpack_button_image,
                                              command=lambda: self.unpack_folder_button_click())
        self.update_unpack_folder_destination()

        self.unpack_folder_label.grid(row=0, column=0)
        self.unpack_folder_destination.grid(row=0, column=1, sticky=tk.EW)
        self.unpack_folder_button.grid(row=0, column=2)

        self.grid_columnconfigure(1, weight=1)

    def unpack_folder_button_click(self):
        unpack_folder = filedialog.askdirectory(title="Select unpacked mods directory")
        if unpack_folder:
            with open('unpackfolder.txt', "w") as writer:
                writer.write(unpack_folder)
            gui_util.unpack_folder_check()
            self.update_unpack_folder_destination()

    def update_unpack_folder_destination(self):
        if gui_util.unpack_folder:
            self.unpack_folder_destination.configure(state=tk.NORMAL)
            self.unpack_folder_destination.delete("1.0", tk.END)
            self.unpack_folder_destination.insert(tk.END, gui_util.unpack_folder)
            self.unpack_folder_destination.configure(state=tk.DISABLED)
        else:
            self.unpack_folder_destination.configure(state=tk.NORMAL)
            self.unpack_folder_destination.delete("1.0", tk.END)
            self.unpack_folder_destination.configure(state=tk.DISABLED)


class ProgressBar(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        self.progress_bar = ttk.Progressbar(self, mode='determinate')

        self.progress_bar.grid(row=0, column=0, sticky=tk.EW)

        self.grid_columnconfigure(0, weight=1)


class ModUnpacker(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        self.unpack_button = tk.Button(self, text='Unpack mods', command=lambda: self.unpack_mods())

        self.unpack_button.grid(row=0, column=0)

        self.grid_columnconfigure(0, weight=1)

    def unpack_mods(self):
        if gui_util.mod_list:
            mod_list = gui_util.mod_list
            unpacker_file = (gui_util.starbound_folder + '/win32/asset_unpacker.exe').replace('/', '\\')
            unpack_folder_name = os.getcwd() + '\\unpack' + str(datetime.datetime.now()).replace(':', '-')
            os.mkdir(unpack_folder_name)
            threading.Thread(target=self.unpack_process, args=(
                unpacker_file,
                [mod_location.replace('/', '\\') for mod_location in mod_list],
                unpack_folder_name)).start()

    def unpack_process(self, unpacker_file, mod_list, unpack_folder):
        self.unpack_button.configure(state=tk.DISABLED)
        self.parent.unpack_folder_select.unpack_folder_button.configure(state=tk.DISABLED)
        self.parent.steamworkshop_folder_select.steamworkshop_folder_button.configure(state=tk.DISABLED)
        self.parent.starbound_folder_select.starbound_folder_button.configure(state=tk.DISABLED)
        gui_util.unpack_folder = unpack_folder.replace('\\', '/')
        self.parent.unpack_folder_select.update_unpack_folder_destination()
        self.parent.progress_bar.progress_bar['value'] = 0
        for mod_location in mod_list:
            unpack_location = unpack_folder + '\\' + mod_location.split('\\')[-2]
            cmd = '\"{}\" \"{}\" \"{}\"'.format(unpacker_file, mod_location, unpack_location)
            if str(subprocess.check_output(cmd))[0] == 'b':
                if mod_list.index(mod_location) == len(mod_list):
                    self.parent.progress_bar.progress_bar['value'] = 100
                else:
                    self.parent.progress_bar.progress_bar['value'] = self.parent.progress_bar.progress_bar['value'] + \
                                                                     round(100/len(mod_list))
        gui_util.unpack_folder = None
        with open('unpackfolder.txt', "w") as writer:
            writer.write(unpack_folder.replace('\\', '/'))
        gui_util.unpack_folder_check()
        self.parent.unpack_folder_select.update_unpack_folder_destination()
        self.unpack_button.configure(state=tk.NORMAL)
        self.parent.steamworkshop_folder_select.steamworkshop_folder_button.configure(state=tk.NORMAL)
        self.parent.starbound_folder_select.starbound_folder_button.configure(state=tk.NORMAL)
        self.parent.unpack_folder_select.unpack_folder_button.configure(state=tk.NORMAL)


if __name__ == "__main__":
    root = tk.Tk()
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    root.title('Starbound Mod Manager')
    gui_util = GuiUtilities()
    gui = MainApplication(root, bg="orange")
    gui.grid(row=0, column=0, sticky=tk.NSEW)
    root.mainloop()
