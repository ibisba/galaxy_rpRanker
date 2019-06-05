#!/usr/bin/env python3

import libsbml
import argparse
import sys #exit using sys exit if any error is encountered
import os

import zipfile
import io

sys.path.insert(0, '/home/src/')
import rpFBA


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


##
#
#
if __name__ == "__main__":
    parser = argparse.ArgumentParser('Calculate the FBA for the reactions')
    parser.add_argument('-inSBMLzip', type=str)
    parser.add_argument('-outSBMLzip', type=str) 
    reader = rpFBA.rpReader()
    params = parser.parse_args()
    rpsbml_paths = readrpSBMLzip(params.inSBMLzip)
    for rpsbml_name in rpsbml_paths:
        rpfba = rpFBA.rpFBA(rpsbml_paths[rpsbml_name])
        rpfba.allObj()
    writerpSBMLzip(rpsbml_paths, params.outSBMLzip)
    exit(0)
