package components

var HotkeysTomlString string = `# Here is global, all global key cant conflicts with other hotkeys
quit = ['esc', 'q']
# 
list_up = ['up', 'k']
list_down = ['down', 'j']
# 
pinned_directory = ['ctrl+p', '']
# 
close_file_panel = ['ctrl+w', '']
create_new_file_panel = ['ctrl+n', '']
# 
next_file_panel = ['tab', 'L']
previous_file_panel = ['shift+left', 'H']
focus_on_process_bar = ['p', '']
focus_on_side_bar = ['b', '']
focus_on_meta_data = ['m', '']
# 
change_panel_mode = ['v', '']
# 
file_panel_directory_create = ['f', '']
file_panel_file_create = ['c', '']
file_panel_item_rename = ['r', '']
paste_item = ['ctrl+v', '']
extract_file = ['ctrl+e', '']
compress_file = ['ctrl+r', '']
toggle_dot_file = ['ctrl+h', '']
# 
oepn_file_with_editor = ['e', '']
open_current_directory_with_editor = ['E', '']
# 
# These hotkeys do not conflict with any other keys (including global hotkey)
cancel = ['ctrl+c', 'esc']
confirm = ['enter', '']
# 
# Here is normal mode hotkey you can conflicts with other mode (cant conflicts with global hotkey)
delete_item = ['ctrl+d', '']
select_item = ['enter', 'l']
parent_directory = ['h', 'backspace']
copy_single_item = ['ctrl+c', '']
cut_single_item = ['ctrl+x', '']
search_bar = ['ctrl+f', '']
# 
# Here is select mode hotkey you can conflicts with other mode (cant conflicts with global hotkey)
file_panel_select_mode_item_single_select = ['enter', 'l']
file_panel_select_mode_item_select_down = ['shift+down', 'J']
file_panel_select_mode_item_select_up = ['shift+up', 'K']
file_panel_select_mode_item_delete = ['ctrl+d', 'delete']
file_panel_select_mode_item_copy = ['ctrl+c', '']
file_panel_select_mode_item_cut = ['ctrl+x', '']
file_panel_select_all_item = ['ctrl+a', '']
`

var ConfigTomlString string = `# change your theme
theme = 'catpuccin'
# 
# useless for now
footer_panel_list = ['processessssssssssss', 'metadata', 'clipboard']
# 
# ==========PLUGINS========== #
# 
# Show more detailed metadata, please install exiftool before enabling this plugin!
metadata = false
`