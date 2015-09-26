#!/usr/bin/env python

'''
Random network with purely inhibitory connections.
Neurons are driven by setting resting potential over spiking threshold.

See also:
Pfeil et al. (2014).
The effect of heterogeneity on decorrelation mechanisms in spiking neural networks: a neuromorphic-hardware study.
arXiv:1411.7916 [q-bio.NC].
'''

# for plotting without X-server
import matplotlib as mpl
mpl.use('Agg')

import pyNN.hardware.spikey as pynn
import numpy as np

pynn.setup()

# set resting potential over spiking threshold
runtime = 1000.0 #ms
popSize = 192
weight = 7.0 * pynn.minExcWeight()
neuronParams = {'v_rest': -40.0}

neurons = pynn.Population(popSize, pynn.IF_facets_hardware1, neuronParams)
pynn.Projection(neurons, neurons, pynn.FixedNumberPreConnector(15, weights=weight), target='inhibitory')
neurons.record()

pynn.run(runtime)

spikes = neurons.getSpikes()

pynn.end()

# save data
print 'Saving data'
np.savetxt('spikes.dat', spikes)

# visualize
print 'Plotting data'
import matplotlib.pyplot as plt

color = 'k'

plt.figure()
plt.plot(spikes[:,1], spikes[:,0], ls='', marker='o', ms=1, c=color, mec=color)
plt.xlim(0, runtime)
plt.xlabel('time (ms)')
plt.ylabel('neuron ID')
plt.ylim(-0.5, popSize - 0.5) 
plt.savefig('raster_plot.png')
