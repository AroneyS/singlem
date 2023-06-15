#!/usr/bin/env python3

import extern
import logging
import argparse
import os

def remove_before(marker, string_to_process):
    splitter = '\n' + marker + '\n'
    if splitter not in string_to_process:
        raise Exception("Marker '{}' not found in string".format(marker))
    return splitter+string_to_process.split(splitter)[1]

if __name__ == '__main__':
    parent_parser = argparse.ArgumentParser(add_help=False)
    # parent_parser.add_argument('--debug', help='output debug information', action="store_true")
    #parent_parser.add_argument('--version', help='output version information and quit',  action='version', version=repeatm.__version__)
    parent_parser.add_argument('--quiet', help='only output errors', action="store_true")

    args = parent_parser.parse_args()

    # Setup logging
    debug = True
    if args.quiet:
        loglevel = logging.ERROR
    else:
        loglevel = logging.DEBUG
    logging.basicConfig(level=loglevel, format='%(asctime)s %(levelname)s: %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

    subdir_and_commands = [
        ['tools', ['data','pipe','appraise','summarise','renew','supplement','read_fraction']],
        ['advanced', ['makedb','query','condense']]
    ]

    for subdir, commands in subdir_and_commands:
        for subcommand in commands:
            cmd_stub = "bin/singlem {} --full-help-roff |pandoc - -t markdown-multiline_tables-simple_tables-grid_tables -f man |sed 's/\\\\\\[/[/g; s/\\\\\\]/]/g; s/^: //'".format(subcommand)
            man_usage = extern.run(cmd_stub)

            subcommand_prelude = 'docs/prelude/{}_prelude.md'.format(subdir, subcommand)
            if os.path.exists(subcommand_prelude):
                # Remove everything before the options section
                splitters = {
                    'pipe': 'COMMON OPTIONS',
                    'read_fraction': 'OPTIONS',
                    'data': 'OPTIONS',
                    'summarise': 'INPUT',
                    'makedb': 'REQUIRED ARGUMENTS',
                    'appraise': 'INPUT OTU TABLE OPTIONS',
                }
                logging.info("For ROFF for command {}, removing everything before '{}'".format(
                    subcommand, splitters[subcommand]))
                man_usage = remove_before(splitters[subcommand], man_usage)

                with open('docs/{}/{}.md'.format(subdir, subcommand),'w') as f:
                    f.write('---\n')
                    f.write('title: SingleM {}\n'.format(subcommand))
                    f.write('---\n')
                    f.write('# singlem {}\n'.format(subcommand))

                    with open(subcommand_prelude) as f2:
                        f.write(f2.read())

                    f.write(man_usage)
            else:
                man_usage = remove_before('DESCRIPTION', man_usage)
                with open('docs/{}/{}.md'.format(subdir, subcommand),'w') as f:
                    f.write('---\n')
                    f.write('title: SingleM {}\n'.format(subcommand))
                    f.write('---\n')
                    f.write('# singlem {}\n'.format(subcommand))

                    f.write(man_usage)

    extern.run("doctave build")