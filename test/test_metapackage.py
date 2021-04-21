#!/usr/bin/env python3

#=======================================================================
# Authors: Ben Woodcroft
#
# Unit tests.
#
# Copyright
#
# This is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.	See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License.
# If not, see <http://www.gnu.org/licenses/>.
#=======================================================================

import unittest
import os.path
import sys
from io import StringIO
import tempfile
import extern

path_to_script = os.path.join(os.path.dirname(os.path.realpath(__file__)),'..','bin','singlem')
path_to_data = os.path.join(os.path.dirname(os.path.realpath(__file__)),'data')

sys.path = [os.path.join(os.path.dirname(os.path.realpath(__file__)),'..')]+sys.path
from singlem.metapackage import Metapackage
from singlem.otu_table_collection import OtuTableCollection
from singlem.taxonomy import Taxonomy

class Tests(unittest.TestCase):
    maxDiff = None

    def test_metapackage_create_on_target_fasta(self):
        with tempfile.NamedTemporaryFile(prefix='singlem-chance',mode='w') as f:
            cmd = "{} metapackage --singlem-packages test/data/4.11.22seqs.v3_archaea_targetted.gpkg.spkg/ --output-prefilter-fasta {}".format(
                path_to_script, f.name
            )
            extern.run(cmd)
            with open(f.name) as f2:
                self.assertEqual(
                    '''>650377985
MASQPVFKRTYVRTKPYPEKKVRIVDELKELFSKYETVLIIDIHETSNRVLQEYRFWLRRRGARVIKAKNTLVLIALRQLMNDVSEDIEKLFTGENLLIFTNENPFEIARWIWGTGVRREAMPGDIAPFDLVAPAGNTNMSPGPIMSKFGKLKIPIKVQDGKIWIVKDTVIVKKGDKINEDAAEILKKLSIRPVFETLKIKAVILRGKYVITADELKLDARTYRSMIEDAVKGAFNLAVNTAYPTPEVLRISITKAYMEAMNLAINARYITPETARYILIKAASEAHALASIIAPKAPELGLQVTQQPQQVKTETEQARAEKKTEEKKETIEEEKKEGPSEEDIAAGFSNLFG
>646564583
MSAVARTYPKWKTEQLEDLVELLKKYKVFLIGDLTGVPASHVQRLRKKLAKTAEVRVVKPKLFAIALERVGIDPEAFKDLLTGQNIVFFTNENPFDVALKIHNIVTMDYYKPGEKTDKEIVIPEGNTGIPPGPMLSVFGKLKIQTKVQANVIHVAKDTVVAKPGDVISPELSSILQKLGLALKEIRLRLKAGYDGILIPGESLILNIDQYVEMVKAASLDALKIAVELAVPEPEVLPLVLSKAVRQATALAVEAGYVTPETVELVLKAAETKAQALAYEVSRLAPELGIEVKVVQQPQEAKPKKEEKPAEEEKKEEGVSEEALAEGLSALFG
>640069326
MLAIGKRQYVREKSYPPRKVRIVQEATELLQKYQYVFLFDLHGLSARILGEYRYKLRPYGAVKIIKPTLFKIAYAKVYGGVPVEIAEKVRGEVGFFFTNHNPAEVVKLVAKYAVRRAARPGDKAPFDIVIPAGPTNASPGPIISKFGKLKIPTRVQEGKIWIAKDTVVAKAGQEITPEMAEVLRVVGIEPIFESLRLIGVLWKGKRFVPIEELIIDVKQYRELIEAAATYARNLALNVVYPTREVLQVVIPAAHARALALAVKLGVVTKETLPALLSRAVAEANALAAAVAPKAPELGLSVAVAPQPAAQPQQVEQQPAAGGEAEEKKEGPSEEEIAGSLGALF
''',
                    f2.read()
                )

if __name__ == "__main__":
    unittest.main()