# openmm-state-to-g96

Convert OpenMM state xml to g96 format

## Usage

```shell
$ usage: state2g96 [-h] -f F [-o O]

Convert OpenMM state xml to g96 format.

optional arguments:
  -h, --help  show this help message and exit
  -f F        OpenMM state xml
  -o O        Output g96 file
```

Have a try

```shell
$ cd example
$ python3 ../src/state2g96.py -f state.xml -o state.g96
```

Then the `state.g96` can be converted into `pdb` or `gro` format with GROMACS

```shell
$ gmx trjconv -f state.g96 -o state.gro -s md.tpr
$ gmx trjconv -f state.g96 -o state.pdb -s md.tpr
```

## License

BSD 2-Clause License
