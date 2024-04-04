from _lnlpcli import LNLPCLI

def test_sequence():
    sequence = '1,11,21,31,41'

    cli = LNLPCLI(save_dir='output', global_data_path='tests/test_data/usa-vaccine-comments.csv', num_samples=500, sequence=sequence)

    cli._process_sequence(sequence)

    data = cli.global_session.logs['data']

    keys = [list(d.keys())[0] for d in data]
    values = [list(d.values())[0] for d in data]

    assert "Embeddings" in keys
    assert "Dimensionality Reduction" in keys
    assert "Clustering" in keys
    assert "Fine Tuning" in keys

    assert "all-MiniLM-L6-v2" in values
    assert "UMAP" in values
    assert "hdbscan" in values
    assert "Enable 2-grams" in values
    
    