# Reproducing Results

Before going through this document, ensure you've read and made all preparations described in the [Model Release section of README.md](../README.md#model-release) (as well as its subsections). By the end of it you should have the DCP project somewhere in your computer and the environmental variable `SPOONFUL_PREFIX` defined. For convenience, we consider defined an additional environmental variable with DCP's project folder
```shell
$ export DCP_PREFIX="<path to dcp's parent folder>/dcp"
```

Currently we only provide instructions for tables whose results can be generated with the original DCP repository. The metrics you're looking for appear as `rot_RMSE`, `rot_MAE`, `trans_RMSE` and `trans_MAE` of the `A--------->B` output section. All follow-up commands assume your current working directory is DCP project folder.
```shell
$ cd "$DCP_PREFIX"
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


