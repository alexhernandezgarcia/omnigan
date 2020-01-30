import sys
import os
from pathlib import Path
import uuid
import addict

from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.resolve()))

from run import print_header

from omnigan.utils import (
    domains_to_class_tensor,
    env_to_path,
    get_increased_path,
    load_opts,
    flatten_opts,
)
from omnigan.data import get_all_loaders

if __name__ == "__main__":

    print_header("test_domains_to_class_tensor")
    root = Path(__file__).parent.parent
    opts = load_opts(root / "config/local_tests.yaml", default=root / "shared/defaults.yml")
    opts.data.loaders.batch_size = 2
    opts.data.loaders.num_workers = 2
    opts.data.loaders.shuffle = True
    loaders = get_all_loaders(opts)
    batch = next(iter(loaders["train"]["rn"]))
    print(domains_to_class_tensor(batch["domain"], True))
    print(domains_to_class_tensor(batch["domain"], False))
    domains = ["rn", "rf", "rf", "sn"]

    try:
        domains_to_class_tensor([1, "sg"])
        raise TypeError("Should raise a ValueError")
    except ValueError:
        print("ok.")

    print_header("test_env_to_path")
    assert env_to_path("$HOME") == os.environ["HOME"]
    assert env_to_path("$HOME/") == os.environ["HOME"] + "/"
    assert env_to_path("$HOME/Documents") == str(Path(os.environ["HOME"]) / "Documents")
    print("ok.")

    print_header("test_get_increased_path")
    uid = str(uuid.uuid4())
    p = Path() / uid
    p.mkdir()
    get_increased_path(p).mkdir()
    get_increased_path(p).mkdir()
    get_increased_path(p).mkdir()
    paths = {str(d) for d in Path().glob(uid + "*")}
    target = {str(p), str(p) + " (1)", str(p) + " (2)", str(p) + " (3)"}
    assert paths == target
    print("ok.")
    for d in Path().glob(uid + "*"):
        d.rmdir()

    print_header("test_flatten_opts")
    d = addict.Dict()
    d.a.b.c = 2
    d.a.b.d = 3
    d.a.e = 4
    d.f = 5
    assert flatten_opts(d) == {
        "a.b.c": 2,
        "a.b.d": 3,
        "a.e": 4,
        "f": 5,
    }
    print("ok.")
