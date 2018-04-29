# Circuit Visualization Protocal
## Gate Representation
* Non-Parametric Single-Qubit Gates like `G(line)`, where `line` is an integer

    * C, NC  # Control and N-Control
    * X, Y, Z, H
    * NOT
* Non-Parametric Multi-Qubit Gates like `G(lines)`, where `lines` can be an integer, slice or list, e.g. `2`, `1&2&3`, `1:4` (which is equivalent to `1&2&3`).

    * Swap  # number of line must be 2.
    * Focus
    * Measure
    * End
* Parametric Gates like `G(line(s), floats)`, `floats` here can be e.g. `0.2&0.3`, `0.2`.

    * Rx, Ry, Rz
    * Rot
* General Gates with Names like `G(line(s), text, float(s))`,
if no parameter, it is `G(line(s), text,)`.

    * G

## Block Tree
* `blocks` contains a list of blocks, and for each block, it contains

    * name: str
    * nline: int
    * blocks: list
    * DISP_OFFSETX: float
    * DISP: bool, whether this box is visible.

Where `DISP*` variables are for display purpose, which is not related to circuit definition.

## Notes

####  Reserved strings for naming a general Gate

* "--" used to split column wise connected gates.
