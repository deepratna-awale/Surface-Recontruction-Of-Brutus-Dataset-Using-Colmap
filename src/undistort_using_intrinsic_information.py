# Undistortion script using python (requires intrinsics)
from scipy.spatial.transform import Rotation
import numpy as np

def fisheye_to_perspective(point, radial_distortion):
  """Remove fisheye and radial distortion, projecting to a perspective camera."""
  r = np.sqrt(point[0] * point[0] + point[1] * point[1])
  theta = np.arctan2(r, point[2])

  r2 = theta * theta
  distortion = 1.0 + r2 * (radial_distortion[0] + r2 * radial_distortion[1])

  return np.array(
      [theta / r * point[0] * distortion,
       theta / r * point[1] * distortion,
       1.0])


