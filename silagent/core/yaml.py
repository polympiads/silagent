from yaml import load, dump
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper
def load_yaml (text: str):
    return load(text, Loader)
def dump_yaml (yaml):
    return dump(yaml, Dumper = Dumper)