import pdb
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation

class DynamicShow():
    '''
    Dynamic plot context, intended for displaying geometries.
    like removing axes, equal axis, dynamically tune your figure and save it.

    Args:
        figsize (tuple, default=(6,4)): figure size.
        filename (filename, str): filename to store generated figure, if None, it will not save a figure.

    Attributes:
        figsize (tuple, default=(6,4)): figure size.
        filename (filename, str): filename to store generated figure, if None, it will not save a figure.
        ax (Axes): matplotlib Axes instance.

    Examples:
        with DynamicShow() as ds:
            c = Circle([2, 2], radius=1.0)
            ds.ax.add_patch(c)
    '''

    def __init__(self, figsize=(6, 4), filename=None, dpi=300, fps=1):
        self.figsize = figsize
        self.filename = filename
        self.ax = None
        self.steps = []
        self.fps = fps

    def __enter__(self):
        plt.ion()
        plt.figure(figsize=self.figsize)
        self.ax = plt.gca()
        return self

    def __exit__(self, exc_type, exc_val, traceback):
        if traceback is not None:
            return False
        plt.axis('equal')
        plt.axis('off')
        plt.tight_layout()
        if self.filename[-4:] in [".gif", ".mp4"]:
            nframe = len(self.steps)+1

            def update(i):
                if i!=0:
                    self.steps[i-1]()

            anim = FuncAnimation(plt.gcf(), update, frames=range(nframe), repeat=False)
            pdb.set_trace()
            anim.save(self.filename, writer="imagemagick", fps=self.fps)
        elif self.filename is not None:
            print('Press `c` to save figure to "%s", `Ctrl+d` to break >>' %
                  self.filename)
            pdb.set_trace()
            plt.savefig(self.filename, dpi=300, transparent=True)
        else:
            pdb.set_trace()
        return True
