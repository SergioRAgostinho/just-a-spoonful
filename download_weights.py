from argparse import ArgumentParser
import os
import shutil
import subprocess
from tempfile import TemporaryDirectory
from warnings import warn

URLS = dict(
    dcp="https://github.com/WangYueFt/dcp/raw/master/pretrained/dcp_v2.t7",
    ours="http://web.tecnico.ulisboa.pt/sergio.agostinho/share/just-a-spoonful/weights.zip",
)

REQUIRED_FILES = dict(
    dcp=[os.path.join("dcp", "vanilla.t7")],
    ours=[os.path.join("dcp", "ours.t7"), os.path.join("dcp", "ours-unseen.t7")],
)


def download_keys(prefix, force=False):
    if force:
        return list(REQUIRED_FILES.keys())

    missing_files = []
    for k, files in REQUIRED_FILES.items():
        complete = True
        for file in files:
            if not os.path.exists(os.path.join(prefix, "share", "weights", file)):
                complete = False
        if not complete:
            missing_files.append(k)
    return missing_files


def download_file(url, prefix=None):
    subprocess.run(["wget", str(url)], cwd=prefix)
    raise NotImplementedError


def download_weights(prefix, download_dir=None, force=False):
    keys = download_keys(prefix, force=force)
    if len(keys):
        print(f"Dowloading files for keys: {' '.join(keys)}")
    else:
        print(f"Downloading files:\nAll files present. Nothing to download")

    for k in keys:
        try:
            subprocess.run(["wget", URLS[k]], cwd=download_dir, check=True)
        except subprocess.CalledProcessError:
            msg = f"Could not download file package '{k}' with url {URLS[k]}"
            raise RuntimeError(msg)
    return keys


def relocate_dcp(prefix, download_dir):
    # create folder
    dest_dir = os.path.join(prefix, "share", "weights", "dcp")
    os.makedirs(dest_dir, exist_ok=True)
    shutil.move(
        os.path.join(download_dir, "dcp_v2.t7"), os.path.join(dest_dir, "vanilla.t7")
    )


def relocate_ours(prefix, download_dir):
    dest_dir = os.path.join(prefix, "share", "weights")
    try:
        subprocess.run(
            ["unzip", "-o", os.path.join(download_dir, "weights.zip")],
            cwd=dest_dir,
            check=True,
        )
    except subprocess.CalledProcessError:
        msg = "Failed to extract weights"
        raise RuntimeError(msg)


def relocate_weights(file_keys, prefix, download_dir):
    f = dict(dcp=relocate_dcp, ours=relocate_ours)
    for k in file_keys:
        f[k](prefix, download_dir)


def find_project_prefix():
    return os.path.dirname(os.path.realpath(__file__))


def checksum(prefix):
    print("Checksumming weights:")
    weights_dir = os.path.join(prefix, "share", "weights")
    try:
        subprocess.run(
            ["sha1sum", "-c", os.path.join(weights_dir, "weights.sha1sum")],
            cwd=weights_dir,
            check=True,
        )
    except subprocess.CalledProcessError:
        msg = "Checksums not validate"
        raise warn(msg)


def main():
    parser = ArgumentParser(description="Helper script to download weights")
    parser.add_argument(
        "--force", action="store_true", help="Force redownload and extraction"
    )
    args = parser.parse_args()

    # find prefix for the project
    prefix = find_project_prefix()

    # Create a temporary folder for performing operation if needed
    with TemporaryDirectory(dir=prefix) as tmp_dir:

        # download files
        missing_files = download_weights(prefix, tmp_dir, force=args.force)

        # extract and relocate weights
        relocate_weights(missing_files, prefix, tmp_dir)

    # validate
    checksum(prefix)


if __name__ == "__main__":
    main()
