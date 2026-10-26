import bpy,sys,glob,hashlib,json,os
root=sys.argv[sys.argv.index('--')+1]; out=sys.argv[sys.argv.index('--')+2]
res={}
for f in sorted(glob.glob(root+'/**/*.fbx',recursive=True)):
    rel=os.path.relpath(f,root)
    try:
        bpy.ops.import_scene.fbx(filepath=f,use_anim=True)
    except Exception as e:
        res[rel]={'err':str(e)}; continue
    arm=[o for o in bpy.data.objects if o.type=='ARMATURE']
    acts=list(bpy.data.actions)
    info={'bones':len(arm[0].data.bones) if arm else 0,'meshes':len([o for o in bpy.data.objects if o.type=='MESH'])}
    if acts:
        a=acts[0]; h=hashlib.md5(); n=0
        hipsx=[]
        for fc in sorted([fc for cb in a.layers[0].strips[0].channelbags for fc in cb.fcurves],key=lambda c:(c.data_path,c.array_index)):
            for k in fc.keyframe_points:
                h.update(("%d:%.3f"%(round(k.co[0]),k.co[1])).encode()); n+=1
            if fc.data_path.endswith('Hips"].location'):
                hipsx.append((fc.array_index,[k.co[1] for k in fc.keyframe_points]))
        info.update(fps=bpy.context.scene.render.fps,frames=[round(x) for x in a.frame_range],keys=n,hash=h.hexdigest())
        # horizontal travel of hips (cm): axes 0 and 2 in mixamo local
        tr=0
        for i,v in hipsx:
            if i in (0,2) and v: tr=max(tr,max(v)-min(v))
        info['travel']=round(tr,1)
    res[rel]=info
    for o in list(bpy.data.objects): bpy.data.objects.remove(o,do_unlink=True)
    for a in list(bpy.data.actions): bpy.data.actions.remove(a)
    for m in list(bpy.data.meshes): bpy.data.meshes.remove(m)
    for m in list(bpy.data.armatures): bpy.data.armatures.remove(m)
json.dump(res,open(out,'w'),indent=1)
print("DONE",len(res))
