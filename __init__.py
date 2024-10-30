bl_info = {
    "name": "pick_tool",
    "author": "zhuhe",
    "version": (0, 5, 0),
    "blender": (3, 6, 8),
    "location": "View3D > Sidebar >Pick",
    "description": "轨迹管理工具",
    "warning": "",
    "doc_url": "",
    "category": "Object",
}

# 提取点坐标工具，将选择的顶点提取出来

import bpy
import os
import sys
import json
import math
import numpy as np
import warnings
import shutil

from bpy.props import (
        IntProperty,
        FloatProperty,
        StringProperty,
        BoolProperty,
        PointerProperty,
        EnumProperty
        )

global_index = []
global_co = []

class Point_output(bpy.types.Operator):

    bl_label='导出数据'
    bl_idname = 'obj.pointoutput' # no da xie
    bl_options = {"REGISTER", "UNDO"}
    
    def execute(self, context):
        ppphy = context.scene.ppphy
        point_output(ppphy.output_path, ppphy)
        return {'FINISHED'}
    
class Point_step(bpy.types.Operator):

    bl_label='导出数据'
    bl_idname = 'obj.pointstep' # no da xie
    bl_options = {"REGISTER", "UNDO"}
    
    def execute(self, context):
        ppphy = context.scene.ppphy
        point_step(ppphy)
        return {'FINISHED'}

class Point_cancel(bpy.types.Operator):

    bl_label='清除数据'
    bl_idname = 'obj.pointclean' # no da xie
    bl_options = {"REGISTER", "UNDO"}
    
    def execute(self, context):
        ppphy = context.scene.ppphy
        point_clean(ppphy)
        return {'FINISHED'}
    


def point_output(output_path, ppphy):
    global global_index, global_co
    res = {}

    
    res["index"] = global_index
    res["co"] = global_co
    print(res["co"])
    with open(os.path.join(output_path, ppphy.pick_name + '.json'), 'w', encoding='utf-8') as f:
        json.dump(res, f, ensure_ascii=False, indent=4)

def point_step(ppphy):
    global global_index, global_co
        
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.mode_set(mode='EDIT')

    selected_index = [v.index for v in bpy.context.object.data.vertices if v.select]
    selected_co = [list(v.co) for v in bpy.context.object.data.vertices if v.select]
    if len(selected_index) == len(global_index):
        raise warnings.warn("未选择新的顶点")
    elif len(selected_index) == len(global_index) + 1:
        for index in selected_index:
            if index not in global_index:
                global_index.append(index)
                global_co.append(selected_co[selected_index.index(index)])
    else:
        raise ValueError("选择顶点数量错误")  
    
    point_update(ppphy)

def point_clean(ppphy):
    global global_index, global_co
    global_index = []
    global_co = []

    point_update(ppphy)


def point_update(ppphy):
    ppphy.pick_num = len(global_index)
    if len(global_index) > 0:
        ppphy.pick_index_latest = global_index[-1]

    else:
        ppphy.pick_index_latest = -1

# RNA属性 在当前场景中命名为traph子类
class Pick_property(bpy.types.PropertyGroup):
    
    output_path: bpy.props.StringProperty(name='output_path',subtype='FILE_PATH')
    pick_target: bpy.props.PointerProperty(name='spray_target', type=bpy.types.Object)
    pick_name: bpy.props.StringProperty(name='pick_name')
    pick_num: bpy.props.IntProperty(name='pick_num', default=0, options={'SKIP_SAVE', 'HIDDEN'})
    pick_index_latest: bpy.props.IntProperty(name='pick_index_latest', default=0, options={'SKIP_SAVE', 'HIDDEN'})

class Pick_ui(bpy.types.Panel):
    bl_idname = "Pick_ui"
    bl_label = "顶点提取工具"

    # 标签分类
    bl_category = "PICK TOOL"

    # ui_type
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    def draw(self, context):
        layout = self.layout
        layout.label(text="顶点提取")
        scene = context.scene.ppphy
        col = layout.column()
        row = col.row(align=False)
        row.prop(scene, "pick_name", text="轨迹名称")
        row.prop(scene, "output_path", text="导出路径")
        row = col.row(align=False)
        row.operator("obj.pointstep", text="记录")
        row.operator("obj.pointclean", text="清除记录")
        row = col.row(align=False)
        row.operator("obj.pointoutput", text="导出轨迹")
        row = col.row(align=False)
        row.prop(scene, "pick_num", text="已记录点数量")
        row.prop(scene, "pick_index_latest", text="最新点索引")


    
classGroup = [Pick_property,
        Point_output,
        Point_step,
        Point_cancel,
        Pick_ui
]


def register():
    bpy.types.Scene.collection_index = bpy.props.IntProperty() # 自定义列表索引
    for item in classGroup:
        # print(1)
        bpy.utils.register_class(item)
    bpy.types.Scene.ppphy = bpy.props.PointerProperty(type=Pick_property)


def unregister():
    del bpy.types.Scene.collection_index
    for item in classGroup:
        bpy.utils.unregister_class(item)


if __name__ == '__main__':
    register()
