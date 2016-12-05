import sublime, sublime_plugin

class SplitLineCommand(sublime_plugin.TextCommand):
    def run(self, edit, **args):
        def remove_ws(txt):
            return txt.strip(' ').strip('\t').strip(' ')

        def split_text(selected_text, indent_size):
            settings = sublime.load_settings('Split_Line.sublime-settings')

            original_text = selected_text

            num_tabs = int(int(indent_size)/4)

            remainder = int(indent_size - 4*num_tabs)
            indent = "\t" * num_tabs + ' ' * remainder

            selected_text = selected_text.lstrip(' ').lstrip('\t')

            pre_multi = ''
            post_multi = ''

            brackets = []

            if '(' in selected_text:
                brackets.append((selected_text.find('('), '('))

            if '[' in selected_text:
                brackets.append((selected_text.find('['), '['))

            if '{' in selected_text:
                brackets.append((selected_text.find('{'), '{'))

            brackets = sorted(brackets, key=lambda tup: tup[0])

            if brackets[0][1] == '(':
                lbracket = '('
                rbracket = ')'
            elif brackets[0][1] == '[':
                lbracket = '['
                rbracket = ']'
            elif brackets[0][1] == '{':
                lbracket = '{'
                rbracket = '}'

            lb_loc = None
            rb_loc = None

            trailing_comma = False

            if lbracket in selected_text:
                lb_loc = selected_text.index(lbracket)
                pre_multi = selected_text[:lb_loc+1]
                selected_text = selected_text[lb_loc+1:]

            if rbracket in selected_text:
                rb_loc = selected_text.rfind(rbracket)

                if selected_text[rb_loc-1] == ',':
                    trailing_comma = True

                post_multi = selected_text[rb_loc:]
                selected_text = selected_text[:rb_loc]

            multi_line_text = None

            if "\n" not in selected_text:
                if (
                    (
                        ',' in selected_text.strip(' ')
                        and selected_text.strip(' ').index(',') != len(selected_text.strip(' '))-1
                    )
                    or (lb_loc is not None and rb_loc is not None)
                ):

                    tarray = []
                    l1 = 0
                    in_bracket = False

                    for i, c in enumerate(selected_text):
                        if c in ['(', '[', '{']:
                            in_bracket = True
                        elif c in [')', ']', '}']:
                            in_bracket = False

                        if c == ',' and not in_bracket:
                            tarray.append(selected_text[l1:i].strip(' '))
                            l1 = i+1
                        elif i == len(selected_text)-1:
                            tarray.append(selected_text[l1:i+1].strip(' '))

                    # Call iteratively on tarray memebers
                    if settings.get('recursive_split', False):
                        for i, t in enumerate(tarray):
                            if (
                                ('(' in t or '[' in t or '{' in t)
                                and remove_ws(t) not in ['(', ')', '[', ']', '{', '}']
                            ):
                                _, tarray[i:i+1] = split_text(t, indent_size)

                    full_array = [pre_multi]
                    full_array.extend(["\t"+t for t in tarray])
                    full_array.append(post_multi)

                    multi_line_text = indent + pre_multi + '\n'
                    for i, l in enumerate(tarray):
                        if (
                            (i != len(tarray)-1 or trailing_comma)
                            and remove_ws(l) not in ['(', '[', '{']
                        ):
                            multi_line_text += indent + "\t" + l + ',\n'
                        else:
                            multi_line_text += indent + "\t" + l + '\n'

                    multi_line_text += indent + post_multi

                    return multi_line_text, full_array
                else:
                    print('No splittable line found.')
            else:
                print('Does not work over multiple lines.')

            return original_text, []

        for region in self.view.sel():
            if region.empty():
                line = self.view.line(region)
                selected_text = self.view.substr(line)

                indent_text = selected_text[:len(selected_text) - len(selected_text.lstrip(' ').lstrip('\t').lstrip(' '))]
                indent_size = 0
                for c in indent_text:
                    if c == '\t':
                        indent_size += 4
                    else:
                        indent_size += 1

                multi_line_text, _ = split_text(selected_text, indent_size)

                self.view.replace(edit, line, multi_line_text)
