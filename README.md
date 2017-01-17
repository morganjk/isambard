#ISAMBARD
###Intelligent System for Analysis, Model Building And Rational Design of proteins.
#### Version 1.1.7 (Jan 13, 2017), Woolfson Group, University of Bristol.
[![CircleCI](https://circleci.com/gh/woolfson-group/isambard_dev.svg?style=shield&circle-token=0af7a4c0efd449fda7db2d1deef2745b8d289dcf)](https://circleci.com/gh/woolfson-group/isambard_dev)
[![codecov](https://codecov.io/gh/woolfson-group/isambard_dev/branch/master/graph/badge.svg?token=UEzouOJSdl)](https://codecov.io/gh/woolfson-group/isambard_dev)
[![Gitter](https://img.shields.io/gitter/room/nwjs/nw.js.svg?maxAge=2592000)](https://gitter.im/woolfson-group/isambard?utm_source=share-link&utm_medium=link&utm_campaign=share-link)
[![MIT licensed](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/woolfson-group/isambard/blob/master/LICENSE.md)

## Recent Changes

#### v1.1

##### v1.1.7
* Restructured the scoring optimiser slightl to allow for alternate scoring functions to be more easily used

##### v1.1.6
* Added GOAP - Generalized Orientation-Dependent All-Atom Statistical Potential for protein structure prediction
    * Incorporates DFIRE potential and this can be accessed independently
    * Run using `isambard.external_programs.run_goap(pdb_file, path=True)`, or it will take an `ampal.pdb` object with path=False.

##### v1.1.5
* Added new optimizer classes GA_Opt_Internal and DE_Opt_Internal that will optimize on the BUFF internal energy.

##### v1.1.4
* Functionality that has now been moved to isocket repository (https://github.com/woolfson-group/isocket) has been removed.
* Deleted:
    * coeus database folder (3 modules)
    * graph_theory and test_graph_theory
    * get_protein_dict_from_cif

##### v1.1.3
* knobs_into_holes now uses clustering instead of gen_sectors, which is no longer imported.


##### v1.1.2
* Import now tests presence of dssp with `--version` flag to prevent import hang in jupyter notebook on windows systems

##### v1.1.1
* `BuffForceField` now has a setter for the `distance_cutoff` property, which will overwrite the default cutoff

##### v1.1.0

* Reworked internals of BUFF to find interactions in a more general way
    * Now has a `score_inter_ampal` function in `isambard.buff` that allows interaction energy to be measured between multiple AMPAL

#### v1.0

##### v1.0.0 - 1.0.4
* knobs_into_holes.KnobGroup.from_helices now works as expected with large cutoff values. Testing added accordingly.
* The `settings.json` file is no more!
    * It has been replaced with `.isambard_settings` which is written to the users home directory
* Added files for managing the install using pip or `setup.py`
    * Can now download and run `python setup.py install` in the `isambard_dev` file to install to your python packages
* Added checks for external program availability
    * Will now raise a `DependencyNotFoundWarning` if a function that requires an external program is called without that dependency being available
* Release API structure
    * All parametric model building is now in the specifications folder under either assembly_specs or polymer_specs
    * From this point out, the version number in the development branch will follow full [semantic versioning](http://semver.org/)

#### v0.7

##### v0.7.2
* Added C5 hydrogen bond
    * As defined by Newberry & Raines (Nat Chem Biol 2016)
    * `isambard.ampal.interactions.find_C5HydrogenBonds(ampal)`
    * Unit tests included

##### v0.7.1
* Added `radius_of_gyration` function
* Added 'ignore_hydrogens' flag to `get_atoms()`
* Updated unit tests

##### v0.7.0
* New force field assignment structure
    * Now uses the `update_ff` method to manage caching and updating force field parameters

#### v0.6

##### v0.6.0-0.6.6
* Fixed a bug where the `TAPolypeptie` did not assign the `ampal_parent` attribute during `build`
* `coiledcoil.py`
    * Fixed coiled-coil interface angles in basis set parameters
* `relabel_monomers`
    * Added option for relabelling monomers by an integer value as well as a list of labels
* Fix for `Optimizers` on Windows
    * Will now use `map` rather than `futures.ProcessPoolExecutor().map` if the platform is Windows or only a single core is used
* Minor bug-fix
     * Caught potential error in loop-closure method
* New BUFF Structure
    * All AMPAL objects should now be picklable after scoring
    * BUFF runs 33-50% faster
* Updated interactions.py with non-covalent interaction classes and methods for identifying them
    * N->pi* interactions
    * Cation->pi interactions
    * Simple salt bridge interactions
    * Methionine-aromatic interactions
    * Pi-Pi interactions
    * Hydrogen bonds with C-H group as a donor

[**See full change log**](https://github.com/woolfson-group/isambard_dev/wiki/Change-Log)

##Principal Investigator
Derek N. Woolfson (d.n.woolfson@bristol.ac.uk)
##Developers
###Core Dev Team
####Woolfson Group
Gail J. Bartlett (g.bartlett@bristol.ac.uk)<br>
Jack W. Heal (jack.heal@bristol.ac.uk)<br>
Kieran L. Hudson (kieran.hudson@bristol.ac.uk)<br>
Andrew R. Thomson (drew.thomson@bristol.ac.uk)<br>
Christopher W. Wood (chris.wood@bristol.ac.uk)<br>
###Contributors
####Woolfson Group
Caitlin Edgell<br>
Kathryn L. Porter Goff<br>
###BUDE Dev Team
####Sessions Group
Amaurys À. Ibarra (amaurys.avilaibarra@bristol.ac.uk)<br>
Richard B. Sessions (r.sessions@bristol.ac.uk)<br>
