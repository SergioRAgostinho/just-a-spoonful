# (Just) A Spoonful of Refinements Helps the Registration Error Go Down

Official repository for the ICCV 2021 (Oral) paper "(Just) A Spoonful of Refinements Helps the Registration Error Go Down"

**Paper:** [CVF Open Access](https://openaccess.thecvf.com/content/ICCV2021/html/Agostinho_Just_A_Spoonful_of_Refinements_Helps_the_Registration_Error_Go_ICCV_2021_paper.html)

**Poster:** [here](docs/poster.pdf)

**Video:** [YouTube](https://www.youtube.com/watch?v=Ut1mLi1cQpI)

**Abstract:**

In this paper, we tackle data-driven 3D point cloud registration. Given point correspondences, the standard Kabsch algorithm provides an optimal rotation estimate. This allows to train registration models in an end-to-end manner by differentiating the SVD operation. However, given the initial rotation estimate supplied by Kabsch, we show we can improve point correspondence learning during model training by extending the original optimization problem. In particular, we linearize the governing constraints of the rotation matrix and solve the resulting linear system of equations. We then iteratively produce new solutions by updating the initial estimate. Our experiments show that, by plugging our differentiable layer to existing learning-based registration methods, we improve the correspondence matching quality. This yields up to a 7% decrease in rotation error for correspondence-based data-driven registration methods. 

## Implementation Release

The repository provides a stripped and clean version of the method reported in the paper that can be added to any correspondence based point cloud registration method. To use it just call
```shell
pip install git+https://github.com/SergioRAgostinho/just-a-spoonful.git
```
and import it from your code as
```python
from spoonful import spoonful
```
Here's the docstring for the function explaining how to use it. You can access it by calling
```
>>> help(spoonful)

Help on function spoonful in module spoonful:

spoonful(R: torch.Tensor, Ps: torch.Tensor, Pt: torch.Tensor, iters: int = 5, weights: torch.Tensor = None, use_target: bool = False, eps: float = 1e-05) -> Tuple[torch.Tensor, torch.Tensor]
    Takes up a candidate rotation and a set of correspondences from the source and target
    point clouds and produces additional poses under the linearized constraints for the rotation.

    This is the function in this file you'll want to call most often.

    B - Batch size
    N - Number of correspondences
    I - Number of iterations

    Parameters:
        R : A batch of initial rotation matrices Bx3x3
        Ps: Correspondence points from the source point cloud BxNx3
        Pt: Correspondence points from the target point cloud BxNx3
        iters: Number of iterations to perform
        weights: A tensor of non-negative weights ranking each correspondence BxN
        use_target: Whether the source or target point clouds should be used to form matrix A. If you experience instability, try setting it to True
        eps: Small epsilon to prevent division by zero situations


    Returns:
        R_all: A set of new rotation estimates BxIx3x3
        t_all: A set of new translation estimates BxIx3
```


## Model Release

Because the paper proposes exclusively a new training technique and shows its benefits in two separate networks -- DCP and RPM-Net -- one can still use the original projects to evaluate the improvements of the newly trained weights in their old tasks, using the DCP's and RPM-Net's published code. After following the instruction bellow, you'll have a minimal setup to start generating some of the tables in the paper. For instruction on how to do that check [docs/reproducing-results.md](docs/reproducing-results.md).

### Downloading All Pretrained Models

If you have access `wget` and `unzip` installed and visible in your PATH, I've packaged a script that will download and extract the weights to [share/weights](share/weights), and verify their integrity automatically.
1. Install `gdown` dependency to download files from Google Drive. This is included in the [requirements.txt](requirements.txt) file.
    ```shell
    pip install -r requirements.txt
    ```
2. Call the script
    ```shell
    python download_weights.py
    ```


In case you don't have these utilities installed, you can also download the weights from [here](http://web.tecnico.ulisboa.pt/sergio.agostinho/share/just-a-spoonful/weights.zip) (as well as from their original projects) and manually extract them to [share/weights](share/weights). If you go down the manual route, you'll need to rename and move the files appropriately. Check [download_weights.py](download_weights.py#L10-L34) for an insight into the required urls and file names.
The SHA-1 checksums for all files are available at [share/weights/weights.sha1sum](share/weights/weights.sha1sum).

---
### DCP Fork

This should be your preferred method for evaluating DCP models moving forward. It will allow you to reproduce most tables in the paper.

1. Clone the fork from https://github.com/SergioRAgostinho/dcp.git and navigate to that project's folder
    ```shell
    git clone https://github.com/SergioRAgostinho/dcp.git; cd dcp
    ```
2. Export the path to `dcp` project, for later reuse
    ```shell
    export DCP_PREFIX="<substitute with the appropriate parent folder>/dcp"
    ```
4. Install DCP's dependencies according to the original [instructions](https://github.com/SergioRAgostinho/dcp#prerequisites)

### Original DCP

Note: Skip this if you already executed the steps in [DCP Fork](#dcp-fork).

Adopting this procedure will prevent you from reproducing certain results presented in the paper. The procedure might be deprecated in the future.

1. Clone the original repository from https://github.com/WangYueFt/dcp.git and navigate to that project's folder
    ```shell
    git clone https://github.com/WangYueFt/dcp.git; cd dcp
    ```
2. Export the path to `dcp` project, for later reuse
    ```shell
    export DCP_PREFIX="<substitute with the appropriate parent folder>/dcp"
    ```
3. DCP needs to be patched for two things: 1) It currently fails to download modelnet40 data due to a missing option in the `wget` call; 2) In order to recreate the exact results reported in our paper, there is randomized step that needs to be made deterministic. The patch in [share/patches/dcp-data.diff](share/patches/dcp-data.diff) addresses both. To apply it, run the following (still in DCP's root folder)
    ```shell
    git apply $SPOONFUL_PREFIX/share/patches/dcp-data.diff
    ```
4. Install DCP's dependencies according to their [instructions](https://github.com/WangYueFt/dcp#prerequisites)



### RPM-Net

1. Clone the original repository from https://github.com/yewzijian/RPMNet.git and navigate to that project's folder
    ```shell
    git clone https://github.com/yewzijian/RPMNet.git; cd RPMNet
    ```
2. Export the path to `RPM-Net` project, for later reuse
    ```shell
    export RPM_PREFIX="<substitute with the appropriate parent folder>/RPMNet"
    ```
3. Install RPM-Net's dependencies according to their [instructions](https://github.com/yewzijian/RPMNet#prerequisites).



## Announcements

#### December 21th 2021

I've released the necessary models and script to generate the results from the DCP initialization experiment (Table 4). To do so, I had to include all pretrained models into the current model pack, which severely increased the list of models being distributed and the repository size. (60MB -> ~900MB)

#### December 20th 2021

I've started releasing modifications to the original DCP project in order to reproduce paper results. The new fork is located at https://github.com/SergioRAgostinho/dcp.git. I will prioritize reproducing all results first before moving into training code.


#### December 17th 2021

I've released a cleaned up version of the method presented in the paper! I've quickly validated it's producing the same outputs but it's still pending actually trying it on a fresh DCP and RPM-Net repo for training. I'll publish the required modifications for that in the next days/weeks.

I've also information about the environments I used while training DCP and RPM-Net in [share/envs](share/envs).

#### December 15th 2021

I've released models and instructions for recreating the RPM-Net's results with their project.

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

For the time being, I've earned myself some vacations. ????????
