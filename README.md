# (Just) A Spoonful of Refinements Helps the Registration Error Go Down

Official repository for the ICCV 2021 (Oral) paper "(Just) A Spoonful of Refinements Helps the Registration Error Go Down"

**Paper:** [CVF Open Access](https://openaccess.thecvf.com/content/ICCV2021/html/Agostinho_Just_A_Spoonful_of_Refinements_Helps_the_Registration_Error_Go_ICCV_2021_paper.html)

**Poster:** [here](docs/poster.pdf)

**Video:** [YouTube](https://www.youtube.com/watch?v=Ut1mLi1cQpI)

**Abstract:**

In this paper, we tackle data-driven 3D point cloud registration. Given point correspondences, the standard Kabsch algorithm provides an optimal rotation estimate. This allows to train registration models in an end-to-end manner by differentiating the SVD operation. However, given the initial rotation estimate supplied by Kabsch, we show we can improve point correspondence learning during model training by extending the original optimization problem. In particular, we linearize the governing constraints of the rotation matrix and solve the resulting linear system of equations. We then iteratively produce new solutions by updating the initial estimate. Our experiments show that, by plugging our differentiable layer to existing learning-based registration methods, we improve the correspondence matching quality. This yields up to a 7% decrease in rotation error for correspondence-based data-driven registration methods. 

## Model Release

Because the paper proposes exclusively a new training technique and shows its benefits in two separate networks -- DCP and RPM-Net -- one can still use the original projects to evaluate the improvements of the newly trained weights in their old tasks, using the DCP's and RPM-Net's published code.

### Downloading All Pretrained Models

If you have access `wget` and `unzip` installed and visible in your PATH, I've packaged a script that will download and extract the weights to [share/weights](share/weights), and verify their integrity automatically. In case you don't have these utilities installed, you can also download the weights from [here](http://web.tecnico.ulisboa.pt/sergio.agostinho/share/just-a-spoonful/weights.zip) and manually extract them to [share/weights](share/weights). The SHA-1 checksums for all files are available at [share/weights/weights.sha1sum](share/weights/weights.sha1sum). Invoke the following command to call the download script.
```shell
$ python download_weights.py
```

### DCP

1. Clone the original repository from https://github.com/WangYueFt/dcp.git and navigate to that project's folder
    ```shell
    $ git clone https://github.com/WangYueFt/dcp.git; cd dcp
    ```
2. Export the path to `just-a-spoonful` project, for later reuse
    ```shell
    $ export SPOONFUL_PREFIX="<substitute with the apropriate parent folder>/just-a-spoonful"
    ```
3. DCP needs to be patched for two things: 1) It currently fails to download modelnet40 data due to a missing option in the `wget` call; 2) In order to recreate the exact results reported in our paper, there is randomized step that needs to be made deterministic. The patch in [share/patches/dcp-data.diff](share/patches/dcp-data.diff) addresses both. To apply it, run the following (still in DCP's root folder)
    ```shell
    $ git apply $SPOONFUL_PREFIX/share/patches/dcp-data.diff
    ```

With this we have the minimal setup to start generating some of the tables in the paper. For instruction on how to do that check [docs/reproducing-results.md](docs/reproducing-results.md).


## Annoucements

#### December 14th 2021

I'm finally putting some work into releasing the code. Current releasing the trained models for DCP. I'll release more things in the coming days.

#### October 12th 2021

Due to high workload, I couldn't manage to release the code on time for ICCV 2021. With the CVPR 2022 submission coming up, I will only be able to allocate some time to this past the deadline. My release plans is as follows:
1. Publish the trained models we produced by employing our method. These can be used to replicate our results in DCP's and RPM-Net's official implementations, i.e. no need to wait for my code upload to evaluate results;
2. Release of the method responsible for solving our alternate optimization problem, than can be directly injected into DCP and RPM-Net;
3. Full release with training code, etc...

My apologies for the delay. Feel free to ping me from time to time for updates. 

#### July 29th 2021

The official (cleaned-up) implementation and an arXiv version of the camera-ready version of paper will be released leading up to the conference date.

For the time being, I've earned myself some vacations. 🏖😎
