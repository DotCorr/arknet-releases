#!/usr/bin/env python3
"""Copy Arknet's developer docs from a checkout of the platform repo into this one.

The docs are written for the site (arknet.si/docs/...), so links are rewritten
to work on GitHub: /docs/<page> becomes <page>.md, and other site paths
(/legal/..., /llms.txt) point at https://arknet.si.

    python3 scripts/sync-docs.py ../arknet-platform
"""
import pathlib
import re
import shutil
import sys

SITE = 'https://arknet.si'


def rewrite(markdown: str) -> str:
    def link(match: re.Match) -> str:
        text, target = match.group(1), match.group(2)
        page = re.fullmatch(r'/docs/?([a-z0-9-]*)(\.md)?(#[^)]*)?', target)
        if page:
            name = page.group(1) or 'index'
            return f'[{text}]({name}.md{page.group(3) or ""})'
        if target == '/docs/openapi.json':
            return f'[{text}](openapi.json)'
        if target.startswith('/'):
            return f'[{text}]({SITE}{target})'
        return match.group(0)

    return re.sub(r'\[([^\]]+)\]\(([^)\s]+)\)', link, markdown)


def main() -> None:
    if len(sys.argv) != 2:
        sys.exit('usage: sync-docs.py <path to arknet-platform checkout>')
    source = pathlib.Path(sys.argv[1]) / 'client' / 'public' / 'docs'
    target = pathlib.Path(__file__).resolve().parent.parent / 'docs'
    if not source.is_dir():
        sys.exit(f'no docs at {source}')
    target.mkdir(exist_ok=True)
    for page in sorted(source.glob('*.md')):
        (target / page.name).write_text(rewrite(page.read_text()))
        print('docs/' + page.name)
    shutil.copy(source / 'openapi.json', target / 'openapi.json')
    print('docs/openapi.json')


if __name__ == '__main__':
    main()
