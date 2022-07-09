s1739768 MVP CP1: 2D Ising Model

I started with the pseudocode provided and copied that into a class.
If needed, it's best to run both programmes run via the command line.

CP1_submission includes:

Three .py files:

	- Ising2D_class.py does nothing on its own. It just contains the Lattice2D
	class. It is required to be in the same directory as Ising2D_animation.py and
	Ising2D_playV2.py for them to work.

	- Ising2D_animation.py outputs animation frames using plt.imshow(). It outputs one
	frame every sweep (NxN attempted spin flips) so looks smooth but takes a while
	to reach the equilibrium steady state but this could be easily changed in the
	code. The initial configuration of spins is random. The user can specify the
	system size N for an NxN lattice and the temperature. After hitting enter, the
	user is prompted for a choice of Glauber or Kawasaki dynamics. Runs for ages
	so best to use Ctrl+C on command line to interrupt it after you get bored.

	- Ising2D_playV2.py makes plots from which the critical temperature can be
	estimated. In this case the user enters the lowest and highest temperatures
	of their desired range. The initial configuration is the equilibrium state at low T
	and the final state of one temperature is the initial state for the next. Choice
	of dynamics is prompted afterwards. A .png file is created of the plots and the
	data is written to a .csv file. Note that running Ising2D_playV2.py will overwrite
	the png and csv included so be careful!

Two .png files:

	- Glauber_plots.png shows plots of mean absolute value of magnetisation, mean energy,
	susceptibility and heat capacity for a 50x50 lattice from T=1.0, 1.1, 1.2,..., 3.0
	using Glauber dynamics. The errors on magnetisation and energy are given by standard
	error on the mean while errors on fluctuations (susceptibility and heat capacity)
	are given by bootstrap resampling).

	- Kawasaki_plots.png is the same for Kawasaki dynamics without the magnetisation
	and susceptibility plots because magnetisation is globally conserved under Kawasaki
	dynamics so does not fluctuate.

From Glauber and Kawasaki fluctuation plots (susceptibility or heat capacity) we see a peak
around T~2.27 where there is most deviation from the average which implies here the system
cannot decide wheter to be ordered or disordered so is an estimate of the critical temperature.

Two .csv files:

	- Ising2D_Glauber_data Ising2D_Kawasaki_data are the data used in the above plots

Note, I forgot to write the temperature to the file so added them afterwards just in case
you thought it was suspicious that np.arange() gives temperatures like 1.20000000001 instead
of 1.2 but I just typed 1.2 in the csv files. Hope that is okay.

Thanks!