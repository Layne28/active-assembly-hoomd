import numpy as np
import matplotlib.pyplot as plt
import sys

import AnalysisTools.particle_io as io
import AnalysisTools.field_analysis as field_analysis
import AnalysisTools.field_particle_correlation as correlation

traj_name = sys.argv[1]
noise_name = sys.argv[2]

traj = io.load_traj(traj_name)
noise = io.load_noise_traj(noise_name)

pressure = -0.5*(traj['virial'][:,:,0] + traj['virial'][:,:,3])

pressure_field = correlation.get_pressure_field()