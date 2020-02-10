bl_info = {
    "name": "Select Connected Faces by Normals",
    "author": "Johnathan Apuzen",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "Edit Mode > Select > Select Connected Faces by Normals",
    "description": "Selects connected faces to a face/s highlighted by the user, creating a group of faces. A face is added to a group if it meets the 'angle limit' and 'group angle limit' criterea. In each group, the difference between the normals of two connected faces is less than a specified 'angle limit'. A face is added to a group only if the difference between its normal and the group's total normal is less than a specified 'group angle limit'. The defaults of 20 derees for the angle and group angle limits work for relatively flat surfaces.",
    "category": "Mesh",
}

import bpy
from bpy.types import Operator
from bpy.props import FloatProperty
from mathutils import Vector
import bmesh
import queue

'''
Helper Functions
'''
#returns a list of selected faces, takes a bmesh object
def find_selected_faces(bm):
    selected_faces = []
    
    for face in bm.faces:
        if face.select == True:
            selected_faces.append(face)
            
    return selected_faces

#returns list of faces directly connected to the face
def find_connected_faces(bm, face):
    connected_faces = []
    
    for e in range(len(face.edges)):
        for connected_face in face.edges[e].link_faces:
            if connected_face != face:
                connected_faces.append(connected_face)
                
    return connected_faces

#create group of connected faces that meet the normal angle limits
#returns a list of the group of faces
def expand_selection_similar_normals(bm, starting_face, is_grouped, angle_limit, group_angle_limit):
    curr_group = []
    curr_group.append(starting_face)
    
    #total x, y, and z normal orientation of all faces in group
    curr_group_total = Vector((0,0,0))
    curr_group_total += starting_face.normal
    
    q = queue.Queue()
    q.put(starting_face)
    
    while(not(q.empty())):
        
        curr_face = q.get()
        connected_faces = find_connected_faces(bm, curr_face)
        
        for connected_face in connected_faces:
            
            #Calculate angle between current face normal and connected face normal
            diff = curr_face.normal.angle(connected_face.normal)
            #Calculate angle between group average normal and connected face normal
            group_diff = curr_face.normal.angle(curr_group_total/len(curr_group))
            
            #Check if connected face is valid
            if diff < angle_limit and group_diff < group_angle_limit:
                if not(is_grouped[connected_face.index]):
                    
                    curr_group.append(connected_face)
                    q.put(connected_face)
                    is_grouped[connected_face.index] = True
                    
                    #Add connected face's normal to group total
                    curr_group_total += connected_face.normal
    
    return curr_group


'''
Main Class/Execution
'''
class Select_Faces_by_Normals(Operator):
    """Selects connected faces whose normals meet the specified angle limits"""
    bl_idname = "select.connected_faces_by_normals"
    bl_label = "Select Connected Faces by Normals"
    bl_options = {'REGISTER', 'UNDO'}

    angle_limit: FloatProperty(
        name="Angle Limit",
        default=0.349066, #20 degrees in radians
        min=0,
        subtype='ANGLE',
        description="Maximum angle permitted between the normals of two directly connected faces."
    )
    
    group_angle_limit: FloatProperty(
        name="Group Angle Limit",
        default=0.349066, #20 degrees in radians
        min=0,
        subtype='ANGLE',
        description="Maximum angle permitted between a connected face and the whole group of faces."
    )

    def execute(self, context):
        
        #Check context, only works in edit mode
        if context.object.mode != 'EDIT':
            self.report({'ERROR'}, "Only works in Edit Mode")
            return {'CANCELLED'}
        
        groups = [] #groups of faces with similar normal based on angle limits
        
        #create bmesh object
        obj = context.edit_object
        me = obj.data
        bm = bmesh.from_edit_mesh(me)
        
        #look-up list to check if a face has been placed in a group
        is_grouped = [False] * len(bm.faces)
        
        #Find faces selected by user
        selected_faces = find_selected_faces(bm)
        
        #Report if no faces were selected
        if len(selected_faces) == 0:
            self.report({'ERROR'}, "No faces selected")
            return {'CANCELLED'}
        
        #For each selected face, find faces with similar normals based on angle limits
        for face in selected_faces:
            if not(is_grouped[face.index]):
                is_grouped[face.index] = True
                
                curr_group = expand_selection_similar_normals(bm, face, is_grouped, self.angle_limit, self.group_angle_limit)
                
                groups.append(curr_group)
        
        #select all faces in all groups
        for group in groups:
            for face in group:
                face.select_set(True)
        bmesh.update_edit_mesh(me)
        
        return {'FINISHED'}

#Used to place add-on in Select menu
def menu_func(self, context):
    self.layout.operator(Select_Faces_by_Normals.bl_idname)

'''
Registration
'''
def register():
    bpy.utils.register_class(Select_Faces_by_Normals)
    bpy.types.VIEW3D_MT_select_edit_mesh.append(menu_func)

def unregister():
    bpy.types.VIEW3D_MT_select_edit_mesh.remove(menu_func)
    bpy.utils.unregister_class(Select_Faces_by_Normals)

if __name__ == "__main__":
    register()