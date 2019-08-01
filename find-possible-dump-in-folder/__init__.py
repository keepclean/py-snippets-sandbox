import argparse
import hashlib
import json
import os


def sha256_checksum(filename, block_size=65536):
    sha256 = hashlib.sha256()
    with open(filename, "rb") as f:
        for block in iter(lambda: f.read(block_size), b""):
            sha256.update(block)

    return sha256.hexdigest()


def main(path):
    possible_dup_files = {}
    dup_files = {}

    for top, _, files in os.walk(path):
        for f in files:
            fpath = os.path.join(top, f)
            fsize = os.path.getsize(fpath)
            possible_dup_files.setdefault(fsize, []).append(fpath)

    for k, v in possible_dup_files.items():
        if len(v) == 1:
            continue

        for i in v:
            if i.endswith((".pdf", ".djvu")):
                dup_files.setdefault(k, {}).update({i: sha256_checksum(i)})

    if not dup_files:
        return

    with open("dup_files.json", "wb") as ofile:
        ofile.write(json.dumps(dup_files, indent=2, sort_keys=True).encode("utf-8"))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("path", default=".", help="path to folder with files")
    args = parser.parse_args()

    main(args.path)
