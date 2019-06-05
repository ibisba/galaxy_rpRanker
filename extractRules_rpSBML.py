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
def extractRules(rpsbml_paths):
    #loop through all the rp_pathway reaction members and return the rules
    allRules = {}
    for rpsbml_name in rpsbml_paths:
        allRules = {**allRules, **rpsbml_paths[rpsbml_name].readRPrules()}
    return allRules

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
    parser = argparse.ArgumentParser('Given an SBML model and the generated SBML heterologous pathway by RetroPath2.0, merge the two')
    parser.add_argument('-inSBMLzip', type=str) 
    parser.add_argument('-outRPrules', type=str) 
    params = parser.parse_args()
    #sbml read the different mode
    allRules = readrpSBMLzip(readrpSBMLzip(params.inSBMLzip))
    


    merged_rpsbml = {}
    for rpsbml_name in rpsbml_paths:
        #read the input sbml model 
        input_rpsbml = rpFBA.rpSBML('inputMergeModel')
        input_rpsbml.readSBML(params.inModel) 
        #merge the heterologous pathway to it
        #TODO: reverse the merge such that the target SBML is merged into the rpsbml object and not vice-versa
        rpsbml_paths[rpsbml_name].mergeModels(input_rpsbml.model)
        merged_rpsbml[rpsbml_name] = input_rpsbml
    writerpSBMLzip(merged_rpsbml, params.outSBMLzip)
    exit(0)
