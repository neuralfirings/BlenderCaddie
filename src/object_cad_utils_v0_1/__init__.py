bl_info = {
    "name": "BlenderCaddie",
    "author": "neuralfirings",
    "description": "Enabling CAD tools for Blender.",
    "version": (0, 1),
    "blender": (2, 72, 0),
    "location": "View3D > Toolbox",
    "warning": "", # used for warning icon and text in addons panel
    "tracker_url": "https://github.com/neuralfirings/BlenderCaddie",
    "wiki": "https://github.com/neuralfirings/BlenderCaddie/wiki",
    "category": "Mesh",
}

import bpy
import bmesh
import math

class CustomPanel(bpy.types.Panel):                   # Creates a custom tab in the Tool menu
    """A Custom Panel in the Viewport Toolbar"""
    bl_label = "BlenderCaddie"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = "CAD"

    def draw(self, context):
        layout = self.layout

        split = layout.split()
        col = split.column(align=True)

        col.label(text="SET EDGE LENGTH")
        col.label(text="1. In edit mode, select edges")
        col.operator("mesh.blender_caddie", text="2. Click here")
        col.label(text="3. See panel below to set value")
        
class Caddie(bpy.types.Operator):                     # Code for the Add On
    """Enabling some CAD features to Blender."""      # blender will use this as a tooltip for menu items and buttons.
    bl_idname = "mesh.blender_caddie"                 # unique identifier for buttons and menu items to reference.
    bl_label = "Blender Caddie"                       # display name in the interface.
    bl_options = {'REGISTER', 'UNDO'}                 # enable undo for the operator.
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'

    # the form field(s) that pop out when addon is activated
    target = bpy.props.IntProperty(name="Target", default=0, min=0, max=100)

    def execute(self, context): 
        print("========== CADDIE ===========")

        obj=bpy.context.object
        edges = []
        target = self.target
        
        if obj.mode == 'EDIT' and target > 0:
            bm=bmesh.from_edit_mesh(obj.data)
            for e in bm.edges: # for each edge in the object
                if e.select: # if edge is selected
                    edges.append(e)
                    
                    # Getting the scale factor to multiple the edge
                    original_distance = ((e.verts[1].co.x-e.verts[0].co.x)**2 + (e.verts[1].co.y-e.verts[0].co.y)**2 + (e.verts[1].co.z-e.verts[0].co.z)**2)**0.5
                    scale_to_target = target/original_distance-1
                    
                    # Store vertices in variables that are easier to work with
                    v1 = e.verts[0].co
                    v2 = e.verts[1].co

                    # Getting new vertices location
                    new_v2x = v1.x + (v2.x-v1.x) * (1+scale_to_target/2)
                    new_v2y = v1.y + (v2.y-v1.y) * (1+scale_to_target/2)
                    new_v2z = v1.z + (v2.z-v1.z) * (1+scale_to_target/2)
                    new_v1x = v1.x - (v2.x-v1.x) * (scale_to_target/2)
                    new_v1y = v1.y - (v2.y-v1.y) * (scale_to_target/2)
                    new_v1z = v1.z - (v2.z-v1.z) * (scale_to_target/2)

                    # Replacing old vertices with new vertices
                    v1.x = new_v1x
                    v1.y = new_v1y
                    v1.z = new_v1z
                    v2.x = new_v2x
                    v2.y = new_v2y
                    v2.z = new_v2z
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

if __name__ == "__main__": # this allows you to run script from Blender text editor w/o installing add on
    register()