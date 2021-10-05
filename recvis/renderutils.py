import bpy
import bmesh
import numpy as np
from analyzeOptions import *
from tools.dimensions import *
from tools.geo import *
import pickle
def generateArrays():
    #=---------------------------------
    template_Array = bpy.data.objects.get('Array')
    try: bpy.data.collections['Arrays']
    except:
        arraycollection = bpy.data.collections.new('Arrays')
        bpy.context.scene.collection.children.link(arraycollection)
        if template_Array:
            print("Arrays")
            for i in tqdm(range(nArray)):
                array = template_Array.copy()
                array.location = units*(ArraytoGlobalCoordinates(0,0,0,i))
                array.rotation_euler = Euler((0, 0, theta*i), 'XYZ')
                arraycollection.objects.link(array)
    else: arraycollection = bpy.data.collections['Arrays']
    #=---------------------------------
def loadXYZ():
    try:
        with open(Options.render_pkl, 'rb') as f:  # Python 3: open(..., 'wb')
            print("[OPENING]")
            xyz = pickle.load(f)
    except FileNotFoundError as VALERIN:
        print(VALERIN)
        print("[REGENERATION] Render Pickling...")
        from recvis.render import render
        xyz = render()
    return xyz
def plot():
    try: 
        bpy.data.collections['Hit']
        hitcollection = bpy.data.collections['Hit']
        while hitcollection.objects:
            hitcollection.objects.unlink(hitcollection.objects[0])
    except:
        hitcollection = bpy.data.collections.new('Hit')
        bpy.context.scene.collection.children.link(hitcollection)
    verts = loadXYZ().T  * blenderOptions.unitScale
    try: 
        _extracted_from_plot_12(hitcollection,verts)
    except Exception as e: 
        print(e)
        _extracted_from_plot_22(hitcollection, verts)

    bpy.data.particles["ParticleSettings.004"].count = len(verts)

def _extracted_from_plot_12(hitcollection, verts):
    mesh = bpy.data.meshes.get("PointCloud.001")
    obj =  bpy.data.objects.get("PointCloud.001")
    bpy.context.view_layer.objects.active = obj  # set as the active object in the scene

    bpy.ops.object.mode_set(mode = 'EDIT')
    bpy.ops.mesh.delete(type='VERT')
    bm = bmesh.from_edit_mesh(mesh)
    # vert0 = obj.data.vertices
    # for v in vert0:
    #     v.select = 1
    # bmesh.ops.delete(bm, geom=verts, context=1)
    for v in verts:
        bm.verts.new(v)
    bmesh.update_edit_mesh(mesh)
    bm.free()
    bpy.ops.object.mode_set(mode = 'OBJECT')
    
    # hitcollection.objects.link(obj)

def _extracted_from_plot_22(hitcollection, verts):
    print("NEW PointCloud")
    mesh = bpy.data.meshes.new("PointCloud")  # add a new mesh
    obj = bpy.data.objects.new("PointCloud", mesh)  # add a new object using the mesh

    scene = bpy.context.collection
    scene.objects.link(obj)  # put the object into the scene (link)
    bpy.context.view_layer.objects.active = obj  # set as the active object in the scene
    # hitcollection.objects.link(obj)

    obj.select_set(True)  # select object

    mesh = bpy.context.object.data
    bm = bmesh.new()

    for v in verts:
        bm.verts.new(v)  # add a new vert

    # make the bmesh the object's mesh
    bm.to_mesh(mesh)
    bm.free()  # always do this when finished


    