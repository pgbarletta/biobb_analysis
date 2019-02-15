from biobb_common.tools import test_fixtures as fx
from biobb_analysis.ambertools.cpptraj_rmsf import Rmsf


class TestCpptrajRmsfFirst():
    def setUp(self):
        fx.test_setup(self,'cpptraj_rmsf_first')

    def tearDown(self):
        fx.test_teardown(self)
        pass

    def test_rmsf_first(self):
        Rmsf(properties=self.properties, **self.paths).launch()
        assert fx.not_empty(self.paths['output_cpptraj_path'])
        assert fx.equal(self.paths['output_cpptraj_path'], self.paths['ref_output_cpptraj_path'])

class TestCpptrajRmsfAverage():
    def setUp(self):
        fx.test_setup(self,'cpptraj_rmsf_average')

    def tearDown(self):
        fx.test_teardown(self)
        pass

    def test_rmsf_average(self):
        Rmsf(properties=self.properties, **self.paths).launch()
        assert fx.not_empty(self.paths['output_cpptraj_path'])
        assert fx.equal(self.paths['output_cpptraj_path'], self.paths['ref_output_cpptraj_path'])

class TestCpptrajRmsfExperimental():
    def setUp(self):
        fx.test_setup(self,'cpptraj_rmsf_experimental')

    def tearDown(self):
        fx.test_teardown(self)
        pass

    def test_rmsf_experimental(self):
        Rmsf(properties=self.properties, **self.paths).launch()
        assert fx.not_empty(self.paths['output_cpptraj_path'])
        assert fx.equal(self.paths['output_cpptraj_path'], self.paths['ref_output_cpptraj_path'])

