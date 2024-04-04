from src._lnlpcli import LNLPCLI
import os

def test_sequence():
    sequence = '1,11,21,31,41,9'

    cli = LNLPCLI(save_dir='output', global_data_path='tests/test_data/usa-vaccine-comments.csv', num_samples=500, sequence=sequence)

    cli.run()

    assert os.path.exists('output')
    assert os.path.exists('output/topics')
    assert os.path.exists('output/topics/0_sample_zipf.csv')
    assert os.path.exists('output/document_viz.html')
    assert os.path.exists('output/topic_viz.html')
    assert os.path.exists('output/topic_size_distribution.png')

    
