import os
import pathlib
from ROI_funcs import wb_convert

cwd = pathlib.Path().resolve().parent
map_to_conv = os.path.join(cwd.parent, 'Hierarchies/action_observation_absBIn.nii.gz')
out_name = os.path.join(cwd.parent, 'Hierarchies/action_observation_absBIn')

surf_type = 'pial'
wb_convert(map_to_conv, out_name, surf_type)
