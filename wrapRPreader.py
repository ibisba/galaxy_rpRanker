#!/usr/bin/env python3

#from io import BytesIO
#from contextlib import closing
#import time

#import tarfile

import libsbml
import argparse
import sys #exit using sys exit if any error is encountered
import os
import sys

import io
import zipfile

sys.path.insert(0, '/home/src/')
import rpFBA

## Function that wraps the SBML files into a zip file to be passed to the next galaxy node
#
'''
def writerpSBMLtar(rpsbml_paths, outTar):
    with tarfile.open(outTar, 'w:xz') as tf:
        for rpsbml_name in rpsbml_paths:
            data = libsbml.writeSBMLToString(rpsbml_paths[rpsbml_name].document).encode('utf-8')
            fiOut = BytesIO(data)
            info = tarfile.TarInfo(rpsbml_name)
            info.size = len(data)
            tf.addfile(tarinfo=info, fileobj=fiOut)
'''


def writerpSBMLzip(rpsbml_paths, outZip):
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, mode="a", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zip_file:
        for rpsbml_name in rpsbml_paths:
            data = libsbml.writeSBMLToString(rpsbml_paths[rpsbml_name].document).encode('utf-8')
            data = io.BytesIO(bytes(data))
            zip_file.writestr(rpsbml_name, data.getvalue())
    with open(outZip, 'wb') as f:
        f.write(zip_buffer.getvalue())


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
    parser = argparse.ArgumentParser('Python wrapper to read the output of rp2paths into SBML files including their cofactors')
    parser.add_argument('-rp2paths_compounds', type=str)
    parser.add_argument('-rp2paths_outPaths', type=str)
    parser.add_argument('-rp2paths_scope', type=str)
    #parser.add_argument('-model_compartments', type=str)
    #parser.add_argument('-model_sink', type=str)
    #parser.add_argument('-outSBMLtar', type=str)
    parser.add_argument('-outSBMLzip', type=str)
    params = parser.parse_args()
    #parse the files into the reader
    rpreader = rpFBA.rpReader()
    rpreader.compounds(params.rp2paths_compounds)
    rpreader.transformation(params.rp2paths_scope)
    #rpreader.compartments(params.model_compartments)
    #rpreader.chemicals(params.model_sink)
    rpreader.outPaths(params.rp2paths_outPaths)
    #add the cofactors to the parsed
    rpcofactors = rpFBA.rpCofactors(rpreader)
    rpcofactors.pathsToSBML()
    #package the rpsbml's for the next pathway
    #writerpSBMLtar(rpcofactors.sbml_paths, params.outSBMLtar)
    writerpSBMLzip(rpcofactors.sbml_paths, params.outSBMLzip)
    exit(0)
