
docker build -t ibisba/rpranker .
docker run -it ibisba/rpranker /bin/bash

python wrapRPreader.py -compounds ../rpFBA/input/muconic_acid/compounds.txt -scope ../rpFBA/input/muconic_acid/results.csv -compartments ../rpFBA/input/muconic_acid/compartments.csv -chemicals ../rpFBA/input/muconic_acid/chemicals.csv -outPaths ../rpFBA/input/muconic_acid/out_paths.csv -outSBMLtar outSBMLtar

python wrapRPthermo.py -inSBMLtar outSBMLtar -outSBMLtar outSBMLtar_thermo
