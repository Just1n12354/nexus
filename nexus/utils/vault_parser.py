"""Vault file parsing — frontmatter, wikilinks, metadata."""

import re
import yaml
from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Frontmatter:
    """YAML frontmatter parsed from a markdown file."""
    title: str = ""
    type: str = ""
    status: str = ""
    updated: str = ""
    description: str = ""
    aliases: list = field(default_factory=list)
    tags: list = field(default_factory=list)
    raw: dict = field(default_factory=dict)
    error: str = ""


@dataclass
class Wikilink:
    """A parsed [[wikilink]] from markdown content."""
    raw: str  # e.g. "[[biografie|Biografie]]"
    target: str  # e.g. "biografie"
    alias: Optional[str] = None  # e.g. "Biografie"
    file_path: str = ""  # source file


@dataclass
class VaultFile:
    """Parsed representation of a single markdown file in the vault."""
    path: Path
    content: str
    frontmatter: Frontmatter = field(default_factory=Frontmatter)
    wikilinks: list = field(default_factory=list)
    is_binary: bool = False
    empty: bool = False
    error: Optional[str] = None


class FrontmatterParser:
    """Parse YAML frontmatter from markdown content."""

    FRONTMATTER_RE = re.compile(
        r'^---\s*\n(.*?)\n^---\s*\n?', re.DOTALL | re.MULTILINE
    )

    def parse(self, content: str) -> Frontmatter:
        """Extract and parse frontmatter from markdown content."""
        fm = Frontmatter()

        match = self.FRONTMATTER_RE.search(content)
        if not match:
            return fm  # No frontmatter found

        try:
            data = yaml.safe_load(match.group(1))
            if isinstance(data, dict):
                fm.raw = data
                fm.title = str(data.get('title', ''))
                fm.type = str(data.get('type', ''))
                fm.status = str(data.get('status', ''))
                fm.updated = str(data.get('updated', ''))
                fm.description = str(data.get('description', ''))
                aliases = data.get('aliases', [])
                fm.aliases = [str(a) for a in aliases] if isinstance(aliases, list) else []
                tags = data.get('tags', [])
                fm.tags = [str(t) for t in tags] if isinstance(tags, list) else []
        except yaml.YAMLError:
            fm.error = "Invalid YAML in frontmatter"

        return fm


class WikilinkParser:
    """Parse [[wikilinks]] from markdown content."""

    WIKILINK_RE = re.compile(
        r'\[\[([^\]]+)\]\]'
    )

    def parse(self, content: str, source_path: str = "") -> list[Wikilink]:
        """Find all wikilinks in content."""
        links = []
        for match in self.WIKILINK_RE.finditer(content):
            raw = match.group(0)
            target_raw = match.group(1)

            if '|' in target_raw:
                target, alias = target_raw.split('|', 1)
                target = target.strip()
                alias = alias.strip()
            else:
                target = target_raw.strip()
                alias = None

            links.append(Wikilink(
                raw=raw,
                target=target,
                alias=alias,
                file_path=source_path,
            ))

        return links


class VaultParser:
    """Parse all markdown files in a vault directory."""

    def __init__(self, vault_path: str):
        self.vault_path = Path(vault_path)
        self.frontmatter_parser = FrontmatterParser()
        self.wikilink_parser = WikilinkParser()
        self.files: list[VaultFile] = []

    def scan(self) -> list[VaultFile]:
        """Walk the vault and parse all .md files."""
        self.files = []
        for md_file in sorted(self.vault_path.rglob('*.md')):
            # Skip binary dirs and .obsidian
            if '.git' in str(md_file):
                continue
            if '.obsidian' in str(md_file):
                continue

            vf = self._parse_file(md_file)
            if vf is not None:
                self.files.append(vf)

        return self.files

    def _parse_file(self, md_file: Path) -> Optional[VaultFile]:
        """Parse a single markdown file."""
        try:
            # Try to read — if it fails (placeholder), handle gracefully
            content = md_file.read_text(encoding='utf-8')
        except OSError:
            return VaultFile(
                path=md_file,
                content="",
                empty=False,
                error=f"Cannot read file (placeholder?): {md_file.name}",
            )

        # Skip empty files
        is_empty = len(content.strip()) == 0
        if is_empty:
            return VaultFile(
                path=md_file,
                content="",
                empty=True,
            )

        # Parse frontmatter
        frontmatter = self.frontmatter_parser.parse(content)

        # Parse wikilinks
        wikilinks = self.wikilink_parser.parse(content, str(md_file.relative_to(self.vault_path)))

        return VaultFile(
            path=md_file,
            content=content,
            frontmatter=frontmatter,
            wikilinks=wikilinks,
        )

    def get_by_path(self, relative_path: str) -> Optional[VaultFile]:
        """Find a parsed file by its relative path."""
        for vf in self.files:
            rp = str(vf.path.relative_to(self.vault_path))
            if rp == relative_path or rp.rstrip('/') == relative_path:
                return vf
        return None

    def get_by_filename(self, filename: str) -> Optional[VaultFile]:
        """Find a parsed file by its filename (basename)."""
        for vf in self.files:
            if vf.path.name == filename:
                return vf
        return None

    def get_empty_files(self) -> list[VaultFile]:
        """Return all empty .md files."""
        return [f for f in self.files if f.empty]

    def get_orphan_files(self) -> list[VaultFile]:
        """Return files with no frontmatter title (orphans)."""
        return [f for f in self.files if not f.frontmatter.title]

    def get_all_wikilinks(self) -> list[Wikilink]:
        """Return all wikilinks from all files."""
        all_links = []
        for vf in self.files:
            all_links.extend(vf.wikilinks)
        return all_links

    def print_summary(self) -> None:
        """Print a summary of the parsed vault."""
        print(f"Vault: {self.vault_path}")
        print(f"  Files parsed: {len(self.files)}")
        print(f"  Empty files: {len([f for f in self.files if f.empty])}")
        print(f"  Total wikilinks: {len(self.get_all_wikilinks())}")
        print(f"  No title: {len([f for f in self.files if not f.frontmatter.title])}")