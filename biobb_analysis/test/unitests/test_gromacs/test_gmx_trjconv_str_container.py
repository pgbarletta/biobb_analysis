from biobb_common.tools import test_fixtures as fx
from biobb_analysis.gromacs.gmx_trjconv_str import GMXTrjConvStr


class TestGMXTrjConvStrDocker():
    def setUp(self):
        fx.test_setup(self,'gmx_trjconv_str_docker')

    def tearDown(self):
        fx.test_teardown(self)
        pass

    def test_trjconv_str_docker(self):
        GMXTrjConvStr(properties=self.properties, **self.paths).launch()
        assert fx.not_empty(self.paths['output_str_path'])
        assert fx.equal(self.paths['output_str_path'], self.paths['ref_output_str_path'])

class TestGMXTrjConvStrSingularity():
    def setUp(self):
        fx.test_setup(self,'gmx_trjconv_str_singularity')

    def tearDown(self):
        fx.test_teardown(self)
        pass

    def test_trjconv_str_singularity(self):
        GMXTrjConvStr(properties=self.properties, **self.paths).launch()
        assert fx.not_empty(self.paths['output_str_path'])
        assert fx.equal(self.paths['output_str_path'], self.paths['ref_output_str_path'])