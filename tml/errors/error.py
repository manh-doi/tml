from functools import reduce


def error_detail(file_name, start_position, end_position, content=None):
    if not content:
        with open(file_name, "r") as f:
            content = f.read()

    def detail(content_in_lines):
        start_line = start_position.line - 1
        end_line = end_position.line

        shown_lines = content_in_lines[start_line:end_line]
        indicator_lines = []

        for i in range(len(shown_lines)):
            indicator_line = ""
            if i == 0:
                indicator_line = "~" * (start_position.col - 1)
                if end_position.line > start_position.line:
                    indicator_line += "^" * (len(shown_lines[i]) - start_position.col)
                else:
                    indicator_line += "^" * max(1, (end_position.col - start_position.col))
            else:
                indicator_line += "^" * end_position.col

            indicator_lines.append(indicator_line)

        res = reduce(lambda r, x: r + [x[0].rstrip(), x[1]], zip(shown_lines, indicator_lines), [])
        return "\n".join(res)

    return detail(content.split("\n"))
