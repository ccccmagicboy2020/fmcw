

# This file was *autogenerated* from the file /home/matt/src/fmcw-radar/fpga/hdl/tb/sage-sim.sage
from sage.all_cmdline import *   # import sage library

_sage_const_3 = Integer(3); _sage_const_2 = Integer(2); _sage_const_1 = Integer(1); _sage_const_0 = Integer(0); _sage_const_4 = Integer(4); _sage_const_16 = Integer(16)
N = _sage_const_16   # input sequence length
Nstages = int(log(N, _sage_const_4 ))
T = _sage_const_2 *N  # number of timesteps

vars = {}


def set_var(var, val):
    """Convenience function for setting the values of Sage variables."""
    sage_eval('None', cmds="{}={}".format(var, val), locals=vars)


def get_var(var):
    """Convenience function for getting the values of Sage
    variables. Basically, it's just a reminder that we need to access
    the variable through `vars'."""
    return vars[var]


# input sequence
# var(["x{}".format(i) for i in range(T)])
for t in range(T):
    sage_eval('None', cmds="x{0}=var('x{0}')".format(t), locals=vars)

# # feedback shift registers
# # stage 0 butterfly 1
# for t in range(T):
#     for n in range(Nstages):
#         var(["s{}bf1_fsr{}_t{}".format(n, i, t)
#              for i in range(int(N/(2**(n+1))))])
#         var(["s{}bf2_fsr{}_t{}".format(n, i, t)
#              for i in range(int(N/(2**(n+1))))])

# # stage outputs
# for t in range(T):
#     var(["s{}bf1_out_t{}".format(i, t) for i in range(Nstages)])
#     var(["s{}bf2_out_t{}".format(i, t) for i in range(Nstages)])

# # select lines
# for t in range(T):
#     var(["sel_s{}bf1_t{}".format(i, t) for i in range(Nstages)])
#     var(["sel_s{}bf2_t{}".format(i, t) for i in range(Nstages)])

# set values of select lines
for t in range(T):
    for n in range(Nstages):
        tstart = _sage_const_0 
        for ni in range(_sage_const_2 *n+_sage_const_1 ):
            tstart += int(N/(_sage_const_2 **(ni+_sage_const_1 )))
        tstart += _sage_const_1 
        tend = tstart + N - int(N/(_sage_const_2 **(_sage_const_2 *n+_sage_const_1 )))
        if t in range(tstart, tend+_sage_const_1 ):
            set_var("sel_s{}bf1_t{}".format(n, t), _sage_const_1 )
        else:
            set_var("sel_s{}bf1_t{}".format(n, t), _sage_const_0 )

        tstart = _sage_const_0 
        for ni in range(_sage_const_2 *n+_sage_const_1 +_sage_const_1 ):
            tstart += int(N/(_sage_const_2 **(ni+_sage_const_1 )))
        tstart += _sage_const_1 
        tend = tstart + N - int(N/(_sage_const_2 **(_sage_const_2 *n+_sage_const_1 +_sage_const_1 )))
        if t in range(tstart, tend+_sage_const_1 ):
            set_var("sel_s{}bf2_t{}".format(n, t), _sage_const_1 )
        else:
            set_var("sel_s{}bf2_t{}".format(n, t), _sage_const_0 )

# twiddle factors
for s in range(Nstages-_sage_const_1 ):
    for k in [_sage_const_0 , _sage_const_2 , _sage_const_1 , _sage_const_3 ]:
        Ngroups = int(N/_sage_const_2 **(_sage_const_2 *s+_sage_const_2 ))
        for n in range(Ngroups):
            if (k == _sage_const_0 ):
                k_idx = _sage_const_0 
            elif (k == _sage_const_2 ):
                k_idx = _sage_const_1 
            elif(k == _sage_const_1 ):
                k_idx = _sage_const_2 
            else:
                k_idx = _sage_const_3 
            w = exp(-_sage_const_2 *pi*I*_sage_const_4 **s*n*k/N)
            offset = _sage_const_0 
            while (get_var("sel_s{}bf2_t{}".format(s, offset)) == _sage_const_0 ):
                offset += _sage_const_1 
            # TODO this fails for more than 1 multiplier. The values
            # should repeat
            set_var("s{}_w_t{}".format(s, Ngroups*k_idx+n+offset), w)
            for i in range(_sage_const_0 , offset):
                set_var("s{}_w_t{}".format(s, i), _sage_const_1 )
            for i in range(T, offset+N, -_sage_const_1 ):
                set_var("s{}_w_t{}".format(s, i), _sage_const_1 )

# initialize variables
for t in range(T):
    for s in range(Nstages):
        for n in range(int(N/(_sage_const_2 **(_sage_const_2 *s+_sage_const_1 )))):
            set_var("s{}bf1_fsr{}_t{}".format(s, n, t), _sage_const_0 )
        for n in range(int(N/(_sage_const_2 **(_sage_const_2 *s+_sage_const_2 )))):
            set_var("s{}bf2_fsr{}_t{}".format(s, n, t), _sage_const_0 )

        set_var("s{}bf1_out_t{}".format(s, t), _sage_const_0 )
        set_var("s{}bf2_out_t{}".format(s, t), _sage_const_0 )


# simulation
for t in range(_sage_const_1 , T):
    for s in range(Nstages):
        # bf1
        max_fsr_bf1 = int(N/_sage_const_2 **(_sage_const_2 *s+_sage_const_1 )-_sage_const_1 )
        for n in range(_sage_const_1 , max_fsr_bf1+_sage_const_1 ):  # shift reg values
            set_var("s{}bf1_fsr{}_t{}".format(s, n, t),
                    get_var("s{}bf1_fsr{}_t{}".format(s, n-_sage_const_1 , t-_sage_const_1 )))

        if (get_var("sel_s{}bf1_t{}".format(s, t)) == _sage_const_0 ):  # mux 0
            set_var("s{}bf1_fsr{}_t{}".format(s, _sage_const_0 , t),
                    get_var("x{}".format(t-_sage_const_1 )))
            set_var("s{}bf1_out_t{}".format(s, t),
                    get_var("s{}bf1_fsr{}_t{}".format(s, max_fsr_bf1, t)))
        else:  # mux 1
            set_var("s{}bf1_fsr{}_t{}".format(s, _sage_const_0 , t),
                    get_var("s{}bf1_fsr{}_t{}".format(s, max_fsr_bf1, t-_sage_const_1 ))
                    - get_var("x{}".format(t-_sage_const_1 )))
            set_var("s{}bf1_out_t{}".format(s, t),
                    get_var("s{}bf1_fsr{}_t{}".format(s, max_fsr_bf1, t)))

        # bf2
        max_fsr_bf2 = int(max_fsr_bf1/_sage_const_2 )
        for n in range(_sage_const_1 , max_fsr_bf2+_sage_const_1 ):  # shift reg values
            set_var("s{}bf2_fsr{}_t{}".format(s, n, t),
                    get_var("s{}bf2_fsr{}_t{}".format(s, n-_sage_const_1 , t-_sage_const_1 )))

        if (get_var("sel_s{}bf2_t{}".format(s, t)) == _sage_const_0 ):
            set_var("s{}bf2_fsr{}_t{}".format(s, _sage_const_0 , t),
                    get_var("s{}bf1_out_t{}".format(s, max_fsr_bf1, t-_sage_const_1 )))
            set_var("s{}bf2_out_t{}".format(s, t),
                    get_var("s{}bf2_fsr{}_t{}".format(s, max_fsr_bf2, t)))
        elif (get_var("sel_s{}bf2_t{}".format(s, t)) == _sage_const_1  and
              get_var("sel_s{}bf1_t{}".format(s, t)) == _sage_const_1 ):
            set_var("s{}bf2_fsr{}_t{}".format(s, _sage_const_0 , t),
                    get_var("s{}bf2_fsr{}_t{}".format(s, max_fsr_bf2, t-_sage_const_1 ))
                    - get_var("s{}bf1_out_t{}".format(s, t-_sage_const_1 )))
            set_var("s{}bf2_out_t{}".format(s, t),
                    get_var("s{}bf2_fsr{}_t{}".format(s, max_fsr_bf2, t))
                    + get_var("s{}bf1_out_t{}".format(s, t)))
        else:
            set_var("s{}bf2_fsr{}_t{}".format(s, _sage_const_0 , t),
                    get_var("s{}bf2_fsr{}_t{}".format(s, max_fsr_bf2, t-_sage_const_1 ))
                    - imag(get_var("s{}bf1_out_t{}".format(s, t-_sage_const_1 )))
                    + I*real(get_var("s{}bf1_out_t{}".format(s, t-_sage_const_1 ))))
            set_var("s{}bf2_out_t{}".format(s, t),
                    get_var("s{}bf2_fsr{}_t{}".format(s, max_fsr_bf2, t))
                    + imag(get_var("s{}bf1_out_t{}".format(s, t)))
                    - I*real(get_var("s{}bf1_out_t{}".format(s, t))))

        if (s % _sage_const_2  == _sage_const_0 ):  # pre-multiplier
            set_var("s{}bf2_out_t{}".format(s, t),
                    get_var("s{}bf2_out_t{}".format(s, t))
                    * get_var("s{}_w_t{}".format(s, t % N)))

        if (s == Nstages-_sage_const_1 ):
            print("t={}: {}".format(t, get_var("s{}bf2_out_t{}".format(s, t))))
