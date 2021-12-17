from math import nan
from typing import Tuple
import torch

__version__ = "1.0.0-rc1"


def solve_linearized(
    R: torch.Tensor, AA: torch.Tensor, Ab: torch.Tensor
) -> torch.Tensor:
    """
    Find the rotation that minimizes distance error between correspondences
    enforcing linearized rotation constraints.

    B - batch size

    Parameters:
        R: An initial rotation Bx3x3

    Returns:
        A solution of size Bx3x3
    """
    nb = len(R)
    R_out = torch.full(R.shape, nan, dtype=R.dtype, device=R.device)

    Eij = (
        torch.eye(3, device=R.device)[:, None, :, None]
        * torch.eye(3, device=R.device)[:, None]
    ).reshape((-1, 3, 3))
    Ekl = Eij[[0, 1, 2, 4, 5, 8]]

    f = (R.transpose(-1, -2) @ R - torch.eye(3, device=R.device)).view(-1, 9)[
        :, [0, 1, 2, 5, 6, 8]
    ]
    J = R[:, None] @ (Ekl + Ekl.transpose(-1, -2))
    Ac = torch.cat(
        [
            torch.cat([AA, J.permute(0, 2, 3, 1).reshape(-1, 9, 6)], dim=-1),
            torch.cat(
                [
                    J.transpose(-2, -1).reshape(-1, 6, 9),
                    torch.zeros(nb, 6, 6, device=AA.device),
                ],
                dim=-1,
            ),
        ],
        dim=-2,
    )
    bc = torch.cat(
        [Ab, torch.unsqueeze(torch.sum(J * R[:, None], dim=(-2, -1)) - f, -1)], dim=-2
    )

    try:
        # prevents issues with backprop update suddenly producing NaNs
        mask = torch.svd(Ac)[1][:, -1] > torch.finfo(Ac.dtype).eps
        X = torch.solve(bc[mask], Ac[mask])[0]
    except RuntimeError:
        return R_out

    R_out[mask] = X[:, :9].view(-1, 3, 3).transpose(-2, -1)
    return R_out


def form_rotation(R: torch.Tensor) -> torch.Tensor:
    """
    Forms a rotation matrix from a candidate rotation matrix in a process with close
    ties to Gram-Schmidt orthogonalization.

    B - Batch size

    Parameters:
        R: A candidate rotation matrix Bx3x3

    Returns:
        Rout: Rotation matrices of size Bx3x3
    """

    # 1st column
    col1 = R[:, :, 0] / R[:, :, 0].norm(dim=-1, keepdim=True)

    # 2nd column
    tmp = (
        (torch.eye(3, device=R.device) - col1[:, :, None] * col1[:, None])
        @ R[:, :, 1, None]
    ).view_as(R[:, :, 1])
    col2 = tmp / tmp.norm(dim=-1, keepdim=True)

    # 3rd column
    col3 = torch.cross(col1, col2, dim=-1)
    Rout = torch.stack([col1, col2, col3], dim=-1)
    return Rout


def spoonful(
    R: torch.Tensor,
    Ps: torch.Tensor,
    Pt: torch.Tensor,
    iters: int = 5,
    weights: torch.Tensor = None,
    use_target: bool = False,
    eps: float = 1e-5,
) -> Tuple[torch.Tensor, torch.Tensor]:
    """
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
    """

    A = torch.full_like(R, nan)
    b = torch.full_like(R, nan)

    if weights is None:
        weights = Ps.new_ones(Ps.shape[:2])

    wn = weights / (weights.sum(dim=-1, keepdim=True) + eps)

    # weighted mean
    Psm = torch.sum(wn[..., None] * Ps, dim=1, keepdim=True)
    Ptm = torch.sum(wn[..., None] * Pt, dim=1, keepdim=True)

    Psc = Ps - Psm
    Ptc = Pt - Ptm

    # Reshaping the linear system of equations
    Eij = (
        torch.eye(3, device=A.device)[:, None, :, None]
        * torch.eye(3, device=A.device)[:, None, :]
    ).reshape((-1, 3, 3))

    if use_target:
        A = Ptc.transpose(-1, -2) @ (wn[..., None] * Ptc)
        AA = (A[:, None] @ Eij).transpose(-1, -2).reshape(-1, 9, 9)
    else:
        A = Psc.transpose(-1, -2) @ (wn[..., None] * Psc)
        AA = (Eij @ A[:, None]).transpose(-1, -2).reshape(-1, 9, 9)

    b = Ptc.transpose(-1, -2) @ (wn[..., None] * Psc)
    Ab = b.view(-1, 9, 1)

    # Linearize
    R_all = []
    for _ in range(iters):
        R = solve_linearized(R, AA, Ab)
        R = form_rotation(R)
        R_all.append(R)

    R_all = torch.stack(R_all, dim=1)
    t_all = Ptm.transpose(-1, -2)[:, None] - R_all @ Psm.transpose(-1, -2)[:, None]
    return R_all, t_all.squeeze(-1)
