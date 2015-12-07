import bpy, re

# アドオン情報
bl_info = {
	"name" : "Unconfirmable Delete",
	"author" : "@saidenka",
	"version" : (0, 1),
	"blender" : (2, 7),
	"location" : "Delete Keys (X key)",
	"description" : "Delete keys replaced non confirm delete operations",
	"warning" : "",
	"wiki_url" : "",
	"tracker_url" : "",
	"category" : "Custom"
}

# メインオペレーター
class unconfirmable_delete(bpy.types.Operator):
	bl_idname = 'wm.unconfirmable_delete'
	bl_label = "Unconfirmable Delete"
	bl_description = "Delete keys replaced non confirm delete operations"
	bl_options = {'REGISTER', 'UNDO'}
	
	command = bpy.props.StringProperty(name="Command")
	
	def execute(self, context):
		try:
			exec("bpy.ops.%s()" % self.command)
		except:
			self.report(type={'ERROR'}, message="Failed remove")
			return {'CANCELLED'}
		return {'FINISHED'}

# グローバル変数
is_shortcuted = False
addon_shortcuts = []

# ショートカットを上書き
def overwrite_keys():
	global is_shortcuted, addon_shortcuts
	if is_shortcuted: return
	
	addon_keyconfig = bpy.context.window_manager.keyconfigs.addon
	for keymap in bpy.context.window_manager.keyconfigs.active.keymaps:
		
		if keymap.name in addon_keyconfig.keymaps.keys():
			addon_keymap = addon_keyconfig.keymaps[keymap.name]
		else:
			addon_keymap = addon_keyconfig.keymaps.new(name=keymap.name, space_type=keymap.space_type, modal=keymap.is_modal)
		
		addon_shortcuts.append((addon_keymap, []))
		
		for keymap_item in keymap.keymap_items:
			
			if re.search('\.(delete)$', keymap_item.idname):
				
				addon_keymap_item = addon_keymap.keymap_items.new('wm.unconfirmable_delete', keymap_item.type, 'PRESS', head=True)
				addon_keymap_item.properties.command = keymap_item.idname
				
				addon_shortcuts[-1][1].append(addon_keymap_item)
	
	is_shortcuted = True

# ヘッダーメニューの描画が更新されたら実行
def menu_func(self, context):
	overwrite_keys()

# アドオンを有効にしたときの処理
def register():
	# オペレーターなどを登録
	bpy.utils.register_module(__name__)
	# ヘッダーメニューに項目追加
	bpy.types.INFO_HT_header.append(menu_func)
	# 和訳を登録
	translation_dict = {'ja_JP': {('*', "Unconfirmable Delete"):"確認せず削除", ('*', "Delete Keys (X key)"):"削除キー (X Delete など)", ('*', "Delete keys replaced non confirm delete operations"):"削除キーを確認メッセージのないものに差し替えます", ('*', "Failed remove"):"削除に失敗しました"}}
	bpy.app.translations.register(__name__, translation_dict)

# アドオンを無効にしたときの処理
def unregister():
	global is_shortcuted, addon_shortcuts
	# オペレーターなどを解除
	bpy.utils.unregister_module(__name__)
	# ヘッダーメニューの項目解除
	bpy.types.INFO_HT_header.remove(menu_func)
	# ショートカットの解除
	for addon_keymap, addon_keymap_items in addon_shortcuts:
		for addon_keymap_item in addon_keymap_items:
			addon_keymap.keymap_items.remove(addon_keymap_item)
	# グローバル変数の初期化
	is_shortcuted = False
	addon_shortcuts = []
	# 和訳を解除
	bpy.app.translations.unregister(__name__)

# このスクリプトを単独で実行した時に実行
if __name__ == '__main__':
	register()
