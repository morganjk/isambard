# ISAMBARD

### Intelligent System for Analysis, Model Building And Rational Design.

### Release 2017.3.0 (Oct 9th, 2017), Woolfson Group, University of Bristol.

[![Chat](https://img.shields.io/badge/chat-riot.im-green.svg)](https://riot.im/app/#/group/+isambard:matrix.org)
[![Documentation](https://img.shields.io/badge/docs-master-orange.svg)](https://woolfson-group.github.io/isambard/)
[![CircleCI](https://circleci.com/gh/woolfson-group/isambard.svg?style=shield&circle-token=27387ac82a6d30c7bd6a72ce3214fa57677e9d87)](https://circleci.com/gh/woolfson-group/isambard)
[![codecov](https://codecov.io/gh/woolfson-group/isambard/branch/master/graph/badge.svg)](https://codecov.io/gh/woolfson-group/isambard)
[![Python Version](https://img.shields.io/badge/python-3.5%2C%203.6-lightgrey.svg)](https://woolfson-group.github.io/isambard/)
[![MIT licensed](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/woolfson-group/isambard/blob/master/LICENSE.md)

ISAMBARD (Intelligent System for Analysis, Model Building And Rational Design), is a Python-based framework for 
structural analysis and rational design of biomolecules, with a particular focus on parametric modelling of proteins. It is developed and maintained by members of the
[Woolfson group, University of Bristol](http://www.chm.bris.ac.uk/org/woolfson/index.html).

Need help getting started? Please visit the [New Users room](https://riot.im/app/#/room/#isambard-new-users:matrix.org) in the ISAMBARD community on riot.im. You don't need to create an account to ask questions. Alternatively, you can raise an issue in the GitHub repository.

### Citing ISAMBARD
Any publication arising from use of the ISAMBARD software package should cite the following reference:

[Wood CW *et al* (2017) ISAMBARD: an open-source computational environment for biomolecular analysis, modelling and design. *Bioinformatics*, **33**, 3043-50](https://doi.org/10.1093/bioinformatics/btx352)

## Basic Install

ISAMBARD can be installed straight from PyPI using `pip`:

```
pip install isambard
```
Or if you want to try an experimental build, download from GitHub either by downloading the zipped file or cloning, then navigate to the ISAMBARD folder and type:

```
python setup.py install
```

ISAMBARD has a few Python package requirements, just install them through pip if it asks for them. We recommend using the [Anaconda Python 3 distribution](https://www.continuum.io/downloads), it contains most of the dependencies.

If you're having trouble installing ISAMBARD take a look at the [troubleshooting](https://github.com/woolfson-group/isambard/wiki/Installation-Troubleshooting) section of the wiki, especially if you're on a bleeding-edge Linux distro like Arch.

## External Programs

To get the most out of ISAMBARD, a couple of external programs are recommended:

1. [Scwrl4](http://dunbrack.fccc.edu/scwrl4/) - Used to pack sidechains, it's fast and accurate. Free for non-commercial use.
1. [DSSP](http://swift.cmbi.ru.nl/gv/dssp/) - Used to find secondary structure in models. Free to download.

When you first import ISAMBARD you'll be asked to give paths to the executables for the dependencies. These are not required to use ISAMBARD, if you don't want to use any of them, just leave the path blank. Once you've finished setting your paths and some other options, a small file called `.isambard_settings` will be made in your home directory, which contains your settings. If you ever want to rerun the configure script that runs when you first import, you can run the following command:

```python
import isambard
isambard.settings.configure()
```

`.isambard_settings` is simple JSON config file, if you're having any trouble with your settings, you can tinker with it manually. You can find an example `.isambard_settings` file [here](https://github.com/woolfson-group/isambard/wiki/Example-%60.isambard_settings%60-file).

Chat with us on riot.im if you get stuck (link above), or raise an issue!

## Once ISAMBARD is installed...

You might want to take a look at the [wiki](https://github.com/woolfson-group/isambard/wiki), there are a range of tutorials that demonstrate various aspects of ISAMBARD. These are IPython notebooks, so please download them and run through them (modify/hack/break them) on your own machine.

Wanting to delve a bit deeper? Take a look at the [docs](https://woolfson-group.github.io/isambard/) to find out more of the features in ISAMBARD, or just take a look through the code base and hack around. Remember, feel free to contact us on Gitter, email or through the issues if you get stuck.

## Unit tests 
To ensure that the package is correctly installed unit tests can be run by:

`python -m unittest discover unit_tests/`

## Releases

### 2017.3.0
Adds the `evo_optimizers.py` module, which is a reworked version of 
`optimizers.py`. The aim was to create a flexible and consistent interface to
the evolutionary optimizers. Usage is slightly different, see [this
Gist](https://gist.github.com/ChrisWellsWood/8647d965de2e3c68620daa2dc64de42a)
for examples. The old optimizer module still exists, but a `PendingDeprecation`
warning has been added, as it will be removed in version 2.0.0.

### 2017.2.4
Fixes a bug with `BuffScore.inter_scores` returned from `score_interactions`
where the interactions did not match the score. _This bug had no impact on the
absolute value of the `BuffScore` or any of the component scores._

### 2017.2.3
Fixes issue with files excluded from module.

### 2017.2.2
Improved error handling for `Residue.backbone`.

### 2017.2.1
Adds a large amount of documentation.

### 2017.2.0
Adds new functionality for working with non-canonical amino acids.

### 2017.1.0
ISAMBARD now contains an add ons module containing code for structural analysis of coiled coils.

### 2017.0.1
The release contains a range of tweaks and bug fixes, including a major bug in the model building of anti-parallel helices in coiled coils.

## Principal Investigator
* Derek N. Woolfson
  * Email: d.n.woolfson@bristol.ac.uk

## Developers - Core Dev Team
### Woolfson Group
* Gail J. Bartlett 
  * Email: g.bartlett@bristol.ac.uk
* Jack W. Heal
  * Email: jack.heal@bristol.ac.uk
  * Twitter: @JackHeal
* Kieran L. Hudson
  * Email: kieran.hudson@bristol.ac.uk
* Andrew R. Thomson
  * Email: drew.thomson@bristol.ac.uk
* Christopher W. Wood
  * Email: chris.wood@bristol.ac.uk
  * Twitter: @ChrisWellsWood

## Contributors
### Woolfson Group
* Caitlin Edgell
* Kathryn L. Porter Goff

## BUDE Dev Team
### Sessions Group
* Amaurys À. Ibarra
  * Email: amaurys.avilaibarra@bristol.ac.uk
* Richard B. Sessions
  * Email: r.sessions@bristol.ac.uk
