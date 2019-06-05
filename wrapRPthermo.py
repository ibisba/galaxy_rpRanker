#!/usr/bin/env python3

##from io import BytesIO
#from contextlib import closing
#import time
import libsbml
import argparse
import sys #exit using sys exit if any error is encountered
import os
#import tarfile

import zipfile
#from io import StringIO
import io

sys.path.insert(0, '/home/src/')
import rpFBA

'''
## Function that wraps the SBML files into a zip file to be passed to the next galaxy node
#
#
def writerpSBMLtar(rpsbml_paths, outTar):
    with tarfile.open(outTar, 'w:xz') as tf:
        for rpsbml_name in rpsbml_paths:
            data = libsbml.writeSBMLToString(rpsbml_paths[rpsbml_name].document).encode('utf-8')
            fiOut = BytesIO(data)
            info = tarfile.TarInfo(rpsbml_name)
            info.size = len(data)
            tf.addfile(tarinfo=info, fileobj=fiOut)


## Function that takes for input a tar of the collection of rpSBML files and reads them to memory
#
#
def readrpSBMLtar(inputTar):
    rpsbml_paths = {}
    tar = tarfile.open(inputTar)
    for member in tar.getmembers():
        rpsbml_paths[member.name] = rpFBA.rpSBML(member.name,libsbml.readSBMLFromString(tar.extractfile(member).read().decode("utf-8")))
    return rpsbml_paths
'''


## 
#
#
def writerpSBMLzip(rpsbml_paths, outZip):
    zip_buffer = io.BytesIO()
    #with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zip_file:
    with zipfile.ZipFile(zip_buffer, mode="a", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zip_file:
        for rpsbml_name in rpsbml_paths:
            data = libsbml.writeSBMLToString(rpsbml_paths[rpsbml_name].document).encode('utf-8')
            data = io.BytesIO(bytes(data))
            zip_file.writestr(rpsbml_name, data.getvalue())
    with open(outZip, 'wb') as f:
        f.write(zip_buffer.getvalue())
    

##
#
#
def readrpSBMLzip(inputZip):
    input_zip = zipfile.ZipFile(inputZip)
    rpsbml_paths = {}
    for name in input_zip.namelist():
        rpsbml_paths[name] = rpFBA.rpSBML(name, libsbml.readSBMLFromString(input_zip.read(name).decode("utf-8")))
    return rpsbml_paths


'''
def writerpSBMLzip(rpsbml_paths, outZip):
    zf = ZipFile(in_memory, mode="w")
    for rpsbml_name in rpsbml_paths:
        data = libsbml.writeSBMLToString(rpsbml_paths[rpsbml_name].document).encode('utf-8')
        in_memory = BytesIO(data)
        zf.writestr(data, file_data)
    #Close the zip file
    zf.close()
    #Go to beginning
    in_memory.seek(0)
    #read the data
    data = in_memory.read()
    #You can save it to disk
    with open(outZip,'wb') as out:
      out.write(data)
'''






if __name__ == "__main__":
    parser = argparse.ArgumentParser('Python wrapper for galaxy to calculate thermodynamics of RetroPath heterologous pathway')
    '''
    parser.add_argument('-inSBMLtar', type=str)
    parser.add_argument('-outSBMLtar', type=str) 
    '''
    parser.add_argument('-inSBMLzip', type=str)
    parser.add_argument('-outSBMLzip', type=str) 
    reader = rpFBA.rpReader()
    params = parser.parse_args()
    #read the passed tar
    #rpsbml_paths = readrpSBMLtar(params.inSBMLtar)
    rpsbml_paths = readrpSBMLzip(params.inSBMLzip)
    #calculate the thermo
    rpthermo = rpFBA.rpThermo()
    for rpsbml_name in rpsbml_paths:
        rpthermo.pathway_drG_prime_m(rpsbml_paths[rpsbml_name])
    #package the rpsbml's for the next pathway
    #writerpSBMLtar(rpsbml_paths, params.outSBMLtar)
    writerpSBMLzip(rpsbml_paths, params.outSBMLzip)
    exit(0)
