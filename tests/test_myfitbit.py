
def test_import():
    import myfitbit
    print(myfitbit)
    assert myfitbit.__version__ == '0.7.0'
    assert myfitbit.FitbitClient
