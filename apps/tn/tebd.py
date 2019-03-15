from viznet import theme, EdgeBrush, DynamicShow, Grid, NodeBrush


def tebd():
    # define a grid with grid space dx = 1, and dy = 1.
    grid = Grid((1, 1))

    # define a set of brushes.
    # NodeBrush can place a node at some location, like `node_brush >> (x, y)`,
    # and it will return a Node instance.
    # EdgeBrush can connect two Nodes (or Pin as a special Node),
    # like `edge_brush >> node_a, node_b`, and will return an Edge instance.
    size = 'normal'
    mps = NodeBrush('tn.mps', size=size)
    # invisible node can be used as a placeholder
    invisible_mps = NodeBrush('invisible', size=size)
    # define a two site mpo, which will occupy 1 column, 0 rows.
    mpo21 = NodeBrush('tn.mpo', size=size)
    edge = EdgeBrush('-', lw=2.)

    with DynamicShow((6, 4), filename='_tebd.png') as ds:
        # add a sequence of mps nodes, a store them in a list for future use.
        mps_list = []
        for i in range(8):
            mps_list.append(mps >> grid[i, 0])
            mps_list[-1].text(r'$\sigma_%d$' % i, position='bottom')
        mps_list.append(invisible_mps >> grid[i + 1, 0])

        # add mpo and connect nodes
        for layer in range(4):
            # set brush color, it will overide theme color!
            # You can set brush color to None to restore theme color.
            mpo21.color = theme.RED if layer % 2 == 0 else theme.GREEN
            mpo_list = []
            start = layer % 2
            for i, (mps_l, mps_r) in enumerate(zip(mps_list[start::2],
                                                   mps_list[start + 1::2])):
                # place an two site mpo slightly above the center of two mps nodes
                y = mps_l.position[1]+layer + 1
                mpo_list.append(mpo21 >> grid[mps_l.position[0]:mps_r.position[0], y:y])
                if layer == 0:
                    # if this is the first mpo layer, connect mps and newly added mpo.
                    pin_l = mps_l
                    pin_r = mps_r
                else:
                    # otherwise, place a pin at the top surface of previous mpo,
                    # we also require it horizontally aligned to some `mps_l` object.
                    # pin is a special node, which is zero sized,
                    # we can use it to connect nodes, add texts.
                    # if you're about to place some pin at `left` or
                    # `right` surface of a node,
                    # align is then intepreted as vertial align.
                    pin_l = mpo_list_pre[i].pin('top', align=mps_l)
                    pin_r = mpo_list_pre[i].pin('top', align=mps_r)
                if layer < 2:
                    edge >> (mps_l, mps_r)
                edge >> (pin_l, mpo_list[-1].pin('bottom', align=mps_l))
                edge >> (pin_r, mpo_list[-1].pin('bottom', align=mps_r))
            mpo_list_pre = mpo_list


if __name__ == '__main__':
    tebd()
