#!/usr/bin/env python3

"""Module containing the Cpptraj Rmsf class and the command line interface."""
import argparse
from biobb_common.configuration import  settings
from biobb_common.tools import file_utils as fu
from biobb_common.command_wrapper import cmd_wrapper
from biobb_analysis.ambertools.common import *


class Rmsf():
    """Wrapper of the Ambertools Cpptraj Rmsf module.
    Cpptraj (the successor to ptraj) is the main program in Ambertools for processing coordinate trajectories and data files.
    The parameter names and defaults are the same as
    the ones in the official Cpptraj manual: https://amber-md.github.io/cpptraj/CPPTRAJ.xhtml

    Args:
        input_top_path (str): Path to the input structure or topology file. Accepted formats: top, pdb, prmtop, parmtop.
        input_traj_path (str): Path to the input trajectory to be processed. Accepted formats: crd, cdf, netcdf, restart, ncrestart, restartnc, dcd, charmm, cor, pdb, mol2, trr, gro, binpos, xtc, cif, arc, sqm, sdf, conflib.
        input_exp_path (str): Path to the experimental reference file (required if reference = experimental).
        output_cpptraj_path (str): Path to the output processed trajectory.
        properties (dic):
            | - **in_parameters** (*dict*) - (None) Parameters for input trajectory. Accepted parameters:
                | - **start** (*int*) - (1) Starting frame for slicing
                | - **end** (*int*) - (-1) Ending frame for slicing
                | - **step** (*int*) - (1) Step for slicing
                | - **mask** (*string*) - ("all-atoms") Mask definition. Values: c-alpha, backbone, all-atoms, heavy-atoms, side-chain, solute, ions, solvent.
                | - **reference** (*string*) - ("first") Reference definition. Values: first, average, experimental.
            | - **cpptraj_path** (*str*) - ("cpptraj") Path to the cpptraj executable binary.
    """

    def __init__(self, input_top_path, input_traj_path,
                 output_cpptraj_path, input_exp_path = None, properties=None, **kwargs):
        properties = properties or {}

        # Input/Output files
        self.input_top_path = check_top_path(input_top_path)
        self.input_traj_path = check_traj_path(input_traj_path)
        self.input_exp_path = input_exp_path
        self.output_cpptraj_path = check_out_path(output_cpptraj_path)

        # Properties specific for BB
        self.instructions_file = get_default_value('instructions_file')
        self.in_parameters = get_parameters(properties, 'in_parameters')
        self.cpptraj_path = get_binary_path(properties, 'cpptraj_path')

        # Properties common in all BB
        self.can_write_console_log = properties.get('can_write_console_log', True)
        self.global_log = properties.get('global_log', None)
        self.prefix = properties.get('prefix', None)
        self.step = properties.get('step', None)
        self.path = properties.get('path', '')

    def create_instructions_file(self):
        """Creates an input file using the properties file settings"""
        instructions_list = []
        self.instructions_file = fu.create_name(prefix=self.prefix, step=self.step, name=self.instructions_file)

        # parm
        instructions_list.append('parm ' + self.input_top_path)

        # trajin
        in_params = get_in_parameters(self.in_parameters, self)
        instructions_list.append('trajin ' + self.input_traj_path + ' ' + in_params)

        # Set up
        instructions_list += setup_structure(self)

        # mask
        mask = self.in_parameters.get('mask', '')
        ref_mask = ''
        if mask:
            strip_mask = get_negative_mask(mask, self)
            ref_mask = get_mask(mask, self)
            instructions_list.append('strip ' + strip_mask)

        # reference
        reference = self.in_parameters.get('reference', '')
        instructions_list += get_reference(reference, self, ref_mask, False)
        instructions_list.append('atomicfluct out ' + self.output_cpptraj_path + ' byres')

        # create .in file
        with open(self.instructions_file, 'w') as mdp:
            for line in instructions_list:
                mdp.write(line.strip() + '\n')

        return self.instructions_file

    def launch(self):
        """Launches the execution of the Ambertools cpptraj module."""
        out_log, err_log = fu.get_logs(path=self.path, prefix=self.prefix, step=self.step, can_write_console=self.can_write_console_log)

        # create instructions file
        self.create_instructions_file() 

        # run command line
        cmd = [self.cpptraj_path, '-i', self.instructions_file]

        returncode = cmd_wrapper.CmdWrapper(cmd, out_log, err_log, self.global_log).launch()
        tmp_files = [self.instructions_file, 'MyAvg']
        removed_files = [f for f in tmp_files if fu.rm(f)]
        fu.log('Removed: %s' % str(removed_files), out_log, self.global_log)
        return returncode

def main():
    parser = argparse.ArgumentParser(description="Wrapper for the Ambertools cpptraj module.")
    parser.add_argument('--config', required=True, help='Configuration file')
    parser.add_argument('--system', required=False)
    parser.add_argument('--step', required=False)

    # Specific args of each building block
    parser.add_argument('--input_top_path', required=True, help='Path to the input Amber structure or topology file.')
    parser.add_argument('--input_traj_path', required=True, help='Path to the input Amber trajectory to be processed.')
    parser.add_argument('--input_exp_path', required=False, help='Path to the experimental reference file (required if reference = experimental).')
    parser.add_argument('--output_cpptraj_path', required=True, help='Path to the output processed Amber trajectory or to the output dat file containing the analysis results.')

    args = parser.parse_args()
    check_conf(args.config)
    args.config = args.config or "{}"
    properties = settings.ConfReader(config=args.config, system=args.system).get_prop_dic()
    if args.step:
        properties = properties[args.step]

    # Specific call of each building block
    Rmsf(input_top_path=args.input_top_path, input_traj_path=args.input_traj_path, output_cpptraj_path=args.output_cpptraj_path, input_exp_path=args.input_exp_path, properties=properties).launch()

if __name__ == '__main__':
    main()