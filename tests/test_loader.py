from pipeline.loader import load_data


def test_load_data():
    source_a, source_b, source_c, dictionary = load_data()

    assert len(source_a) == 26004
    assert len(source_b) == 53891
    assert len(source_c) == 24186
    assert len(dictionary) == 40