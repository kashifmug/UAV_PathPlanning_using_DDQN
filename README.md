## Table of contents

* [Introduction](#introduction)
* [Requirements](#requirements)
* [How to use](#how-to-use)
* [Resources](#resources)
* [Reference](#reference)
* [License](#
* license)

## Introduction

This repository contains an implementation of the double deep Q-learning (DDQN) approach to control a UAV on a coverage path planning mission, including global-local map processing.


## Requirements

```
python==3.8.10
 
 or newer
numpy==1.24.4 or newer
keras==2.10.0 or newer
tensorflow==2.10.0 or newer
matplotlib==3.7.1 or newer
scikit-image==0.16.2 or newer
tqdm==4.45.0 or newer
opencv-python=4.7.0 or newer
```


## How to use

Train a new DDQN model with the parameters of your choice in the specified config file for CPP or DH:

```
python main.py --cpp --gpu --config config/manhattan32_cpp.json --id manhattan32_cpp

--cpp                       Activates CPP 
--gpu                       Activates GPU acceleration for DDQN training
--config                    Path to config file in json format
--id                        Overrides standard name for logfiles and model
--generate_config           Enable only to write default config from default values in the code
```

Evaluate a model through Monte Carlo analysis over the random parameter space for the performance indicators 'Successful Landing', 'Collection Ratio', 'Collection Ratio and Landed' as defined in the paper (plus 'Boundary Counter' counting safety controller activations), e.g. for 1000 Monte Carlo iterations:

```
python main_mc.py --cpp --weights example/models/manhattan32_cpp --config config/manhattan32_cpp.json --id manhattan32_cpp_mc --samples 1000


--cpp                       Activates CPP 
--weights                   Path to weights of trained model
--config                    Path to config file in json format
--id                        Name for exported files
--samples                   Number of Monte Carlo  over random scenario parameters
--seed                      Seed for repeatability
--show                      Pass '--show True' for individual plots of scenarios and allow plot saving
```

For an example run of pretrained agents the following commands can be used:
```
python main_scenario.py --cpp --config config/manhattan32_cpp.json --weights example/models/manhattan32_cpp --scenario example/scenarios/manhattan_cpp.json --video

```

## Resources

The city environments from the paper 'manhattan32' are included in the 'res' directory. Map information is formatted as PNG files with one pixel representing on grid world cell. The pixel color determines the type of cell according to

* red #ff0000 no-fly zone (NFZ)
* blue #0000ff start and landing zone
* yellow #ffff00 buildings blocking wireless links (also obstacles for flying)

If you would like to create a new map, you can use any tool to design a PNG with the same pixel dimensions as the desired map and the above color codes.

The shadowing maps, defining for each position and each IoT device whether there is a line-of-sight (LoS) or non-line-of-sight (NLoS) connection, are computed automatically the first time a new map is used for training and then saved to the 'res' directory as an NPY file. The shadowing maps are further used to determine which cells the field of view of the camera in a CPP scenario.


## Reference

If using this code for research purposes, please cite:

[1] M. Theile, H. Bayerlein, R. Nai, D. Gesbert, M. Caccamo, “UAV Path Planning using Global and Local Map Information with Deep Reinforcement Learning" arXiv:2010.06917 [cs.RO], 2020. 

```
@article{Theile2020,
        author  = {Mirco Theile and Harald Bayerlein and Richard Nai and David Gesbert and Marco Caccamo},
        title   = {{UAV} Path Planning using Global and Local Map Information with Deep Reinforcement Learning},
        journal = {arXiv:2010.06917 [cs.RO]},
        year    = {2020},
        url     = {https://arxiv.org/abs/2010.06917}
}
```


## License 

This code is under a BSD license.