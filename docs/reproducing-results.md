# Reproducing Results

Before going through this document, ensure you've read and made all preparations described in the [Model Release section of README.md](../README.md#model-release) (as well as its subsections). By the end of it you should have the DCP and RPM-Net projects somewhere in your computer and the environmental variable `SPOONFUL_PREFIX` defined. For convenience, we consider defined an additional environmental variable with DCP's and RPM-Net's project folder
```shell
export DCP_PREFIX="<path to dcp's parent folder>/dcp"
export RPM_PREFIX="<path to rpmnet's parent folder>/RPMNet"
```

# DCP

The following results can be generated with the original DCP repository. The metrics you're looking for appear as `rot_RMSE`, `rot_MAE`, `trans_RMSE` and `trans_MAE` of the `A--------->B` output section. All follow-up commands assume your current working directory is DCP project folder.
```shell
cd "$DCP_PREFIX"
```

## Table 2 - DCP on ModelNet40 with unseen categories

1. DCP vanilla - no available model. The model provided by the project was trained with access to all categories of objects. I just copied the results from DCP's paper.
2. Ours
    ```shell
    $ python main.py --exp_name=dcp_v2 --model=dcp --emb_nn=dgcnn --pointer=transformer --head=svd --eval --unseen True --model_path="$SPOONFUL_PREFIX/share/weights/dcp/ours-unseen.t7"
    ```

## Table 1 (Supplementary) - DCP on ModelNet40

1. DCP
    ```shell
    $ python main.py --exp_name=dcp_v2 --model=dcp --emb_nn=dgcnn --pointer=transformer --head=svd --eval --model_path="$SPOONFUL_PREFIX/share/weights/dcp/vanilla.t7"
    ```

2. Ours
    ```shell
    $ python main.py --exp_name=dcp_v2 --model=dcp --emb_nn=dgcnn --pointer=transformer --head=svd --eval --model_path="$SPOONFUL_PREFIX/share/weights/dcp/ours.t7"
    ```

# RPM-Net

The following results can be generated with the original RPM-Net repository. The metrics you're looking for appear as `DeepCP metrics: rot-mae, trans-mae`, `Rotation error (deg, mean)`, `Translation error (mean)` and `Chamfer error (mean-sq)`, for the final iteration (5th - `Evaluation result (iter 4)`) of the iterative registration procedure.
All follow-up commands assume your current working directory is
```shell
cd "$RPM_PREFIX/src"
```

## Table 3 - RPM-Net on ModelNet40 with partial visible data with noise

1. RPM vanilla - provided by the authors [here](https://drive.google.com/drive/folders/1CqbcyJ8cwIqTeuv6kRWsnUoYUY46ewb9)
    ```shell
    python eval.py --noise_type crop --resume "$SPOONFUL_PREFIX/share/weights/rpm-net/vanilla-crop.pth"
    ```
2. Ours
    ```shell
    python eval.py --noise_type crop --resume "$SPOONFUL_PREFIX/share/weights/rpm-net/ours-crop.pth"
    ```
3. RPM vanilla trained without the inlier loss
    ```shell
    python eval.py --noise_type crop --resume "$SPOONFUL_PREFIX/share/weights/rpm-net/vanilla-no-inlier-loss-crop.pth"
    ```
4. Ours trained without the inlier loss
    ```shell
    python eval.py --noise_type crop --resume "$SPOONFUL_PREFIX/share/weights/rpm-net/ours-no-inlier-loss-crop.pth"
    ```
