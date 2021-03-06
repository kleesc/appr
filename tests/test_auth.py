import os.path

import yaml

from appr.auth import ApprAuth


def test_fake_home(fake_home):
    assert os.path.expanduser("~") == fake_home


def test_init_create_dir(fake_home):
    ApprAuth(".appr")
    assert os.path.exists(os.path.join(str(fake_home), ".appr"))


def test_init_token_empty(fake_home):
    k = ApprAuth()
    assert os.path.exists(k.tokenfile) is False


def test_get_empty_token(fake_home):
    k = ApprAuth()
    assert k.token('*') is None
    assert k.tokens is None


def test_delete_empty_token(fake_home):
    """ Should not fail if there is no token """
    k = ApprAuth()
    assert k.delete_token('*') is None


def test_delete_token(fake_home):
    """ Should not fail if there is no token """
    k = ApprAuth()
    k.add_token('*', "titid")
    assert k.token('*') == "titid"
    assert k.delete_token('*') == {'scope': {'namespace': '*', 'repo': '*'}, 'token': 'titid'}
    assert k.token('*') is None

def test_create_token_value(fake_home):
    """ Should not fail if there is no token """
    k = ApprAuth()
    k.add_token('a', "titic")
    k.add_token('b', "titib")
    assert k.token('a') == "titic"
    assert k.token('a') == "titic"
    assert k.token('c') is None


def test_create_token_file(fake_home):
    k = ApprAuth()
    k.add_token('a', "titib")
    assert os.path.exists(k.tokenfile) is True
    f = open(k.tokenfile, 'r')
    r = f.read()
    assert {'auths': {'a': {'scope': {'namespace': '*', 'repo': '*'}, 'token': 'titib'}}} == yaml.load(r)



def test_create_delete_get_token(fake_home):
    k = ApprAuth()
    k.add_token('a', "titia")
    assert k.token('a') == "titia"
    k.delete_token('a')
    assert k.token('a') is None


def test_get_token_from_file(fake_home):
    k = ApprAuth()
    f = open(k.tokenfile, 'w')
    r = yaml.dump({'auths': {'a': {'scope': {'namespace': '*', 'repo': '*'}, 'token': 'titib'}}})
    f.write(r)
    f.close()
    k = ApprAuth()
    assert k.token('a') == "titib"


def test_retro_compat(fake_home):
    k = ApprAuth()
    f = open(k.tokenfile, 'w')
    r = yaml.dump({'auths': {'a': 'foo', 'b': 'bar'}})
    f.write(r)
    f.close()
    k = ApprAuth()
    f = open(k.tokenfile, 'r')
    new_format = f.read()
    f.close()
    expected = {'auths': {'a': {'scope': {'namespace': '*', 'repo': '*'}, 'token': 'foo'},
                          'b': {'scope': {'namespace': '*', 'repo': '*'}, 'token': 'bar'}}}
    assert yaml.load(new_format) == expected
    assert k.tokens == expected
