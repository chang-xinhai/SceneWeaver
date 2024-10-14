# Copyright (C) 2023, Princeton University.
# This source code is licensed under the BSD 3-Clause license found in the LICENSE file in the root directory of this source tree.

# Authors: Lingjie Mei
from collections.abc import Iterable

from numpy.random import uniform

from infinigen.assets.materials import common
from infinigen.assets.utils.uv import unwrap_normal
from infinigen.core.nodes.node_info import Nodes
from infinigen.core.nodes.node_utils import build_color_ramp
from infinigen.core.nodes.node_wrangler import NodeWrangler
from infinigen.core.util.color import hsv2rgba
from infinigen.core.util.random import log_uniform


def shader_plaster(nw: NodeWrangler, plaster_colored, **kwargs):
    # 随机生成色相和亮度值
    hue = uniform(0, 1)
    front_value = log_uniform(0.5, 1.0)
    back_value = front_value * uniform(0.6, 1)

    # 根据 plaster_colored 的值生成前景和背景颜色
    if plaster_colored:
        front_color = hsv2rgba(hue, uniform(0.3, 0.5), front_value)
        back_color = hsv2rgba(hue + uniform(-0.1, 0.1), uniform(0.3, 0.5), back_value)
    else:
        front_color = hsv2rgba(hue, 0, front_value)
        back_color = hsv2rgba(hue + uniform(-0.1, 0.1), 0, back_value)

    # 创建 UV 映射节点
    uv_map = nw.new_node(Nodes.UVMap)

    # 创建穆斯格雷夫纹理节点
    musgrave = nw.new_node(
        Nodes.MusgraveTexture,
        [uv_map],
        input_kwargs={"Detail": log_uniform(15, 30), "Dimension": 0},
    )

    # 创建噪声纹理节点
    noise = nw.new_node(
        Nodes.NoiseTexture,
        [uv_map],
        input_kwargs={"Detail": log_uniform(15, 30), "Distortion": log_uniform(4, 8)},
    )
    # 构建颜色渐变
    noise = build_color_ramp(
        nw, noise, [0, uniform(0.3, 0.5)], [(0, 0, 0, 1), (1, 1, 1, 1)]
    )

    # 将穆斯格雷夫纹理和噪声结合为差异效果
    difference = nw.new_node(
        Nodes.MixRGB, [musgrave, noise], attrs={"blend_type": "DIFFERENCE"}
    )

    # 创建基础颜色
    base_color = build_color_ramp(
        nw, difference, [uniform(0.2, 0.3), 1], [back_color, front_color]
    )

    # 创建位移节点
    displacement = nw.new_node(
        Nodes.Displacement,
        input_kwargs={
            "Scale": log_uniform(0.0001, 0.0003),
            "Height": nw.new_node(
                Nodes.MusgraveTexture, input_kwargs={"Scale": uniform(1e3, 2e3)}
            ),
        },
    )

    # 创建 BSDF 节点
    principled_bsdf = nw.new_node(
        Nodes.PrincipledBSDF,
        input_kwargs={
            "Base Color": base_color,
            "Roughness": uniform(0.7, 0.8),
        },
    )

    # 输出材质节点
    nw.new_node(
        Nodes.MaterialOutput,
        input_kwargs={"Surface": principled_bsdf, "Displacement": displacement},
    )


def apply(obj, selection=None, plaster_colored=None, **kwargs):
    if plaster_colored is None:
        plaster_colored = uniform() < 0.4
    for o in obj if isinstance(obj, Iterable) else [obj]:
        unwrap_normal(o, selection)
    common.apply(
        obj, shader_plaster, selection, plaster_colored=plaster_colored, **kwargs
    )
