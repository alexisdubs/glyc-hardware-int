This software is an example of how to use GlycoPy for model predictive control.
Author: Alexis Dubs adubs@mit.edu
github: https://github.com/alexisdubs/glyc-hardware-int


main.py is the script one would run.
One would need to download GlycoPy separately. Details on this can be found in the GlycoPy user guide.
Parts of this script that are relevant to other users are how to import the needed object from GlycoPy (lines 10, 30-36). The user would edit glycopy_path to be a string describing where the glycopy code is stored relative to the main.py script currently being run (line 10). Lines 30-36 then add the relevant file from GlycoPy to the system path and import the MPCWrapper object.
Line 43 shows the creation of an instance of the MPCWrapper object.
Line 54 then shows the use of this object to call the move_one_step child function. The input to this function is the data from the system. This data should be a dataframe, formatted as in the example_df.xlsx included. The time column should be in hours since the process started.
Finally, since we are using the MPCWrapper object to store the past data and simulation results for the run, the script wherein you instatiate this object should not stop running until the creation of your run. This is accomplished here with a while True loop.