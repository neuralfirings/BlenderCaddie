# ##### BEGIN GPU LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

# ################################################################
# Init
# ################################################################

bl_info = {
    "name": "BlenderCaddie",
    "author": "neuralfirings",
    "tracker_url": "https://github.com/neuralfirings/BlenderCaddie",
    "category": "Edit"
}


# To support reload properly, try to access a package var,
# if it's there, reload everything

import bpy
import bmesh
import math

class CustomPanel(bpy.types.Panel):
    """A Custom Panel in the Viewport Toolbar"""
    bl_label = "Blender Caddie"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = "CAD Tools"

    def draw(self, context):
        layout = self.layout

        row = layout.row()
#        row.label(text="Add Objects:")

        split = layout.split()
        col = split.column(align=True)

        col.operator("mesh.blender_caddie", text="Set Edge Length")
        

class Caddie(bpy.types.Operator):
    """adding some CAD features to Blender."""      # blender will use this as a tooltip for menu items and buttons.
    bl_idname = "mesh.blender_caddie"        # unique identifier for buttons and menu items to reference.
    bl_label = "Blender Caddie"                 # display name in the interface.
    bl_options = {'REGISTER', 'UNDO'}  # enable undo for the operator.
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'

    types = [
        ("pos", "Positive Direction", "", 1),
        ("neg", "Negative Direction", "", 2),
        ("center", "Bidirectional", "", 3)
    ]
        
    target = bpy.props.IntProperty(name="Target", default=0, min=0, max=100)
    type = bpy.props.EnumProperty(items=types, name="Type")

    def execute(self, context):        # execute() is called by blender when running the operator.
            
        print("========== CADDIE ===========")
        
        obj=bpy.context.object
        
        # VARIABLES
        vertices = []
        edges = []
        vertices_coords = []
        
        # PARAMETERS
        target = self.target
        type = self.type 
        
        # DO STUFF
        if obj.mode == 'EDIT' and target > 0:
            bm=bmesh.from_edit_mesh(obj.data)
            for v in bm.verts:
                if v.select:
                    vertices.append(v)
                    vertices_coords.append(v.co)
                    print(v.co)
            for e in bm.edges:
                if e.select:
                    edges.append(e)
                    print("--edge--")
                    print(e.verts[0].co)
                    print(e.verts[1].co)
                    
                    old_dist = ((e.verts[1].co.x-e.verts[0].co.x)**2 + (e.verts[1].co.y-e.verts[0].co.y)**2 + (e.verts[1].co.z-e.verts[0].co.z)**2)**0.5
                    diff = target - old_dist
                    diffscale = target/old_dist-1
                    
                    v1 = e.verts[0].co
                    v2 = e.verts[1].co
                    
                    if type=="pos":
                        v2.x = v1.x + (v2.x-v1.x) * (1+diffscale)
                        v2.y = v1.y + (v2.y-v1.y) * (1+diffscale)
                        v2.z = v1.z + (v2.z-v1.z) * (1+diffscale)
                    elif type == "neg":
                        v1.x = v1.x - (v2.x-v1.x) * (diffscale)
                        v1.y = v1.y - (v2.y-v1.y) * (diffscale)
                        v1.z = v1.z - (v2.z-v1.z) * (diffscale)
                    elif type=="center":
                        x2 = v2.x # store old variables
                        y2 = v2.y
                        z2 = v2.z
                        v2.x = v1.x + (v2.x-v1.x) * (1+diffscale/2)
                        v2.y = v1.y + (v2.y-v1.y) * (1+diffscale/2)
                        v2.z = v1.z + (v2.z-v1.z) * (1+diffscale/2)
                        v1.x = v1.x - (x2-v1.x) * (diffscale/2)
                        v1.y = v1.y - (y2-v1.y) * (diffscale/2)
                        v1.z = v1.z - (z2-v1.z) * (diffscale/2)
                    
        else:
            print("Object is not in edit mode.")

        bmesh.update_edit_mesh(obj.data)
        return {'FINISHED'}            # this lets blender know the operator finished successfully.

def menu_func(self, context):
    self.layout.operator(Caddie.bl_idname)
 
    
def register():
    bpy.utils.register_class(Caddie)
    bpy.utils.register_class(CustomPanel)
    
    
    

def unregister():
    bpy.utils.unregister_class(Caddie)


# This allows you to run the script directly from blenders text editor
# to test the addon without having to install it.
if __name__ == "__main__":
    register()
