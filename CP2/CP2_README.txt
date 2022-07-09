s1739768 MVP CP2: Cellular automata

To run any .py file, best to run from command line.

CP2_submission includes:

Conway's Game of Life:

	Game_of_life_class.py - Does nothing on its own, has a 2D lattice
	class. Is required to be in same directoy as Game_of_life_play.py
	for it to work.

	Game_of_life_play.py - User is required to provide the system size
	as argument N=50 for example for a 50x50 lattice. Optionally give
	'glider' or 'blinker' as a second argument for special initial
	conditions. Then user is prompted if they would like it animated.
	If yes then displays an animation using plt.imshow(). If no then
	it collects data for the steady state time experiment unless
	'glider' was also passed, in which case it does the glider speed
	experiment instead.

	GOLplots.ipynb - Jupyter notebook doing the data analysis for both
	experiments. Uses GOL_glider_com.csv and GOL_ss_times.csv generated
	by Game_of_life_play.py for the data.

SIRS Model:
	
	SIRS_class.py - 2D lattice class for SIRS model this time.

	SIRS_play.py - Solely for animation. Must provide system size, p1,
	p2 and p3. Uses plt.imshow().

	SIRS_phases.py - Plots phase diagram for fixed p2=0.5. The colour
	denotes the mean infected fraction over 900 sweeps in the steady
	state. Also makes a variance plot to highlight the phase boundary
	ie. where we might see infection come in waves. Writes data to
	SIRS_phase_diagram.csv and output plot is Phasediagram.png.

	SIRS_variance.py - Plots scaled variance of infected number for slice
	of phase diagram p1 = 0.2 to 0.5. Calculations are done over 9900
	sweeps for each value of p1. Peak at p1 ~= 0.32 shows where system
	can't decide whether to be an absorbing state or dynamic equilibrium
	so gives maximum variance and is where we expect waves. Writes data
	to SIRS_variance_data.csv and output plot is Variance.png where
	errorbars are given by the bootstrap resampling method.

	SIRS_immune.py - Plots mean infected fraction against immune
	fraction going from 0 to 1. Writes data to SIRS_immunity_data.csv
	and output plot is Immunity_allp_05.png for p1=p2=p3=0.5. We see an
	immune fraction of ~= 0.3 is enough to stop the spread of infection.
	I also ran it for the case of p1=0.8, p2=0.1 and p3=0.02 from
	lecture recording 6 but unsure if it's needed. If it is then the
	corresponding data file and plot are SIRS_immunity_data2.csv and
	Immunity_p1_08_p2_01_p3_002.png and the immune fraction required to
	stop infection spreading is ~= 0.36. Error bars are given by the
	standard error of the mean across 5 runs.
	
	Example
	Parameters leading to an abdsorbing state: p1=0.2, p2=0.5, p3=0.2
	Parameters leading to a dynamic equilibrium: p1=0.8, p2=0.5, p3=0.8
	Parameters leading to waves of indection: p1=0.8, p2=0.1, p3=0.01
	(Waves are more visually clear for a 100x100 lattice rather than
	50x50)

Thanks.

	