import sys
import torch
import os
from pathlib import Path
import uuid

sys.path.append("..")

from run import print_header

from omnigan.utils import (
    domains_to_class_tensor,
    env_to_path,
    get_increased_path,
    load_opts,
    transforms_string,
)
from omnigan.data import OmniListDataset, get_all_loaders

if __name__ == "__main__":
    print_header("test_domains_to_class_tensor")

    opts = load_opts("../shared/defaults.yml")
    opts.data.loaders.batch_size = 2
    opts.data.loaders.num_workers = 2
    opts.data.loaders.shuffle = True
    loaders = get_all_loaders(opts)
    batch = next(iter(loaders["train"]["rn"]))
    print(domains_to_class_tensor(batch["domain"]))
    domains = ["rn", "rf", "rf", "sn"]
    target = torch.Tensor([1, 0, 0, 3])
    assert all(domains_to_class_tensor(domains) == target)
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
