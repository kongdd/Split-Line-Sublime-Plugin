import sublime, sublime_plugin

class SplitLineCommand(sublime_plugin.TextCommand):
    def run(self, edit, **args):
        def split_text(selected_text, indent_size):
            num_tabs = int(int(indent_size)/4)

            remainder = int(indent_size - 4*num_tabs)
            indent = "\t" * num_tabs + ' ' * remainder

            selected_text = selected_text.lstrip(' ').lstrip('\t')

            pre_multi = ''
            post_multi = ''

            lbracket = '('
            rbracket = ')'

            if '(' in selected_text:
                lbracket = '('
                rbracket = ')'
            elif '[' in selected_text:
                lbracket = '['
                rbracket = ']'
            elif '{' in selected_text:
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
                if ',' in selected_text or (lb_loc is not None and rb_loc is not None):

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
                    for i, t in enumerate(tarray):
                        if '(' in t or '[' in t or '{' in t:
                            _, tarray[i:i+1] = split_text(t, indent_size)

                    full_array = [pre_multi]
                    full_array.extend(["\t"+t for t in tarray])
                    full_array.append(post_multi)

                    multi_line_text = indent + pre_multi + '\n'
                    for i, l in enumerate(tarray):
                        if (
                            (i != len(tarray)-1 or trailing_comma)
                            and l.strip(' ') not in ['(', '[', '{']
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

            return selected_text, []



        for region in self.view.sel():
            if region.empty():
                line = self.view.line(region)
                selected_text = self.view.substr(line)

                # indent_size = len(selected_text) - len(selected_text.lstrip(' ').lstrip('\t'))
                indent_text = selected_text[:len(selected_text) - len(selected_text.lstrip(' ').lstrip('\t'))]
                indent_size = 0
                for c in indent_text:
                    if c == '\t':
                        indent_size += 4
                    else:
                        indent_size += 1

                multi_line_text, _ = split_text(selected_text, indent_size)

                self.view.replace(edit, line, multi_line_text)
