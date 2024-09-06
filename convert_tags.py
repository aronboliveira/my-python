import os
import sys
import time
import json
import re
from colorama import Fore, Style
def walk_dir(dirp) -> None:
  file_acc = 0
  dir_acc = 0
  no_files = True
  no_match_files = True
  for root, _, files in os.walk(dirp, onerror=lambda err: print(Fore.RED + f'Error acessing directory when checking for any files: {err}' + Style.RESET_ALL)):
    if files:
      no_files = False
      break
  if no_files:
    print (Fore.RED + 'No files found.' + Style.RESET_ALL)
    return
  for root, _, files in os.walk(dirp, onerror=lambda err: print(Fore.RED + f'Error acessing directory when checking for matching files: {err}' + Style.RESET_ALL)):
    print(f'Reading ${root}...')
    dir_acc += 1
    matched_files = [file for file in files if file.endswith(('.jsx', '.tsx', '.vue', '.html'))]
    if matched_files:
      no_match_files = False
    if no_match_files:
      print(Fore.RED + 'No matching files found.' + Style.RESET_ALL)
      return
    for file in matched_files:
      file_acc += 1
      check_tags(os.path.join(root, file))
  print(f'Finished reading ${file_acc} files in ${dir_acc} directories from ${dirp}.')
def check_tags(path) -> None:
    try:
        with open(path, 'r', encoding='utf-8', errors='replace') as file:
            content = file.read()
            if not content or content == '':
                raise ValueError(f'No string in the content.')
        
        tags = re.findall(re.compile(r'</?\n?[a-zA-Z]+[.]*[\n\s]*/?>', flags=(re.MULTILINE)), content)
        if not tags:
            raise ValueError(f"No tags found in file: {path}")
        
        file_name, file_ext = os.path.splitext(os.path.basename(path))
        outp = os.path.join(os.path.dirname(path), f'{os.path.basename(os.path.dirname(path))}-rn')
        os.makedirs(outp, exist_ok=True)
        replacements_json_path = os.path.join(outp, 'replacements-rn.json')
        
        if os.path.exists(replacements_json_path):
            with open(replacements_json_path, 'r', encoding='utf-8') as json_file:
                replacements = json.load(json_file)
        else:
            replacements = {}
        
        if file_ext in ['.jsx', '.tsx']:
            replacement_styles = os.path.join(outp, f'replaced_styles{file_ext[:1]}')
            replacement_content = f'''import {{ StyleSheet }} from "react-native";
							const styles = StyleSheet.create({{
									b: {{
											fontWeight: 'bold',
									}},
									bdo__ltr: {{
											writingDirection: 'ltr',
									}},
									bdo__rtl: {{
											writingDirection: 'rtl',
									}},
									big: {{
											fontSize: 20,
									}},
									br: {{
											lineHeight: 1.5,
									}},
									center: {{
											textAlign: 'center',
									}},
									cite: {{
											fontStyle: 'italic',
									}},
									code: {{
											fontFamily: 'monospace',
									}},
									del: {{
											textDecorationLine: 'line-through',
									}},
									dfn: {{
											fontStyle: 'italic',
									}},
									h1: {{
											fontSize: 32,
											fontWeight: 'bold',
									}},
									h2: {{
											fontSize: 28,
											fontWeight: 'bold',
									}},
									h3: {{
											fontSize: 24,
											fontWeight: 'bold',
									}},
									h4: {{
											fontSize: 20,
											fontWeight: 'bold',
									}},
									h5: {{
											fontSize: 18,
											fontWeight: 'bold',
									}},
									h6: {{
											fontSize: 16,
											fontWeight: 'bold',
									}},
									hr: {{
											marginTop: 8,
											marginBottom: 8,
									}},
									ins: {{
											textDecorationLine: 'underline'
									}},
									kbd: {{
											fontFamily: 'monospace',
											backgroundColor: '#ddd',
											paddingTop: 2,
											paddingRight: 2,
											paddingBottom: 2,
											paddingLeft: 2,
									}},
									mark: {{
											backgroundColor: 'yellow',
									}},
									pre: {{
											fontFamily: 'monospace',
									}},
									s: {{
											textDecorationLine: 'line-through',
									}},
									samp: {{
											fontFamily: 'monospace',
									}},
									small: {{
											fontSize: 12,
									}},
									strike: {{
											textDecorationLine: 'line-through',
									}},
									strong: {{
											fontWeight: 'bold',
									}},
									sub: {{
											fontSize: 12,
											verticalAlign: 'bottom',
									}},
									super: {{
											fontSize: 12,
											verticalAlign: 'top',
									}},
									u: {{
											textDecorationLine: 'underline',
									}},
									wbr: {{
											fontSize: 9,
											lineHeight: 1.5,
									}},
									//last-flag
							}})
							'''
											
        new_file_path = os.path.join(outp, f'{file_name}-rn{file_ext}')

        def check_imports(content: str, file_ext: str, main_imports: str = 'Text', lib='react-native') -> str:
            replaced_styles_pattern = r'import\s*{\s*replaced_styles\s*}\s*from\s*["\']\./replaced_styles\.(jsx|tsx|vue)["\'];?'
            main_imports_pattern = fr'import\s*{{\s*{main_imports}\s*}}\s*from\s*["\']{lib}["\'];?'
            if not re.search(replaced_styles_pattern, content, flags=re.MULTILINE):
                content = f'import {{ replaced_styles }} from "./replaced_styles{file_ext}";\n{content}'
            if not re.search(main_imports_pattern, content, flags=re.MULTILINE):
                content = f'import {{ {main_imports} }} from "{lib}";\n{content}'
            return content

        def replace_content(content: str, tag: str, case_tag: str, main_tag: str = 'Text', onPress: bool = False) -> str:
            press = ' onPress={() => {}}' if onPress else ''
            return content.replace(
                f'<{tag}>',
                f'<{main_tag} style={{replaced_styles.{case_tag}}}{press}>'
            ).replace(
                f'</{tag}>',
                f'</{main_tag}>'
            ).replace(
                f'<{tag} />',
                f'<{main_tag} style={{replaced_styles.{case_tag}}}{press} />'
            ).replace(
                f'<{tag}/>',
                f'<{main_tag} style={{replaced_styles.{case_tag}}}{press}/>'
            )

        for tag in set(tags):
            tag_classes = []
            tag_id = ''
            tag_parts = re.sub(r'[<>\n]', repl='', string=tag, flags=re.MULTILINE).split()
            tag_name = tag_parts[0] if len(tag_parts) > 0 else 0
            tag_selectors = f'{{replaced_styles.{tag_name}}}'
            for part in tag_parts[1:]:
                if part.strip().startswith('class'):
                    tag_classes = [''.join(word.capialize() if i > 0 else word for i, word in enumerate(clas.split('-')))
                                   for clas in part[(part.index('=') + 1):].replace("'", '').replace('"', '').split(' ')]
                if part.strip().startswith('id'):
                    tag_id = part[(part.index('=') + 1):].replace("'", '').replace('"', '')
            if tag_id != '' or len(tag_classes) > 0:
                tag_selectors = f'{{[replaced_styles.{tag_name}]}}'
                for classEl in tag_classes:
                    tag_selectors = tag_selectors[:-3] + ',_' + classEl + ']}}'
                    replacement_content = replacement_content[:replacement_content.index('//last-flag')] + f'''
								_{classEl} {{}};
								//last-flag
								'''
                if tag_id != '':
                    tag_selectors = tag_selectors[:-3] + ',__' + tag_id + ']}}'
                    replacement_content = replacement_content[:replacement_content.index('//last-flag')] + f'''
								__{tag_id} {{}};
								//last-flag
								'''

            if tag_name == 'input' or tag_name == 'textarea':
                native_tag = '<TextInput'
                if tag_name == 'textarea':
                    native_tag = '<TextInput multiline={true}'
                elif tag_name == 'input':
                    inpType = 'text'
                    for part in tag_parts[1:]:
                        if part.strip().startswith('type'):
                            inpType = part[(part.index('=') + 1):].replace("'", '').replace('"', '')
                    if inpType == 'password':
                        native_tag = '<TextInput secureTextEntry={true}'
                    if inpType == 'email':
                        native_tag = '<TextInput keyboardType="email-address"'
                    if inpType == 'number':
                        native_tag = '<TextInput keyboardType="numeric"'
                    if inpType == 'tel':
                        native_tag = '<TextInput keyboardType="phone-pad"'
                    if inpType == 'url':
                        native_tag = '<TextInput keyboardType="url"'
                    if inpType == 'button' or inpType == 'submit' or inpType == 'reset':
                        native_tag = '<TouchableOpacity onPress={() => {}}'
                    if inpType == 'checkbox':
                        native_tag = '<Switch onPress={() => {}}'
                    if inpType == 'radio':
                        native_tag = '<RadioButton onPress={() => {}}'
                    if inpType == 'color':
                        native_tag = '<ColorPickerWheel onColorChangeComplete={() => {}}'
                    if inpType == 'date' or inpType == 'month':
                        native_tag = '<DatePicker date={} mode="date" placeholder="Select date" format="YYYY-MM-DD" confirmBtnText="Confirm" cancelBtnText="Cancel" onDateChange={() => {}}'
                    if inpType == 'datetime-local':
                        native_tag = '<DatePicker value={} mode="datetime" onChange={() => {}}'
                    if inpType == 'week':
                        native_tag = '<CalendarPicker onDateChange={() => {}}'
                    if inpType == 'time':
                        native_tag = '<DateTimePickerModal isVisible={} mode="time" onConfirm={() => {}} onCancel={() => {}}'
                    if inpType == 'file':
                        native_tag = '''<View>
												<Button title="Pick Document" onPress={() => {}} />
												<Button title="Pick Document onPress={() => {}} />
										</View>
										'''

            if tag_name == 'bdo':
                bdo_dir = 'ltr'
                for part in tag_parts[1:]:
                    if part == 'dir="rtl"':
                        bdo_dir = 'rtl'

            is_react = file_ext in ['.jsx', '.tsx']
            if tag_name in ['a', 'abbr', 'option']:
                if is_react:
                    content = check_imports(content, file_ext)
                replacements[tag_name] = 'Text__onPress'
                content = replace_content(content, tag, tag_name, onPress=True)
            elif tag_name in ['address', 'area', 'acronym', 'big', 'caption', 'code', 'del', 'dfn', 'output', 'em', 'font',
                              'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'i', 'label', 'mark', 'marquee', 'samp', 'nobr', 'output',
                              'param', 'plaintext', 'q', 'rb', 'rp', 'rt', 'rtc', 's', 'small', 'span', 'strike', 'strong', 'time',
                              'tt', 'u', 'var', 'xmp']:
                if is_react:
                    content = check_imports(content, file_ext)
                replacements[tag_name] = 'Text'
                content = replace_content(content, tag, tag_name)
            elif tag_name in ['article', 'aside', 'blockquote', 'body', 'br', 'center', 'dt', 'dd', 'fieldset', 'figcaption',
                              'figure', 'frameset', 'view', 'header', 'hgroup', 'hr', 'legend', 'li', 'main', 'nav', 'noembed',
                              'noframes', 'ol', 'optgroup', 'p', 'picture', 'portal', 'ruby', 'search', 'section', 'slot', 'summary',
                              'table', 'tbody', 'tfoot', 'td', 'th', 'thead', 'tr', 'track', 'ul', 'wbr']:
                if is_react:
                    content = check_imports(content, file_ext, 'View')
                replacements[tag_name] = 'View'
                content = replace_content(content, tag, tag_name, 'View')

            elif tag_name == 'bdo':
                if is_react:
                    content = check_imports(content, file_ext)
                replacements[tag_name] = 'Text__direction'
                content = content.replace(
                    f'<{tag}>',
                    f'<Text style={{[replaced_styles.{tag_name}, replaced_styles.{tag_name}__{bdo_dir}]}}>'
                ).replace(
                    f'</{tag}>',
                    '</Text>'
                ).replace(
                    f'<{tag} />',
                    f'<Text style={{[replaced_styles.{tag_name}, replaced_styles.{tag_name}__{bdo_dir}]}} />'
                ).replace(
                    f'<{tag}/>',
                    f'<Text style={{[replaced_styles.{tag_name}, replaced_styles.{tag_name}__{bdo_dir}]}}/>'
                )

            elif tag_name in ['button', 'details']:
                if is_react:
                    content = check_imports(content, file_ext, 'TouchableOpacity')
                replacements[tag_name] = 'TouchableOpacity'
                content = replace_content(content, tag, tag_name, main_tag='TouchableOpacity', onPress=True)

            elif tag_name in ['dialog', 'datalist']:
                if is_react:
                    content = check_imports(content, file_ext, 'Modal')
                replacements[tag_name] = 'Modal'
                content = replace_content(content, tag, tag_name, 'Modal', onPress=True)

            elif tag_name == 'dl':
                if is_react:
                    content = check_imports(content, file_ext, 'SectionList')
                replacements[tag_name] = 'SectionList'
                content = replace_content(content, tag, tag_name, 'SectionList')

            elif tag_name in ['menu', 'ol', 'ul']:
                if is_react:
                    content = check_imports(content, file_ext, 'FlatList')
                replacements[tag_name] = 'FlatList'
                content = replace_content(content, tag, tag_name, 'FlatList')

            elif tag_name == 'img':
                if is_react:
                    content = check_imports(content, file_ext, 'Image')
                replacements[tag_name] = 'Image'
                content = replace_content(content, tag, tag_name, 'Image')

            elif tag_name in ['input', 'textarea']:
                if native_tag.startswith('<TextInput'):
                    if is_react:
                        content = check_imports(content, file_ext)
                    if native_tag == 'textarea':
                        replacements[f'{tag_name}'] = 'TextInput__multiline'
                    elif re.search(r'secureTextEntry', native_tag):
                        replacement_content[f'{tag_name}__{native_tag}'] = 'TextInput__secureTextEntry'
                    elif re.search(r'keyboardType', native_tag):
                        if re.search(r'email', native_tag):
                            replacement_content[f'{tag_name}__{native_tag}'] = 'TextInput__email'
                        elif re.search(r'number', native_tag):
                            replacement_content[f'{tag_name}__{native_tag}'] = 'TextInput__number'
                        elif re.search(r'phone', native_tag):
                            replacement_content[f'{tag_name}__{native_tag}'] = 'TextInput__phone'
                elif native_tag.startswith('<TouchableOpacity'):
                    if is_react:
                        content = check_imports(content, file_ext, 'TouchableOpacity')
                    replacement_content[f'{tag_name}__{native_tag}'] = 'TouchableOpacity'
                elif native_tag.startswith('<Switch'):
                    if is_react:
                        content = check_imports(content, file_ext, 'Switch')
                    replacement_content[f'{tag_name}__{native_tag}'] = 'Switch'
                elif native_tag.startswith('<RadioButton'):
                    if is_react:
                        content = check_imports(content, file_ext, 'RadioButton', 'react-native-paper')
                    replacement_content[f'{tag_name}__{native_tag}'] = 'RadioButton'
                elif native_tag.startswith('<ColorPickerWheel'):
                    if is_react:
                        content = check_imports(content, file_ext, 'ColorPickerWheel', 'react-native-color-picker-wheel')
                    replacement_content[f'{tag_name}__{native_tag}'] = 'ColorPickerWheel'
                elif native_tag.startswith('<DatePicker'):
                    if is_react:
                        content = check_imports(content, file_ext, 'DatePicker', 'react-native-date-picker')
                    if re.search(r'datetime', native_tag):
                        replacement_content[f'{tag_name}__{native_tag}'] = 'DatePicker__datetime'
                    else:
                        replacement_content[f'{tag_name}__{native_tag}'] = 'DatePicker__date'
                elif native_tag.startswith('<CalendarPicker'):
                    if is_react:
                        content = check_imports(content, file_ext, 'CalendarPicker', 'react-native-calendar-picker')
                    replacement_content[f'{tag_name}__{native_tag}'] = 'CalendarPicker'
                elif native_tag.startswith('<DateTimePickerModal'):
                    if is_react:
                        content = check_imports(content, file_ext, 'DateTimePickerModal', 'react-native-modal-datetime-picker')
                    replacement_content[f'{tag_name}__{native_tag}'] = 'DateTimePickerModal'
                elif native_tag.startswith('<View'):
                    if is_react:
                        content = check_imports(content, file_ext, 'View')
                    replacement_content[f'{tag_name}__{native_tag}'] = 'View'
                if inpType == 'file':
                    content = content.replace(
												f'<{tag}>',
												f'<View style={{{{replaced_styles.{tag_name}}}}}><Button title="Pick Document" onPress={{() => {{}}}} /><Button title="Pick Document onPress={{() => {{}}}} />'
										).replace(
												f'</{tag}>',
												'</View>'
										).replace(
												f'<{tag} />',
												f'<View style={{{{replaced_styles.{tag_name}}}}}><Button title="Pick Document" onPress={{() => {{}}}} /><Button title="Pick Document onPress={{() => {{}}}} /></View>'
										).replace(
												f'<{tag}/>',
												f'<View style={{{{replaced_styles.{tag_name}}}}}><Button title="Pick Document" onPress={{() => {{}}}} /><Button title="Pick Document onPress={{() => {{}}}} /></View>'
										)
                else:
                    content = content.replace(
                        f'<{tag}>',
                        f'{native_tag} style={{replaced_styles.{tag_name}}}>'
                    ).replace(
                        f'</{tag}>',
                        f'</{native_tag[:native_tag.index(" ")]}>'
                    ).replace(
                        f'<{tag} />',
                        f'{native_tag} style={{replaced_styles.{tag_name}}} />'
                    ).replace(
                        f'<{tag}/>',
                        f'{native_tag} style={{replaced_styles.{tag_name}}}/>'
                    )

            elif tag_name == 'select':
                if is_react:
                    content = check_imports(content, file_ext, 'Picker', 'react-native-picker-select')
                replacements[tag_name] = 'Picker'
                content = replace_content(content, tag, tag_name, 'Picker', onPress=True)

            elif tag_name == 'audio':
                if is_react:
                    content = check_imports(content, file_ext, 'View, Button')
                replacements[tag_name] = 'View__Button'
                content = content.replace(
                    f'<{tag}>',
                    f'<View>\n\t<Button title="Play Sound" onPress={{() => {{}}}} />\n\t<Button title="Stop Sound" onPress={{() => {{}}}} />'
                ).replace(
                    f'</{tag}>',
                    '</View>'
                ).replace(
                    f'<{tag} />',
                    f'<View>\n\t<Button title="Play Sound" onPress={{() => {{}}}} />\n\t<Button title="Stop Sound" onPress={{() => {{}}}} />\n</View>'
                ).replace(
                    f'<{tag}/>',
                    f'<View>\n\t<Button title="Play Sound" onPress={{() => {{}}}} />\n\t<Button title="Stop Sound" onPress={{() => {{}}}} />\n</View>'
                )

            elif tag_name == 'canvas':
                if is_react:
                    content = check_imports(content, file_ext, 'Canvas', 'react-native-canvas')
                replacements[tag_name] = 'Canvas'
                content = replace_content(content, tag, tag_name, 'Canvas')

            elif tag_name in ['embed', 'fencedframe', 'iframe', 'frame', 'object']:
                if is_react:
                    content = check_imports(content, file_ext, 'WebView', 'react-native-webview')
                replacements[tag_name] = 'WebView'
                content = replace_content(content, tag, tag_name, 'WebView', onPress=True)

            elif tag_name in ['progress', 'meter']:
                if is_react:
                    content = check_imports(content, file_ext, 'Progress.Bar', 'react-native-progress')
                replacements[tag_name] = 'Progress.Bar'
                content = replace_content(content, tag, tag_name, 'Progress.Bar')

            elif tag_name == 'video':
                if is_react:
                    content = check_imports(content, file_ext, 'Video', 'react-native-video')
                replacements[tag_name] = 'Video'
                content = replace_content(content, tag, tag_name, 'Video', onPress=True)

            elif tag_name in ['base', 'col', 'colgroup', 'data', 'template', 'head', 'html', 'link', 'meta', 'noscript', 'script',
                              'source', 'style', 'title']:
                replacements[tag_name] = 'removed'
                content = content.replace(
                    f'<{tag_name}>',
                    '<Text style={ display: "none"; }>'
                ).replace(
                    f'</{tag}>',
                    '</Text>'
                ).replace(
                    f'<{tag} />',
                    '<Text style={ display: "none"; } />'
                ).replace(
                    f'<{tag}/>',
                    '<Text style={ display: "none"; }/>'
                )

            else:
                content = content.replace(
                    f'<{tag}>',
                    '<Text>#ERR'
                ).replace(
                    f'</{tag}>',
                    '</Text>'
                ).replace(
                    f'<{tag} />',
                    '<Text>#ERR</Text>'
                ).replace(
                    f'<{tag}/>',
                    '<Text>#ERR</Text>'
                )
        with open(new_file_path, 'w', encoding='utf-8', errors='replace') as new_file:
            new_file.write(content)
            print(Fore.GREEN + f'Created: {new_file_path}' + Style.RESET_ALL)

        with open(replacements_json_path, 'w', encoding='utf-8', errors='replace') as json_file:
            json.dump(replacements, json_file, indent=4)
            print(Fore.GREEN + f'Created: {replacements_json_path}' + Style.RESET_ALL)

        with open(replacement_styles, 'w', encoding='utf-8', errors='replace') as new_style:
            new_style.write(replacement_content)
            print(Fore.GREEN + f'Created: {replacement_styles}' + Style.RESET_ALL)

    except Exception as e:
        print(Fore.RED + f'Error reading file {path}: {e}' + Style.RESET_ALL)

def validate_dirp() -> str | None:
  acc = 0
  while acc < 10:
    dirp = input('Enter the directory path:')
    if (os.path.isdir(dirp)):
      return dirp
    print(Fore.RED + 'No such valid directory. Enter another path or press Escape.')
    acc += 1
    if (acc >= 10):
      print(Fore.RED + 'Maximum attempts reached. Exiting...' + Style.RESET_ALL)
      time.sleep(3)
      sys.exit(1)
if __name__ == '__main__':
  walk_dir(validate_dirp())