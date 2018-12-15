"""
"""

class DefaultFormatter:
    header_start = ''
    header_end = ''
    addition_start = ''
    addition_end = ''
    subtraction_start = ''
    subtraction_end = ''

class ConsoleFormatter(DefaultFormatter):
    header_start = '\033[1m'
    header_end = '\033[0m'
    addition_start = '\033[92m'
    addition_end = '\033[0m'
    subtraction_start = '\033[91m'
    subtraction_end = '\033[0m'

class HTMLFormatter(DefaultFormatter):
    header_start = '<b>'
    header_end = '</b>'
    addition_start = '<span style="color:green">'
    addition_end = '</span>'
    subtraction_start = '<span style="color:red">'
    subtraction_end = '</span>'

class OutputFormatting:

    def __str__(self):
        return self._format(DefaultFormatter)

    def to_console(self):
        return self._format(ConsoleFormatter)

    def to_html(self, full_html=False):
        partial_html = self._format(HTMLFormatter)
        if not full_html:
            return partial_html
        else:
            html_page = '''
                <html>
                    <body>
                        <pre>
                            {}
                        </pre>
                    </body>
                </html>
            '''
            html_page = '\n'.join([l.strip() for l in html_page.splitlines()])
            return html_page.format(partial_html)
