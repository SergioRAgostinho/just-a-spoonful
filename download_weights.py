from argparse import ArgumentParser
import os
import shutil
import subprocess
from tempfile import TemporaryDirectory
from warnings import warn

import gdown

URLS = dict(
    dcp=["https://github.com/WangYueFt/dcp/raw/master/pretrained/dcp_v2.t7"],
    ours=[
        "http://web.tecnico.ulisboa.pt/sergio.agostinho/share/just-a-spoonful/weights.zip"
    ],
    rpm_net=[
        "https://drive.google.com/uc?id=1NukECCiaklakqNgqsX8jb_Fueh9_UaK-",
        "https://drive.google.com/uc?id=1cvgpWG93Tb2z_xH8JTXYtKlIzXe_o5ri",
    ],
)

REQUIRED_FILES = dict(
    dcp=[os.path.join("dcp", "vanilla.t7")],
    ours=[
        os.path.join("dcp", "ours.t7"),
        os.path.join("dcp", "ours-unseen.t7"),
        os.path.join("dcp", "init-unseen", "ours", "0.t7"),
        os.path.join("dcp", "init-unseen", "ours", "1.t7"),
        os.path.join("dcp", "init-unseen", "ours", "2.t7"),
        os.path.join("dcp", "init-unseen", "ours", "3.t7"),
        os.path.join("dcp", "init-unseen", "ours", "4.t7"),
        os.path.join("dcp", "init-unseen", "ours", "5.t7"),
        os.path.join("dcp", "init-unseen", "ours", "6.t7"),
        os.path.join("dcp", "init-unseen", "ours", "7.t7"),
        os.path.join("dcp", "init-unseen", "ours", "8.t7"),
        os.path.join("dcp", "init-unseen", "ours", "9.t7"),
        os.path.join("dcp", "init-unseen", "ours", "10.t7"),
        os.path.join("dcp", "init-unseen", "ours", "11.t7"),
        os.path.join("dcp", "init-unseen", "ours", "12.t7"),
        os.path.join("dcp", "init-unseen", "ours", "13.t7"),
        os.path.join("dcp", "init-unseen", "ours", "14.t7"),
        os.path.join("dcp", "init-unseen", "ours", "15.t7"),
        os.path.join("dcp", "init-unseen", "ours", "16.t7"),
        os.path.join("dcp", "init-unseen", "ours", "17.t7"),
        os.path.join("dcp", "init-unseen", "ours", "18.t7"),
        os.path.join("dcp", "init-unseen", "ours", "19.t7"),
        os.path.join("dcp", "init-unseen", "ours", "20.t7"),
        os.path.join("dcp", "init-unseen", "ours", "21.t7"),
        os.path.join("dcp", "init-unseen", "ours", "22.t7"),
        os.path.join("dcp", "init-unseen", "ours", "23.t7"),
        os.path.join("dcp", "init-unseen", "ours", "24.t7"),
        os.path.join("dcp", "init-unseen", "ours", "25.t7"),
        os.path.join("dcp", "init-unseen", "vanilla", "0.t7"),
        os.path.join("dcp", "init-unseen", "vanilla", "1.t7"),
        os.path.join("dcp", "init-unseen", "vanilla", "2.t7"),
        os.path.join("dcp", "init-unseen", "vanilla", "3.t7"),
        os.path.join("dcp", "init-unseen", "vanilla", "4.t7"),
        os.path.join("dcp", "init-unseen", "vanilla", "5.t7"),
        os.path.join("dcp", "init-unseen", "vanilla", "6.t7"),
        os.path.join("dcp", "init-unseen", "vanilla", "7.t7"),
        os.path.join("dcp", "init-unseen", "vanilla", "8.t7"),
        os.path.join("dcp", "init-unseen", "vanilla", "9.t7"),
        os.path.join("dcp", "init-unseen", "vanilla", "10.t7"),
        os.path.join("dcp", "init-unseen", "vanilla", "11.t7"),
        os.path.join("dcp", "init-unseen", "vanilla", "12.t7"),
        os.path.join("dcp", "init-unseen", "vanilla", "13.t7"),
        os.path.join("dcp", "init-unseen", "vanilla", "14.t7"),
        os.path.join("dcp", "init-unseen", "vanilla", "15.t7"),
        os.path.join("dcp", "init-unseen", "vanilla", "16.t7"),
        os.path.join("dcp", "init-unseen", "vanilla", "17.t7"),
        os.path.join("dcp", "init-unseen", "vanilla", "18.t7"),
        os.path.join("dcp", "init-unseen", "vanilla", "19.t7"),
        os.path.join("dcp", "init-unseen", "vanilla", "20.t7"),
        os.path.join("dcp", "init-unseen", "vanilla", "21.t7"),
        os.path.join("dcp", "init-unseen", "vanilla", "22.t7"),
        os.path.join("dcp", "init-unseen", "vanilla", "23.t7"),
        os.path.join("dcp", "init-unseen", "vanilla", "24.t7"),
        os.path.join("dcp", "init-unseen", "vanilla", "25.t7"),
        os.path.join("rpm-net", "ours-crop.pth"),
        os.path.join("rpm-net", "ours-no-inlier-loss-crop.pth"),
        os.path.join("rpm-net", "vanilla-no-inlier-loss-crop.pth"),
    ],
    rpm_net=[
        os.path.join("rpm-net", "vanilla-crop.pth"),
        os.path.join("rpm-net", "vanilla-jitter.pth"),
    ],
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


def download_file_wget(url, dest_dir):
    try:
        subprocess.run(["wget", url], cwd=dest_dir, check=True)
    except subprocess.CalledProcessError:
        msg = f"Could not download file package with url {url}"
        raise RuntimeError(msg)


def download_file_gdrive(url, dest_dir):
    cwd = os.getcwd()
    os.chdir(dest_dir)
    gdown.download(url)
    os.chdir(cwd)


def download_weights(prefix, download_dir=None, force=False):
    keys = download_keys(prefix, force=force)
    if len(keys):
        print(f"Dowloading files for keys: {' '.join(keys)}")
    else:
        print(f"Downloading files:\nAll files present. Nothing to download")

    f = dict(
        dcp=download_file_wget, ours=download_file_wget, rpm_net=download_file_gdrive
    )

    for k in keys:
        for url in URLS[k]:
            f[k](url, dest_dir=download_dir)
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


def relocate_rpm_net(prefix, download_dir):
    dest_dir = os.path.join(prefix, "share", "weights", "rpm-net")
    os.makedirs(dest_dir, exist_ok=True)
    shutil.move(
        os.path.join(download_dir, "partial-trained.pth"),
        os.path.join(dest_dir, "vanilla-crop.pth"),
    )
    shutil.move(
        os.path.join(download_dir, "noisy-trained.pth"),
        os.path.join(dest_dir, "vanilla-jitter.pth"),
    )


def relocate_weights(file_keys, prefix, download_dir):
    f = dict(dcp=relocate_dcp, ours=relocate_ours, rpm_net=relocate_rpm_net)
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
