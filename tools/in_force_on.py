"""Which Acts and Legal Notices were published, or say they come into force, by a date; or print one of them.

    python tools/in_force_on.py 2022-06-01                  # every Act and L.N. published on or before that day
    python tools/in_force_on.py 2022-06-01 --amending cap/12  # ... that amend Cap. 12
    python tools/in_force_on.py 2022-06-01 act/2020/5       # Act V of 2020 as published, if it was by then
    python tools/in_force_on.py 2022-06-01 act/2020/5 3     # its section 3

Commits are dated by publication, so this reads the `Published:` trailer (the real date; commit dates before 1970
are clamped). A law's own commencement, where it states one, is in its `Commencement:` trailers. Standard library only.
"""
import re
import subprocess
import sys


def git(*args: str) -> str:
    return subprocess.run(['git', *args], capture_output=True, text=True, encoding='utf-8', check=True).stdout


def published(day: str) -> list[tuple[str, str, str, list[str], list[str]]]:
    fmt = ('%H%x1f%an%x1f%(trailers:key=Published,valueonly,separator=)%x1f'
           '%(trailers:key=Amends,valueonly,separator=;)%x1f%(trailers:key=Commencement,valueonly,separator=;)%x1e')
    out = []
    for rec in git('log', '--first-parent', '--reverse', f'--format={fmt}', 'HEAD').split('\x1e'):
        parts = rec.strip('\n').split('\x1f')
        if len(parts) < 5 or not parts[2].strip():
            continue
        h, name, pub, amends, comm = parts
        if pub.strip() <= day:
            out.append((h, name, pub.strip(), [a for a in amends.split(';') if a],
                        [c for c in comm.split(';') if c]))
    return out


def main() -> None:
    sys.stdout.reconfigure(encoding='utf-8')
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    day = sys.argv[1]
    rest = sys.argv[2:]
    if rest and rest[0] == '--amending':
        want = rest[1].replace('cap/', 'Cap. ').replace('sl/', 'S.L. ')
        for h, name, pub, amends, comm in published(day):
            if want in amends:
                print(f"{pub}  {name}  commencement: {', '.join(comm) or '-'}")
        return
    if rest:
        path = 'acts/' + rest[0].strip('/') + (f'/{rest[1]}.md' if len(rest) > 1 else '')
        touched = set(git('log', '--format=%H', 'HEAD', '--', path).split())
        hits = [h for h, *_ in published(day) if h in touched]
        if not hits:
            sys.exit(f'{path}: not published on or before {day}')
        if len(rest) > 1:
            sys.stdout.write(git('show', f'{hits[-1]}:{path}'))
        else:
            names = git('ls-tree', '--name-only', hits[-1], path + '/').split()
            key = lambda n: (not n.endswith('/title.md'), [int(x) if x.isdigit() else x for x in re.split(r'(\d+)', n)])
            for n in sorted(names, key=key):
                sys.stdout.write(git('show', f'{hits[-1]}:{n}') + '\n')
        return
    for h, name, pub, amends, comm in published(day):
        print(f"{pub}  {name}  amends: {', '.join(amends) or '-'}")


if __name__ == '__main__':
    main()
