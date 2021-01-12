import re
import os
import alpha_quant.common.utils.notebook_utils as nbu
import alpha_quant.common.unittest as ut
from alpha_quant.static import get_project_root


class TestNotebookUtils(ut.TestCase):
    def test_execute_notebook(self):
        project_root = get_project_root()
        nb_input_file = os.path.join(project_root, 'notebook', 'data', 'pandas_datareader.ipynb')
        benchmark_file = self.get_benchmark_file(basename='pandas_datareader.SPY.20200101-20201231.html')

        target = nbu.execute_notebook(nb_input_file=nb_input_file, nb_output_file=None,
                                      param_dict={'ticker': 'SPY', 'start': '2020-01-01', 'end': '2020-12-31'},
                                      title='pandas_datareader',
                                      export_html=True)
        target = re.sub(r'id=".+"', 'id=""', target)
        target = re.sub(r"getElementById\('.+'\)", "Id('')", target)

        with open(benchmark_file, 'r') as fh:
            benchmark = fh.read()#nbu.read_notebook(nb_input_file=benchmark_file)
            benchmark = re.sub(r'id=".+"', 'id=""', benchmark)
            benchmark = re.sub(r"getElementById\('.+'\)", "Id('')", benchmark)
        #

        # print(benchmark)
        self.assertEqual(benchmark, target)
    #
#


if __name__ == '__main__':
    ut.main()
#
