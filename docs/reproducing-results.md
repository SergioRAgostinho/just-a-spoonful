# Reproducing Results

Before going through this document, ensure you've read and made all preparations described in the [Model Release section of README.md](../README.md#model-release) (as well as its subsections). By the end of it you should have the DCP and RPM-Net projects somewhere in your computer and the environmental variable `SPOONFUL_PREFIX` defined. For convenience, we consider defined an additional environmental variable with DCP's and RPM-Net's project folder
```shell
export SPOONFUL_PREFIX="<path to just-a-spoonful's parent folder>/just-a-spoonful"
export DCP_PREFIX="<path to dcp's parent folder>/dcp"
export RPM_PREFIX="<path to rpmnet's parent folder>/RPMNet"
```

Results that can generated with the original repositories from DCP and RPM-Net will have the tag `[original]` in the title.

# DCP

The following results can be generated with the original DCP repository. The metrics you're looking for appear as `rot_RMSE`, `rot_MAE`, `trans_RMSE` and `trans_MAE` of the `A--------->B` output section. All follow-up commands assume your current working directory is DCP project folder.
```shell
cd "$DCP_PREFIX"
```

## Table 1 - DCP on ModelNet40 with Gaussian noise added to the source point cloud

1. DCP vanilla
    ```shell
    python main.py --exp_name=dcp_v2 --model=dcp --emb_nn=dgcnn --pointer=transformer --head=svd --eval --gaussian_spoonful True --model_path="$SPOONFUL_PREFIX/share/weights/dcp/vanilla.t7"
    ```
2. Ours
    ```shell
    python main.py --exp_name=dcp_v2 --model=dcp --emb_nn=dgcnn --pointer=transformer --head=svd --eval --gaussian_spoonful True --model_path="$SPOONFUL_PREFIX/share/weights/dcp/ours.t7"
    ```

## Table 2 - DCP on ModelNet40 with unseen categories [original]

1. DCP vanilla - no available model. The model provided by the project was trained with access to all categories of objects. I just copied the results from DCP's paper.
2. Ours
    ```shell
    python main.py --exp_name=dcp_v2 --model=dcp --emb_nn=dgcnn --pointer=transformer --head=svd --eval --unseen True --model_path="$SPOONFUL_PREFIX/share/weights/dcp/ours-unseen.t7"
    ```

## Table 4 - Initialization experiment with DCP on ModelNet40 with unseen categories

Note: In the following commands I make use of the wildcard symbol * used to expand the paths to all models under `share/weights/init-unseen/vanilla/` and `share/weights/init-unseen/ours/`. Because of it, I no longer escape the path between quotes when specifying the model paths.

1. DCP vanilla
    ```shell
    python eval_initialization.py --exp_name=dcp_v2 --model=dcp --emb_nn=dgcnn --pointer=transformer --head=svd --eval --unseen True --init_model_list $SPOONFUL_PREFIX/share/weights/dcp/init-unseen/vanilla/*
    ```
2. Ours
    ```shell
    python eval_initialization.py --exp_name=dcp_v2 --model=dcp --emb_nn=dgcnn --pointer=transformer --head=svd --eval --unseen True --init_model_list $SPOONFUL_PREFIX/share/weights/dcp/init-unseen/ours/*
    ```

## Table 1 (Supplementary) - DCP on ModelNet40 [original]

1. DCP vanilla
    ```shell
    python main.py --exp_name=dcp_v2 --model=dcp --emb_nn=dgcnn --pointer=transformer --head=svd --eval --model_path="$SPOONFUL_PREFIX/share/weights/dcp/vanilla.t7"
    ```

2. Ours
    ```shell
    python main.py --exp_name=dcp_v2 --model=dcp --emb_nn=dgcnn --pointer=transformer --head=svd --eval --model_path="$SPOONFUL_PREFIX/share/weights/dcp/ours.t7"
    ```


# RPM-Net

The following results can be generated with the original RPM-Net repository. The metrics you're looking for appear as `DeepCP metrics: rot-mae, trans-mae`, `Rotation error (deg, mean)`, `Translation error (mean)` and `Chamfer error (mean-sq)`, for the final iteration (5th - `Evaluation result (iter 4)`) of the iterative registration procedure.
All follow-up commands assume your current working directory is
```shell
cd "$RPM_PREFIX/src"
```

## Table 3 - RPM-Net on ModelNet40 with partial visible data with noise [original]

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

## Table 2 (Supplementary) - RPM-Net on ModelNet40 with independent Gaussian noise [original]

1. RPM vanilla - provided by the authors [here](https://drive.google.com/uc?id=1cvgpWG93Tb2z_xH8JTXYtKlIzXe_o5ri)
    ```shell
    python eval.py --noise_type jitter --resume "$SPOONFUL_PREFIX/share/weights/rpm-net/vanilla-jitter.pth"
    ```
2. Ours. You'll notice the mean isotropic error is actually lower than what we reported in the table. Probably a copy-paste error.
    ```shell
    python eval.py --noise_type jitter --resume "$SPOONFUL_PREFIX/share/weights/rpm-net/ours-jitter.pth"
    ```
