from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from tkinter import ttk
from sim import *

# initialize gui
gui = Tk()
left = Frame(gui, height=200, width=200)
left.pack(side=LEFT, expand=True, fill=Y)
right = Frame(gui, height=200, width=200)
right.pack(side=LEFT, expand=True, fill=BOTH)

# general variables
years = IntVar()
steps = IntVar()
qu = IntVar()
filename = StringVar()
filename.set('orbits')
av = BooleanVar()
avs = BooleanVar()
pv = BooleanVar()
pvs = BooleanVar()
dv = BooleanVar()
radio = BooleanVar()
system = StringVar()
system.set('Sol')


# gui functions
def new_file():
    years.set(1)
    steps.set(250)
    qu.set(5)
    filename.set('orbits')
    av.set(True)
    avs.set(False)
    pv.set(False)
    pvs.set(False)
    dv.set(False)
    radio.set(False)
    system.set('Sol')


def open_file():
    file = filedialog.askopenfile(mode="r", defaultextension='.gv', title = 'Use settings from file.')
    settings = []
    for line in file:
        settings.append(str(line).strip())
    years.set(int(settings[0]))
    steps.set(int(settings[1]))
    qu.set(int(settings[2]))
    filename.set(str(settings[3]))
    av.set(str_to_bool(settings[4]))
    avs.set(str_to_bool(settings[5]))
    pv.set(str_to_bool(settings[6]))
    pvs.set(str_to_bool(settings[7]))
    dv.set(str_to_bool(settings[8]))
    radio.set(str_to_bool(settings[9]))
    system.set(str(settings[10]))


def save_file():
    file = filedialog.asksaveasfile(mode='w', defaultextension='.gv', title = 'Save settings to file.')
    settings = [years.get(), steps.get(), qu.get(), filename.get(), av.get(), avs.get(), pv.get(), pvs.get(), dv.get(),
                radio.get(), system.get()]
    for element in settings:
        file.write(str(element) + '\n')
    file.close()


def close():
    exit_app = messagebox.askyesno(title='Closing', message='Are You Sure?')
    if exit_app:
        gui.destroy()


def help_docs():
    messagebox.showinfo(title='About', message='...')


def about():
    messagebox.showinfo(title='About', message='A simple gravity simulator written by GH.\n\nVer 0.1')


def run():
    main(years, steps, radio, pv, pvs, av, avs, dv, system, qu, filename, progress_bar)


def str_to_bool(s):
    if s == 'True':
        return True
    if s == 'False':
        return False


# gui layout
gui.title('Gravity Simulation')

# menu bar
menu_bar = Menu(gui)

file_menu = Menu(menu_bar, tearoff=0)
file_menu.add_command(label='New', command=new_file)
file_menu.add_command(label='Open Settings', command=open_file)
file_menu.add_command(label='Save Settings', command=save_file)
file_menu.add_command(label='Close', command=close)
menu_bar.add_cascade(label='File', menu=file_menu)

help_menu = Menu(menu_bar, tearoff=0)
help_menu.add_command(label='Help Docs', command=help_docs)
help_menu.add_command(label='About', command=about)
menu_bar.add_cascade(label='Help', menu=help_menu)

gui.config(menu=menu_bar)

# year slider
label_years = Label(left, text='years:').pack()
slider_year = Scale(left, orient=HORIZONTAL, length=150, tickinterval=5, from_=1, to=16, variable=years).pack()

# randomize entries
radio_randomize = Radiobutton(left, text='randomize', value=True, variable=radio).pack()
label_objects = Label(left, text='# of mass objects:').pack()
slider_objects = Scale(left, orient=HORIZONTAL, length=150, tickinterval=5, from_=5, to=25, variable=qu).pack()

# preset system list
radio_preset = Radiobutton(left, text='preset', value=False, variable=radio).pack()
label_list_system = Label(left, text='available presets').pack()
list_system = Listbox(left, height=4)
list_system.insert(1, 'Sol')
list_system.insert(2, 'missing data ...')
list_system.pack()

# button to select
button_select = Button(left, text='Set', command=lambda: system.set(list_system.get(ACTIVE))).pack()

# step slider
label_steps = Label(right, text='steps to calculate:').pack()
slider_steps = Scale(right, orient=HORIZONTAL, length=150, tickinterval=250, from_=250, to=1000, variable=steps)
slider_steps.pack()

# plot buttons
check_plot = Checkbutton(right, text='plot?', variable=pv, onvalue=1, offvalue=0).pack()
radio1_plot = Radiobutton(right, text='show', value=False, variable=pvs).pack()
radio2_plot = Radiobutton(right, text='save', value=True, variable=pvs).pack()

# animation buttons
check_animation = Checkbutton(right, text='animate?', variable=av, onvalue=1, offvalue=0).pack()
radio1_animation = Radiobutton(right, text='show', value=False, variable=avs).pack()
radio2_animation = Radiobutton(right, text='save', value=True, variable=avs).pack()

# filename entry
label_filename = Label(right, text='Enter filename here:').pack()
entry_filename = Entry(right, textvariable=filename).pack()

# dataout checker
dataout = Checkbutton(right, text='write raw data', variable=dv, onvalue=1, offvalue=0).pack()

# progressbar
progress_bar = ttk.Progressbar(right, orient='horizontal', mode='determinate')
progress_bar.pack()

# button to run the simulation
button_start = Button(right, text='Run', command=lambda: run()).pack()

gui.mainloop()
