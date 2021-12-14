# (Just) A Spoonful of Refinements Helps the Registration Error Go Down

Official repository for the ICCV 2021 (Oral) paper "(Just) A Spoonful of Refinements Helps the Registration Error Go Down"

**Paper:** [CVF Open Access](https://openaccess.thecvf.com/content/ICCV2021/html/Agostinho_Just_A_Spoonful_of_Refinements_Helps_the_Registration_Error_Go_ICCV_2021_paper.html)

**Poster:** [here](docs/poster.pdf)

**Video:** [YouTube](https://www.youtube.com/watch?v=Ut1mLi1cQpI)

**Abstract:**

In this paper, we tackle data-driven 3D point cloud registration. Given point correspondences, the standard Kabsch algorithm provides an optimal rotation estimate. This allows to train registration models in an end-to-end manner by differentiating the SVD operation. However, given the initial rotation estimate supplied by Kabsch, we show we can improve point correspondence learning during model training by extending the original optimization problem. In particular, we linearize the governing constraints of the rotation matrix and solve the resulting linear system of equations. We then iteratively produce new solutions by updating the initial estimate. Our experiments show that, by plugging our differentiable layer to existing learning-based registration methods, we improve the correspondence matching quality. This yields up to a 7% decrease in rotation error for correspondence-based data-driven registration methods. 


## Annoucements

#### October 12th 2021

Due to high workload, I couldn't manage to release the code on time for ICCV 2021. With the CVPR 2022 submission coming up, I will only be able to allocate some time to this past the deadline. My release plans is as follows:
1. Publish the trained models we produced by employing our method. These can be used to replicate our results in DCP's and RPM-Net's official implementations, i.e. no need to wait for my code upload to evaluate results;
2. Release of the method responsible for solving our alternate optimization problem, than can be directly injected into DCP and RPM-Net;
3. Full release with training code, etc...

My apologies for the delay. Feel free to ping me from time to time for updates. 

#### July 29th 2021

The official (cleaned-up) implementation and an arXiv version of the camera-ready version of paper will be released leading up to the conference date.

For the time being, I've earned myself some vacations. 🏖😎
