#!/usr/bin/env python3

import argparse
import sys

sys.path.insert(0, '/home/src/')
import rpFBA

if __name__ == "__main__":
    parser = argparse.ArgumentParser('Generate the sink from a model SBML by specifying the compartment')
    parser.add_argument('-inSBML', type=str)
    parser.add_argument('-outSink', type=str)
    parser.add_argument('-compartmentId', type=str, default='MNXC3')
    params = parser.parse_args()
    rpsbml = rpFBA.rpSBML('tmp')
    rpsbml.readSBML(params.inSBML)
    rpreader = rpFBA.rpReader()
    rpreader.genSink(rpsbml, params.outSink, params.compartmentId)
    exit(0)
