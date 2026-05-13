bl_info = {
    "name": "Pinned Modifiers",
    "author": "Francesco Yoshi Gobbo",
    "version": (1, 0, 0),
    "blender": (4, 3, 0),
    "location": "Properties > Modifiers > Add Modifier",
    "description": "Pins favorite modifiers setups to the Add Modifier menu.",
    "category": "Interface",
}

import bpy
import json
import os
from bpy_extras.io_utils import ExportHelper, ImportHelper

# NOTE: in case of variations to the modifiers list, change in both AVAILABLE_MODIFIERS, and in the PinnedModifiersPreferences class.

AVAILABLE_MODIFIERS = {
    # --- EDIT SECTION ---
    'pin_data_transfer': {"name": "Data Transfer", "kind": "MODIFIER", "type": 'DATA_TRANSFER', "icon": 'MOD_DATA_TRANSFER'},
    'pin_mesh_cache': {"name": "Mesh Cache", "kind": "MODIFIER", "type": 'MESH_CACHE', "icon": 'MOD_MESHDEFORM'},
    'pin_mesh_sequence_cache': {"name": "Mesh Sequence Cache", "kind": "MODIFIER", "type": 'MESH_SEQUENCE_CACHE', "icon": 'MOD_MESHDEFORM'},
    'pin_uv_project': {"name": "UV Project", "kind": "MODIFIER", "type": 'UV_PROJECT', "icon": 'MOD_UVPROJECT'},
    'pin_uv_warp': {"name": "UV Warp", "kind": "MODIFIER", "type": 'UV_WARP', "icon": 'MOD_UVPROJECT'},
    'pin_vertex_weight_edit': {"name": "Vertex Weight Edit", "kind": "MODIFIER", "type": 'VERTEX_WEIGHT_EDIT', "icon": 'MOD_VERTEX_WEIGHT'},
    'pin_vertex_weight_mix': {"name": "Vertex Weight Mix", "kind": "MODIFIER", "type": 'VERTEX_WEIGHT_MIX', "icon": 'MOD_VERTEX_WEIGHT'},
    'pin_vertex_weight_proximity': {"name": "Vertex Weight Proximity", "kind": "MODIFIER", "type": 'VERTEX_WEIGHT_PROXIMITY', "icon": 'MOD_VERTEX_WEIGHT'},
    
    # --- GENERATE SECTION ---
    'pin_array': {"name": "Array", "kind": "NODES", "node_group": "Array", "icon": 'MOD_ARRAY'},
    'pin_array_legacy': {"name": "Array (Legacy)", "kind": "MODIFIER", "type": 'ARRAY', "icon": 'MOD_ARRAY'}, # Legacy Version
    'pin_bevel': {"name": "Bevel", "kind": "MODIFIER", "type": 'BEVEL', "icon": 'MOD_BEVEL'},
    'pin_boolean': {"name": "Boolean", "kind": "MODIFIER", "type": 'BOOLEAN', "icon": 'MOD_BOOLEAN'},
    'pin_build': {"name": "Build", "kind": "MODIFIER", "type": 'BUILD', "icon": 'MOD_BUILD'},
    'pin_curve_to_tube': {"name": "Curve to Tube", "kind": "NODES", "node_group": "Curve to Tube", "icon": 'GEOMETRY_NODES'},
    'pin_decimate': {"name": "Decimate", "kind": "MODIFIER", "type": 'DECIMATE', "icon": 'MOD_DECIM'},
    'pin_edge_split': {"name": "Edge Split", "kind": "MODIFIER", "type": 'EDGE_SPLIT', "icon": 'MOD_EDGESPLIT'},
    'pin_mask': {"name": "Mask", "kind": "MODIFIER", "type": 'MASK', "icon": 'MOD_MASK'},
    'pin_mirror': {"name": "Mirror", "kind": "MODIFIER", "type": 'MIRROR', "icon": 'MOD_MIRROR'},
    'pin_multires': {"name": "Multiresolution", "kind": "MODIFIER", "type": 'MULTIRES', "icon": 'MOD_MULTIRES'},
    'pin_remesh': {"name": "Remesh", "kind": "MODIFIER", "type": 'REMESH', "icon": 'MOD_REMESH'},
    'pin_scatter_on_surface': {"name": "Scatter on Surface", "kind": "NODES", "node_group": "Scatter on Surface", "icon": 'GEOMETRY_NODES'},
    'pin_screw': {"name": "Screw", "kind": "MODIFIER", "type": 'SCREW', "icon": 'MOD_SCREW'},
    'pin_skin': {"name": "Skin", "kind": "MODIFIER", "type": 'SKIN', "icon": 'MOD_SKIN'},
    'pin_solidify': {"name": "Solidify", "kind": "MODIFIER", "type": 'SOLIDIFY', "icon": 'MOD_SOLIDIFY'},
    'pin_subsurf': {"name": "Subdivision Surface", "kind": "MODIFIER", "type": 'SUBSURF', "icon": 'MOD_SUBSURF'},
    'pin_triangulate': {"name": "Triangulate", "kind": "MODIFIER", "type": 'TRIANGULATE', "icon": 'MOD_TRIANGULATE'},
    'pin_volume_to_mesh': {"name": "Volume to Mesh", "kind": "MODIFIER", "type": 'VOLUME_TO_MESH', "icon": 'VOLUME_DATA'},
    'pin_weld': {"name": "Weld", "kind": "MODIFIER", "type": 'WELD', "icon": 'AUTOMERGE_OFF'},
    'pin_wireframe': {"name": "Wireframe", "kind": "MODIFIER", "type": 'WIREFRAME', "icon": 'MOD_WIREFRAME'},
    
    # --- DEFORM SECTION ---
    'pin_armature': {"name": "Armature", "kind": "MODIFIER", "type": 'ARMATURE', "icon": 'MOD_ARMATURE'},
    'pin_cast': {"name": "Cast", "kind": "MODIFIER", "type": 'CAST', "icon": 'MOD_CAST'},
    'pin_curve': {"name": "Curve", "kind": "MODIFIER", "type": 'CURVE', "icon": 'MOD_CURVE'},
    'pin_displace': {"name": "Displace", "kind": "MODIFIER", "type": 'DISPLACE', "icon": 'MOD_DISPLACE'},
    'pin_hook': {"name": "Hook", "kind": "MODIFIER", "type": 'HOOK', "icon": 'HOOK'},
    'pin_laplaciandeform': {"name": "Laplacian Deform", "kind": "MODIFIER", "type": 'LAPLACIANDEFORM', "icon": 'MOD_MESHDEFORM'},
    'pin_lattice': {"name": "Lattice", "kind": "MODIFIER", "type": 'LATTICE', "icon": 'MOD_LATTICE'},
    'pin_mesh_deform': {"name": "Mesh Deform", "kind": "MODIFIER", "type": 'MESH_DEFORM', "icon": 'MOD_MESHDEFORM'},
    'pin_shrinkwrap': {"name": "Shrinkwrap", "kind": "MODIFIER", "type": 'SHRINKWRAP', "icon": 'MOD_SHRINKWRAP'},
    'pin_simple_deform': {"name": "Simple Deform", "kind": "MODIFIER", "type": 'SIMPLE_DEFORM', "icon": 'MOD_SIMPLEDEFORM'},
    'pin_smooth': {"name": "Smooth", "kind": "MODIFIER", "type": 'SMOOTH', "icon": 'MOD_SMOOTH'},
    'pin_corrective_smooth': {"name": "Smooth Corrective", "kind": "MODIFIER", "type": 'CORRECTIVE_SMOOTH', "icon": 'MOD_SMOOTH'},
    'pin_laplaciansmooth': {"name": "Smooth Laplacian", "kind": "MODIFIER", "type": 'LAPLACIANSMOOTH', "icon": 'MOD_SMOOTH'},
    'pin_surface_deform': {"name": "Surface Deform", "kind": "MODIFIER", "type": 'SURFACE_DEFORM', "icon": 'MOD_MESHDEFORM'},
    'pin_warp': {"name": "Warp", "kind": "MODIFIER", "type": 'WARP', "icon": 'MOD_WARP'},
    'pin_wave': {"name": "Wave", "kind": "MODIFIER", "type": 'WAVE', "icon": 'MOD_WAVE'},
    
    # --- NORMALS SECTION ---
    'pin_normal_edit': {"name": "Normal Edit", "kind": "MODIFIER", "type": 'NORMAL_EDIT', "icon": 'MOD_NORMALEDIT'},
    'pin_weighted_normal': {"name": "Weighted Normal", "kind": "MODIFIER", "type": 'WEIGHTED_NORMAL', "icon": 'MOD_NORMALEDIT'},
    'pin_smooth_by_angle': {"name": "Smooth by Angle", "kind": "NODES", "node_group": "Smooth by Angle", "icon": 'GEOMETRY_NODES'},
    
    # --- PHYSICS SECTION ---
    'pin_cloth': {"name": "Cloth", "kind": "MODIFIER", "type": 'CLOTH', "icon": 'MOD_CLOTH'},
    'pin_collision': {"name": "Collision", "kind": "MODIFIER", "type": 'COLLISION', "icon": 'MOD_PHYSICS'},
    'pin_dynamic_paint': {"name": "Dynamic Paint", "kind": "MODIFIER", "type": 'DYNAMIC_PAINT', "icon": 'MOD_DYNAMICPAINT'},
    'pin_explode': {"name": "Explode", "kind": "MODIFIER", "type": 'EXPLODE', "icon": 'MOD_EXPLODE'},
    'pin_fluid': {"name": "Fluid", "kind": "MODIFIER", "type": 'FLUID', "icon": 'MOD_FLUIDSIM'},
    'pin_ocean': {"name": "Ocean", "kind": "MODIFIER", "type": 'OCEAN', "icon": 'MOD_OCEAN'},
    'pin_particle_instance': {"name": "Particle Instance", "kind": "MODIFIER", "type": 'PARTICLE_INSTANCE', "icon": 'MOD_PARTICLE_INSTANCE'},
    'pin_particle_system': {"name": "Particle System", "kind": "MODIFIER", "type": 'PARTICLE_SYSTEM', "icon": 'MOD_PARTICLES'},
    'pin_soft_body': {"name": "Soft Body", "kind": "MODIFIER", "type": 'SOFT_BODY', "icon": 'MOD_SOFT'},
}

def get_config_path():
    config_dir = bpy.utils.user_resource('CONFIG')
    return os.path.join(config_dir, "pinned_modifiers.json")

def load_settings():
    path = get_config_path()
    if os.path.exists(path):
        try:
            with open(path, 'r') as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def deferred_save():
    """Timer callback to execute the file write once (trailing-edge debounce)."""
    addon_prefs = bpy.context.preferences.addons.get(__name__)
    if not addon_prefs:
        return None

    prefs = addon_prefs.preferences
    path = get_config_path()
    settings = {key: getattr(prefs, key) for key in AVAILABLE_MODIFIERS.keys()}
    settings['pinned_order'] = getattr(prefs, "pinned_order", "")
    settings['show_settings_button'] = getattr(prefs, "show_settings_button", True)

    try:
        with open(path, 'w') as f:
            json.dump(settings, f, indent=4)
    except Exception as e:
        print(f"Pinned Modifiers Addon: Could not save preferences: {e}")
    # Return None so the timer does not repeat
    return None

def save_settings(self, context):
    """Property update callback with trailing-edge debounce (defined timer after last change)."""
    if getattr(self, "is_initial_loading", False):
        return
    # Cancel any pending save and schedule a new one
    if bpy.app.timers.is_registered(deferred_save):
        bpy.app.timers.unregister(deferred_save)

    bpy.app.timers.register(deferred_save, first_interval=0.5)

def make_prop(prop_name, default_val):
    return bpy.props.BoolProperty(name=prop_name, default=default_val, update=save_settings)


# --- EXPORT / IMPORT / RESET / PREFS OPERATORS ---

class PINNEDMODIFIERS_OT_export_settings(bpy.types.Operator, ExportHelper):
    bl_idname = "pinned_modifiers.export_settings"
    bl_label = "Export Config"
    bl_description = "Export current pinned modifiers configuration to a JSON file"
    filepath: bpy.props.StringProperty(subtype='FILE_PATH')
    filename_ext = ".json"
    filter_glob: bpy.props.StringProperty(default="*.json", options={'HIDDEN'})

    def invoke(self, context, event):
        if bpy.data.is_saved:
            base_dir = os.path.dirname(bpy.data.filepath)
        else:
            base_dir = os.path.expanduser("~")
            
        self.filepath = os.path.join(base_dir, "pinned_modifiers.json")
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

    def execute(self, context):
        prefs = context.preferences.addons[__name__].preferences
        settings = {key: getattr(prefs, key) for key in AVAILABLE_MODIFIERS.keys()}
        settings['pinned_order'] = getattr(prefs, 'pinned_order', '')
        settings['show_settings_button'] = getattr(prefs, 'show_settings_button', True)
        try:
            with open(self.filepath, 'w') as f:
                json.dump(settings, f, indent=4)
            self.report({'INFO'}, f"Successfully exported to {self.filepath}")
        except Exception as e:
            self.report({'ERROR'}, f"Failed to export: {e}")
        return {'FINISHED'}

class PINNEDMODIFIERS_OT_import_settings(bpy.types.Operator, ImportHelper):
    bl_idname = "pinned_modifiers.import_settings"
    bl_label = "Import Config"
    bl_description = "Import pinned modifiers configuration from a JSON file"
    filename_ext = ".json"
    filter_glob: bpy.props.StringProperty(default="*.json", options={'HIDDEN'})

    def execute(self, context):
        prefs = context.preferences.addons[__name__].preferences
        try:
            with open(self.filepath, 'r') as f:
                settings = json.load(f)

            for key, val in settings.items():
                if hasattr(prefs, key):
                    setattr(prefs, key, val)
                    
            self.report({'INFO'}, f"Successfully imported from {self.filepath}")
        except Exception as e:
            self.report({'ERROR'}, f"Failed to import: {e}")
            
        return {'FINISHED'}

class PINNEDMODIFIERS_OT_reset_settings(bpy.types.Operator):
    bl_idname = "pinned_modifiers.reset_settings"
    bl_label = "Reset to Defaults"
    bl_description = "Restore all pinned modifiers to their default configuration"

    def invoke(self, context, event):
        return context.window_manager.invoke_confirm(self, event)

    def execute(self, context):
        prefs = context.preferences.addons[__name__].preferences
        try:
            for key in AVAILABLE_MODIFIERS.keys():
                default_val = prefs.bl_rna.properties[key].default
                setattr(prefs, key, default_val)
            
            prefs.pinned_order = prefs.bl_rna.properties["pinned_order"].default
            prefs.show_settings_button = prefs.bl_rna.properties["show_settings_button"].default
                
            self.report({'INFO'}, "Configuration reset to defaults")
        except Exception as e:
            self.report({'ERROR'}, f"Failed to reset: {e}")

        return {'FINISHED'}

class PINNEDMODIFIERS_OT_open_prefs(bpy.types.Operator):
    bl_idname = "pinned_modifiers.open_prefs"
    bl_label = "Pinned Modifiers Settings..."
    bl_description = "Open the preferences to add, remove, or reorder pinned modifiers"

    def execute(self, context):
        bpy.ops.screen.userpref_show('INVOKE_DEFAULT')
        bpy.context.preferences.active_section = 'ADDONS'
        bpy.ops.preferences.addon_expand(module=__name__)
        bpy.ops.preferences.addon_show(module=__name__)
        return {'FINISHED'}


# --- ACTION OPERATORS ---

class PINNEDMODIFIERS_OT_add_pinned(bpy.types.Operator):
    bl_idname = "pinned_modifiers.add_pinned"
    bl_label = "Add Pinned Modifier"
    bl_description = "Adds the selected modifier to the active object"
    
    item_key: bpy.props.StringProperty()
    
    def execute(self, context):
        obj = context.object
        if not obj:
            self.report({'WARNING'}, "No active object selected")
            return {'CANCELLED'}
            
        item = AVAILABLE_MODIFIERS.get(self.item_key)
        if not item:
            return {'CANCELLED'}
            
        if item["kind"] == "MODIFIER":
            bpy.ops.object.modifier_add(type=item["type"])
            
        elif item["kind"] == "NODES":
            ng_name = item.get("node_group")
            
            # Check if it already exists in the local file memory
            ng = bpy.data.node_groups.get(ng_name)
            
            if ng:
                # Local assignment
                mod = obj.modifiers.new(name=item["name"], type='NODES')
                mod.node_group = ng
            else:
                # Fallback: Dictionary for Blender 5.1 Essentials paths
                # Format: "nodes/geometry_nodes_essentials.blend/NodeTree/Asset Name"
                essential_paths = {
                    "Curve to Tube": "nodes/geometry_nodes_essentials.blend/NodeTree/Curve to Tube",
                    "Scatter on Surface": "nodes/geometry_nodes_essentials.blend/NodeTree/Scatter on Surface",
                    "Array": "nodes/geometry_nodes_essentials.blend/NodeTree/Array",
                    "Smooth by Angle": "nodes/geometry_nodes_essentials.blend/NodeTree/Smooth by Angle"
                }
                
                asset_path = essential_paths.get(ng_name)
                
                if asset_path:
                    try:
                        # Forward slashes are safe on both Windows and Linux in Blender Python
                        bpy.ops.object.modifier_add_node_group(
                            asset_library_type="ESSENTIALS", 
                            asset_library_identifier="", 
                            relative_asset_identifier=asset_path
                        )
                    except Exception as e:
                        self.report({'ERROR'}, f"Could not load asset. Internal error: {e}")
                        return {'CANCELLED'}
                else:
                    self.report({'WARNING'}, f"Node Group '{ng_name}' missing and not found in Essentials path dictionary!")
                    return {'CANCELLED'}
                
        return {'FINISHED'}

class PINNEDMODIFIERS_OT_move_item(bpy.types.Operator):
    bl_idname = "pinned_modifiers.move_item"
    bl_label = "Move Pinned Modifier"
    bl_description = "Move this modifier up, down, to top, or to bottom in the pinned list"
    
    item_key: bpy.props.StringProperty()
    direction: bpy.props.StringProperty() # 'UP', 'DOWN', 'TOP', 'BOTTOM'
    
    def execute(self, context):
        prefs = context.preferences.addons[__name__].preferences
        
        active = [k for k in AVAILABLE_MODIFIERS.keys() if getattr(prefs, k)]
        order = [k for k in prefs.pinned_order.split(',') if k]
        
        final_order = []
        for k in order:
            if k in active:
                final_order.append(k)
        for k in active:
            if k not in final_order:
                final_order.append(k)
                
        if self.item_key not in final_order:
            return {'CANCELLED'}
            
        idx = final_order.index(self.item_key)
        
        if self.direction == 'UP' and idx > 0:
            final_order[idx], final_order[idx-1] = final_order[idx-1], final_order[idx]
        elif self.direction == 'DOWN' and idx < len(final_order) - 1:
            final_order[idx], final_order[idx+1] = final_order[idx+1], final_order[idx]
        elif self.direction == 'TOP' and idx > 0:
            item = final_order.pop(idx)
            final_order.insert(0, item)
        elif self.direction == 'BOTTOM' and idx < len(final_order) - 1:
            item = final_order.pop(idx)
            final_order.append(item)
            
        prefs.pinned_order = ','.join(final_order)
        
        for area in context.screen.areas:
            if area.type == 'PREFERENCES':
                area.tag_redraw()
                
        return {'FINISHED'}

# --- ADDON PREFERENCES UI ---

class PinnedModifiersPreferences(bpy.types.AddonPreferences):
    bl_idname = __name__

    pinned_order: bpy.props.StringProperty(
        default="pin_array,pin_bevel,pin_boolean,pin_mirror,pin_subsurf,pin_weld",
        update=save_settings
    )
    
    show_settings_button: bpy.props.BoolProperty(
        name="Show Settings Button in Menu",
        description="Show the 'Pinned Modifiers Settings...' button at the bottom of the Add Modifier menu",
        default=True,
        update=save_settings
    )

    # --- EDIT SECTION ---
    pin_data_transfer: make_prop("Data Transfer", False)
    pin_mesh_cache: make_prop("Mesh Cache", False)
    pin_mesh_sequence_cache: make_prop("Mesh Sequence Cache", False)
    pin_uv_project: make_prop("UV Project", False)
    pin_uv_warp: make_prop("UV Warp", False)
    pin_vertex_weight_edit: make_prop("Vertex Weight Edit", False)
    pin_vertex_weight_mix: make_prop("Vertex Weight Mix", False)
    pin_vertex_weight_proximity: make_prop("Vertex Weight Proximity", False)
    
    # --- GENERATE SECTION ---
    pin_array: make_prop("Array", True)
    pin_array_legacy: make_prop("Array (Legacy)", False)
    pin_bevel: make_prop("Bevel", True)
    pin_boolean: make_prop("Boolean", True)
    pin_build: make_prop("Build", False)
    pin_curve_to_tube: make_prop("Curve to Tube", False)
    pin_decimate: make_prop("Decimate", False)
    pin_edge_split: make_prop("Edge Split", False)
    pin_mask: make_prop("Mask", False)
    pin_mirror: make_prop("Mirror", True)
    pin_multires: make_prop("Multiresolution", False)
    pin_remesh: make_prop("Remesh", False)
    pin_scatter_on_surface: make_prop("Scatter on Surface", False)
    pin_screw: make_prop("Screw", False)
    pin_skin: make_prop("Skin", False)
    pin_solidify: make_prop("Solidify", False)
    pin_subsurf: make_prop("Subdivision Surface", True)
    pin_triangulate: make_prop("Triangulate", False)
    pin_volume_to_mesh: make_prop("Volume to Mesh", False)
    pin_weld: make_prop("Weld", True)
    pin_wireframe: make_prop("Wireframe", False)
    
    # --- DEFORM SECTION ---
    pin_armature: make_prop("Armature", False)
    pin_cast: make_prop("Cast", False)
    pin_curve: make_prop("Curve", False)
    pin_displace: make_prop("Displace", False)
    pin_hook: make_prop("Hook", False)
    pin_laplaciandeform: make_prop("Laplacian Deform", False)
    pin_lattice: make_prop("Lattice", False)
    pin_mesh_deform: make_prop("Mesh Deform", False)
    pin_shrinkwrap: make_prop("Shrinkwrap", False)
    pin_simple_deform: make_prop("Simple Deform", False)
    pin_smooth: make_prop("Smooth", False)
    pin_corrective_smooth: make_prop("Smooth Corrective", False)
    pin_laplaciansmooth: make_prop("Smooth Laplacian", False)
    pin_surface_deform: make_prop("Surface Deform", False)
    pin_warp: make_prop("Warp", False)
    pin_wave: make_prop("Wave", False)
    
    # --- NORMALS SECTION ---
    pin_normal_edit: make_prop("Normal Edit", False)
    pin_weighted_normal: make_prop("Weighted Normal", False)
    pin_smooth_by_angle: make_prop("Smooth by Angle", False)
    
    # --- PHYSICS SECTION ---
    pin_cloth: make_prop("Cloth", False)
    pin_collision: make_prop("Collision", False)
    pin_dynamic_paint: make_prop("Dynamic Paint", False)
    pin_explode: make_prop("Explode", False)
    pin_fluid: make_prop("Fluid", False)
    pin_ocean: make_prop("Ocean", False)
    pin_particle_instance: make_prop("Particle Instance", False)
    pin_particle_system: make_prop("Particle System", False)
    pin_soft_body: make_prop("Soft Body", False)

    def draw(self, context):
        layout = self.layout
        config_path = get_config_path()
        box = layout.box()
        box.label(text=f"Settings are permanently saved to: {config_path}", icon='INFO')
        
        row = box.row()
        row.operator("pinned_modifiers.export_settings", text="Export", icon='EXPORT')
        row.operator("pinned_modifiers.import_settings", text="Import", icon='IMPORT')
        row.operator("pinned_modifiers.reset_settings", text="Reset Defaults", icon='FILE_REFRESH')
        
        layout.separator()
        
        # --- MODIFIERS CATEGORIES SEPARATION ---
        keys = list(AVAILABLE_MODIFIERS.keys())
        
        # Slicing the keys based on the order of AVAILABLE_MODIFIERS
        categories = {
            "Edit": keys[0:8],
            "Generate": keys[8:29],
            "Deform": keys[29:45],
            "Normals": keys[45:48],
            "Physics": keys[48:]
        }
        
        for cat_name, cat_keys in categories.items():
            # Add a section label for the category
            layout.label(text=f"{cat_name}", icon='DOT')
            
            grid_row = layout.row()
            cols = [grid_row.column() for _ in range(4)]
            
            # Calculate how many items fit in each column for this specific category
            items_per_col = (len(cat_keys) + 3) // 4
            
            for i, key in enumerate(cat_keys):
                # Ensure we don't go out of bounds if distribution is slightly uneven
                col_index = min(i // items_per_col, 3) 
                target_col = cols[col_index]
                
                icon_string = AVAILABLE_MODIFIERS[key]["icon"]
                target_col.prop(self, key, icon=icon_string)
                
            layout.separator()
            
        layout.separator()
        layout.prop(self, "show_settings_button", icon='PREFERENCES')
        layout.separator()
        
        # --- REORDER PINNED MODIFIERS ---
        active = [k for k in keys if getattr(self, k)]
        order = [k for k in self.pinned_order.split(',') if k]
        
        final_order = []
        for k in order:
            if k in active:
                final_order.append(k)
        for k in active:
            if k not in final_order:
                final_order.append(k)
                
        if final_order:
            layout.label(text="Reorder Pinned Modifiers:")
            reorder_box = layout.box()
            
            for idx, key in enumerate(final_order):
                row = reorder_box.row(align=True)
                name = AVAILABLE_MODIFIERS[key]["name"]
                icon_string = AVAILABLE_MODIFIERS[key]["icon"]
                
                if idx < len(final_order) - 1:
                    bot_btn = row.operator("pinned_modifiers.move_item", text="", icon='TRIA_DOWN_BAR')
                    bot_btn.item_key = key
                    bot_btn.direction = 'BOTTOM'
                else:
                    row.label(text="", icon='BLANK1')
                    
                if idx > 0:
                    top_btn = row.operator("pinned_modifiers.move_item", text="", icon='TRIA_UP_BAR')
                    top_btn.item_key = key
                    top_btn.direction = 'TOP'
                else:
                    row.label(text="", icon='BLANK1')
                    
                if idx < len(final_order) - 1:
                    down_btn = row.operator("pinned_modifiers.move_item", text="", icon='TRIA_DOWN')
                    down_btn.item_key = key
                    down_btn.direction = 'DOWN'
                else:
                    row.label(text="", icon='BLANK1')
                    
                if idx > 0:
                    up_btn = row.operator("pinned_modifiers.move_item", text="", icon='TRIA_UP')
                    up_btn.item_key = key
                    up_btn.direction = 'UP'
                else:
                    row.label(text="", icon='BLANK1')
                
                row.label(text=name, icon=icon_string)
                    
            layout.separator()
        
        # --- SUPPORT & LINKS SECTION ---
        support_box = layout.box()
        header_row = support_box.row()
        header_row.alignment = 'CENTER'
        header_row.label(text="If this add-on saves you time, please consider supporting its development!", icon='HEART')
        
        support_box.separator()
        support_row = support_box.row(align=True)
        support_row.scale_y = 1.2  
        
        support_row.operator("wm.url_open", text="Libera Pay", icon='FUND').url = "https://liberapay.com/FraYoshi"
        support_row.operator("wm.url_open", text="Ko-Fi", icon='FUND').url = "https://ko-fi.com/frayoshi"
        support_row.operator("wm.url_open", text="More Ways to Support", icon='URL').url = "https://furayoshi.com/support"
        
        links_row = support_box.row(align=True)
        links_row.operator("wm.url_open", text="Source Code & Issues", icon='HELP').url = "https://github.com/FraYoshi/blender-pinned-modifiers"
        links_row.operator("wm.url_open", text="Discord invite", icon='COMMUNITY').url = "https://furayoshi.com/discord"
        links_row.operator("wm.url_open", text="Homepage (furayoshi.com)", icon='WORLD_DATA').url = "https://furayoshi.com"


# --- MENU INJECTION & REGISTRATION ---

def draw_pinned_modifiers_top(self, context):
    layout = self.layout
    prefs = context.preferences.addons[__name__].preferences
    
    active = [k for k in AVAILABLE_MODIFIERS.keys() if getattr(prefs, k)]
    order = [k for k in prefs.pinned_order.split(',') if k]
    
    final_order = []
    for k in order:
        if k in active:
            final_order.append(k)
    for k in active:
        if k not in final_order:
            final_order.append(k)
            
    if final_order:
        for key in final_order:
            item = AVAILABLE_MODIFIERS[key]
            op = layout.operator("pinned_modifiers.add_pinned", text=item["name"], icon=item["icon"])
            op.item_key = key
            
        layout.separator()

def draw_pinned_modifiers_bottom(self, context):
    prefs = context.preferences.addons[__name__].preferences
    if getattr(prefs, "show_settings_button", True):
        layout = self.layout
        layout.separator()
        layout.operator("pinned_modifiers.open_prefs", icon='PREFERENCES')


classes = (
    PINNEDMODIFIERS_OT_export_settings,
    PINNEDMODIFIERS_OT_import_settings,
    PINNEDMODIFIERS_OT_reset_settings,
    PINNEDMODIFIERS_OT_open_prefs,
    PINNEDMODIFIERS_OT_add_pinned,
    PINNEDMODIFIERS_OT_move_item,
    PinnedModifiersPreferences,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    
    bpy.types.OBJECT_MT_modifier_add.prepend(draw_pinned_modifiers_top)
    bpy.types.OBJECT_MT_modifier_add.append(draw_pinned_modifiers_bottom)
    
    try:
        prefs = bpy.context.preferences.addons[__name__].preferences
        prefs.is_initial_loading = True 
        
        saved_settings = load_settings()
        for key, val in saved_settings.items():
            if hasattr(prefs, key):
                setattr(prefs, key, val)
    except Exception:
        pass
    finally:
        if 'prefs' in locals():
            prefs.is_initial_loading = False

def unregister():
    bpy.types.OBJECT_MT_modifier_add.remove(draw_pinned_modifiers_top)
    bpy.types.OBJECT_MT_modifier_add.remove(draw_pinned_modifiers_bottom)
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()
