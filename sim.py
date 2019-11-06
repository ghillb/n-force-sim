import csv, os, sys
import random as rd
import matplotlib.pyplot as plt
import matplotlib.animation as ani
import numpy as np


class Object:
    def __init__(self):
        self.id = None
        self.name = None
        self.mass = None
        self.position = None
        self.velocity = None
        self.pos_list = None
        self.vel_list = None


def gravity(object1, object2):
    """
    calculates the force of gravity between two objects
    :param object1:
    :param object2:
    :return: force of gravity between two objects
    """
    g = 6.67408e-11
    m1, m2 = object1.mass, object2.mass
    x1, y1 = object1.position[0], object1.position[1]
    x2, y2 = object2.position[0], object2.position[1]
    dx, dy = x2 - x1, y2 - y1
    d = np.sqrt(dx**2 + dy**2)
    fx = g * m1 * m2 * (x2 - x1) / (d**3)
    fy = g * m1 * m2 * (y2 - y1) / (d**3)
    return fx, fy


def calculate(objects, t_max, steps, progress_bar):
    """
    loops for each time step over the bodies until tmax is reached
    :param objects: list of objects
    :param t_max: simulation length
    :param steps: how many steps
    :param progress_bar: tkinter progress_bar
    :return: returns nothing but updates the objects in the list of objects
    """
    t, dt = 0.0, t_max / steps
    while t < t_max:
        for object1 in objects:
            total_force = np.array([0.0, 0.0])
            for object2 in objects:
                if object1 != object2:
                    total_force += np.array(gravity(object1, object2))
            object1.velocity += total_force * (1 / object1.mass) * dt
            object1.position += object1.velocity * dt
            object1.pos_list.append(object1.position.tolist())
            object1.vel_list.append(object1.velocity.tolist())
        t += dt
        if t * 1000 / t_max % 10 == 0:
            progress_bar.step(0.99999)
            progress_bar.update_idletasks()


def plot(objects, scale, filename, save=True):
    """
    takes a list of objects and plots them
    :param objects: objects to plot
    :param scale: scale of the plot
    :param filename: filename of the plot
    :param save: boolean to decide weather to save or show
    :return: has no return
    """
    plt.figure(0)
    plt.axes(xlim=(-scale, scale), ylim=(-scale, scale))
    for obj in objects:
        x, y = zip(*obj.pos_list)
        plt.plot(x, y, label=obj.name)
    plt.title('Orbits')
    plt.xlabel('x')
    plt.ylabel('y')
    # plt.legend(loc='lower right')
    if save:
        plt.savefig('data/saves/' + filename + '.png')
    else:
        plt.show()


def animate(objects, scale, frames, filename, save=True):
    """
    creates an animation of objects trajectory over time
    :param objects: list of objects
    :param scale: scale of the animation
    :param frames: frames of the animation
    :param filename: filename of the animation
    :param save: boolean to decide weather to save or show
    :return: has no return
    """
    fig = plt.figure(1)
    ax1 = plt.axes(xlim=(-scale, scale), ylim=(-scale, scale))
    lines = []
    for _ in objects:
        obj = ax1.plot([], [])[0]
        lines.append(obj)

    def init():
        for line in lines:
            line.set_data([], [])
        return lines

    def update(i):
        counter = 0
        for line in lines:
            x, y = zip(*objects[counter].pos_list)
            x_next = x[0:i]
            y_next = y[0:i]
            line.set_data(x_next, y_next)
            counter += 1
        return lines

    ani_object = ani.FuncAnimation(fig, update, init_func=init, frames=frames, interval=10, blit=True)
    plt.title('Orbits')
    plt.xlabel('x')
    plt.ylabel('y')
    if save:
        ani_object.save('data/saves/' + filename + '.mp4', fps=30, extra_args=['-vcodec', 'libx264'])
    else:
        plt.show()


def datain(filename):
    """
    reads out the initial conditions and initializes the objects
    :param filename:
    :return: list of objects
    """
    objects = []
    with open('data/' + filename, 'r') as file:
        reader = csv.reader(file)
        reader.__next__()
        for row in reader:
            body = Object()
            body.name = row[0].strip()
            body.mass = float(row[1])
            body.position = np.array([float(row[2]), float(row[3])])
            body.velocity = np.array([float(row[4]), float(row[5])])
            body.pos_list = [body.position.tolist()]
            body.vel_list = [body.velocity.tolist()]
            objects.append(body)
        return objects


def dataout(objects):
    """
    writes all calculated values into a file
    :param objects: objects of witch the data is written
    :return: has no return
    """
    for obj in objects:
        file = open('data/objects/' + obj.name, 'w')
        for i in range(len(obj.pos_list)):
            file.write(str(obj.pos_list[i]) + str(obj.vel_list[i]) + '\n')
        file.close()


def randomize(quantity, m_min, m_max, pos, vel, star_mass):
    """
    creates a list of objects with random attributes in certain ranges
    :param quantity: number of objects
    :param m_min: min mass
    :param m_max: max mass
    :param pos: position parameter
    :param vel: velocity parameter
    :param star_mass: mass of central star
    :return: the list of objects
    """
    objects = []
    star = Object()
    star.name = 'star'
    star.mass = star_mass
    star.position = np.array([0.0, 0.0])
    star.velocity = np.array([0.0, 0.0])
    star.pos_list = [star.position.tolist()]
    star.vel_list = [star.velocity.tolist()]
    objects.append(star)
    for i in range(quantity):
        body = Object()
        body.name = str(i + 1)
        body.mass = rd.uniform(m_min, m_max)
        body.position = np.array([rd.uniform(-pos, pos), rd.uniform(-pos, pos)])
        body.velocity = np.array([rd.uniform(-vel, vel), rd.uniform(-vel, vel)])
        body.pos_list = [body.position.tolist()]
        body.vel_list = [body.velocity.tolist()]
        objects.append(body)
    return objects


def utility():
    """
    utility function that takes care of some things
    :return:
    """
    if not os.path.exists('data/objects'):
        os.makedirs('data/objects')
    if not os.path.exists('data/saves'):
        os.makedirs('data/saves')


def main(years, steps, rnd, pv, pvs, av, avs, dv, system, qu, filename, progress_bar):
    """
    main program
    :param years: how many years
    :param steps: how many steps
    :param rnd: randomize the simulation or use preset?
    :param pv: plot it or not
    :param pvs: save plot or show
    :param av: animate it or not
    :param avs: save animation or not
    :param dv: write raw data to files or not
    :param system: what system (preset)
    :param qu: quantity of randomized objects
    :param filename: name of the plots
    :param progress_bar: tkinter progressbar
    :return:
    """
    utility()
    t_max = 365 * 24 * 60 * 60 * years.get()
    objects = []
    if rnd.get():
        objects = randomize(qu.get(), 1e21, 1e23, 1e11, 1e5, 2.0e30)
    else:
        if system.get() == 'Sol':
            objects = datain('sol')
            print('ok')
        if system.get() == 'Alpha Centauri':
            sys.exit('not implemented yet')
        if system.get() == 'Sol (moons)':
            objects = datain('sol(moons)')
            print('ok')

    calculate(objects, t_max, steps.get(), progress_bar)

    if dv.get():
        dataout(objects)
    if pv.get():
        plot(objects, 1e12, filename.get(), pvs.get())
    if av.get():
        animate(objects, 1e12, steps.get(), filename.get(), avs.get())
