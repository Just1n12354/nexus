"""Nexus-specific parsing — broken link detection, index generation."""

from pathlib import Path
from typing import Optional
from .vault_parser import VaultParser, VaultFile, Wikilink


class BrokenLinkChecker:
    """Check wikilinks against the actual vault filesystem."""

    def __init__(self, vault_path: str):
        self.vault_path = Path(vault_path)
        self.vault = VaultParser(vault_path)
        self.vault.scan()

    def find_broken_links(self, exclude_patterns: Optional[list[str]] = None) -> list[dict]:
        """Find all broken wikilinks in the vault.

        Args:
            exclude_patterns: Patterns to skip (e.g. 'LOG.md' for week logs)

        Returns:
            List of dicts with file, link, and reason.
        """
        if exclude_patterns is None:
            exclude_patterns = []

        broken = []

        for vf in self.vault.files:
            rel_path = str(vf.path.relative_to(self.vault_path))

            # Skip excluded patterns
            skip = False
            for pat in exclude_patterns:
                if pat in rel_path:
                    skip = True
                    break
            if skip:
                continue

            # Skip files without content
            if not vf.content or vf.empty:
                continue

            # Check each wikilink
            for link in vf.wikilinks:
                if self._is_resolvable(link):
                    continue

                broken.append({
                    'file': rel_path,
                    'link': link.target,
                    'raw': link.raw,
                    'alias': link.alias,
                })

        return broken

    def _is_resolvable(self, link: Wikilink) -> bool:
        """Check if a wikilink can be resolved to an actual file."""
        stem = link.target.strip()

        # Skip fragments and special references
        if stem.startswith('#'):
            return True
        if stem in ('wikilink', 'NAME', 'stem', 'Dateiname', 'Sichtbarer Text'):
            return True

        # Check relative to current file's directory
        candidates = [
            self.vault_path / stem,  # e.g. 40_Finanzen/README
            self.vault_path / f"{stem}.md",  # e.g. 40_Finanzen/README.md
            self.vault_path / stem / "README.md",  # e.g. 40_Finanzen/README.md
        ]

        # Also check relative to source file's directory
        src_dir = link.file_path and Path(link.file_path).parent
        if src_dir:
            src_dir = self.vault_path / src_dir
            candidates.extend([
                src_dir / stem,
                src_dir / f"{stem}.md",
                src_dir / stem / "README.md",
            ])

        return any(c.exists() for c in candidates)

    def find_orphans(self) -> list[VaultFile]:
        """Find files with no frontmatter title (orphans)."""
        return self.vault.get_orphan_files()

    def print_broken_report(self) -> None:
        """Print a report of broken links."""
        broken = self.find_broken_links()

        print(f"Broken links found: {len(broken)}")
        for b in broken:
            print(f"  {b['file']} → [[{b['link']}]]")


class NexusParser:
    """High-level Nexus vault operations."""

    def __init__(self, vault_path: str):
        self.vault_path = Path(vault_path)
        self.vault = VaultParser(vault_path)
        self.checker = BrokenLinkChecker(vault_path)

    def scan_all(self) -> dict:
        """Run full scan and return results."""
        files = self.vault.scan()
        broken = self.checker.find_broken_links(exclude_patterns=['LOG.md'])

        return {
            'total_files': len(files),
            'empty_files': len(self.vault.get_empty_files()),
            'no_title': len(self.vault.get_orphan_files()),
            'total_wikilinks': len(self.vault.get_all_wikilinks()),
            'broken_links': len(broken),
            'broken_details': broken,
        }

    def add_frontmatter(self, file_path: Path, title: str, ftype: str = "note", status: str = "aktiv") -> bool:
        """Add frontmatter to a file that has none."""
        try:
            content = file_path.read_text(encoding='utf-8')
            if not content.strip():
                return False  # Empty file

            # Check if already has frontmatter
            if content.strip().startswith('---'):
                return False  # Already has frontmatter

            fm = f"---\ntitle: {title}\ntype: {ftype}\nstatus: {status}\nupdated: {Path(file_path).parent.name}\n---\n\n{content}"
            file_path.write_text(fm, encoding='utf-8')
            return True
        except Exception:
            return False

    def generate_readme(self, folder_path: Path, title: str, description: str) -> str:
        """Generate a README.md for a folder."""
        children = sorted([
            str(f.relative_to(folder_path))
            for f in folder_path.glob('*.md')
            if f.name != 'README.md'
        ])

        lines = [
            "---",
            f"title: {title}",
            f"type: moc",
            "status: aktiv",
            "updated: 2026-06-25",
            f"description: {description}",
            "---",
            "",
            f"# {title}",
            "",
            description,
            "",
            "## Dateien",
            "",
        ]

        for child in children:
            name = Path(child).stem
            lines.append(f"- [[{child}|{name}]]")

        lines.extend(["", "## Verweise", ""])

        return '\n'.join(lines)