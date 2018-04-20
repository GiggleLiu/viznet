from viznet import theme, NodeBrush, EdgeBrush, DynamicShow


def tebd():
    with DynamicShow((4, 4), filename='_contract.png') as ds:
        size = 'normal'
        mps = NodeBrush('tn.mps', size=size)
        # invisible node can be used as a placeholder
        invisible = NodeBrush('invisible', ds.ax, size=size)
        left = NodeBrush('box', size=(0.3, 1.3), color='#333333')
        mpo = NodeBrush('tn.mpo', size=size)
        edge = EdgeBrush('---', ds.ax, lw=2.)
        l = left >> (0, 1)
        dn = mps >> (1.2, 0)
        up = mps >> (1.2, 2.0)
        o = mpo >> (1.2, 1)
        dn_ = invisible >> (2.2, 0)
        up_ = invisible >> (2.2, 2.0)
        o_ = invisible >> (2.2, 1)
        for i, r in enumerate([up, o, dn]):
            ei = edge >> (l.pin('right', align=r), r)
            ei.text('%d'%(i+1), 'top', fontsize=16)
        euo = edge >> (up, o)
        edo = edge >> (dn, o)
        euo.text(4, 'right', fontsize=16)
        edo.text(5, 'right', fontsize=16)
        euu = edge >> (up, up_)
        eoo = edge >> (o, o_)
        edd = edge >> (dn, dn_)
        euu.text(6, 'top', fontsize=16)
        eoo.text(7, 'top', fontsize=16)
        edd.text(8, 'top', fontsize=16)


if __name__ == '__main__':
    tebd()
