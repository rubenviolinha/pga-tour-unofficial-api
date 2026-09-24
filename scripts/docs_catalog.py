"""Render the bundled CSV as searchable, accessible documentation at build time."""
import csv
from html import escape
from pathlib import Path


def on_page_markdown(markdown, page, config, **kwargs):
    marker = "<!-- STATS_CATALOG -->"
    if marker not in markdown:
        return markdown
    source = Path(config["docs_dir"]) / "data" / "stat_ids.csv"
    with source.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    parts = ['<div class="stats-catalog" data-stats-catalog>',
             '<div class="stats-controls" hidden>',
             '<label>Search statistics<input type="search" data-search placeholder="Name or ID, e.g. greens or 02675"></label>',
             '<label>Category<select data-category><option value="">All categories</option></select></label>',
             '<label>Subcategory<select data-subcategory><option value="">All subcategories</option></select></label>',
             '<button type="button" data-reset>Clear filters</button></div>',
             f'<p data-count role="status">{len(rows)} statistics</p>',
             '<p data-copy-status role="status"></p>',
             '<div class="stats-table-scroll" tabindex="0" role="region" aria-label="Statistics catalog">',
             '<table><thead><tr><th scope="col">ID</th><th scope="col">Statistic</th><th scope="col">Category</th><th scope="col">Subcategory</th></tr></thead><tbody>']
    for row in rows:
        sid, name, category, subcategory = [escape(row[key], quote=True) for key in
                                          ("stat_id", "stat_name", "category", "subcategory")]
        parts.append(f'<tr data-category="{category}" data-subcategory="{subcategory}"><td><code>{sid}</code> <button type="button" data-copy="{sid}" aria-label="Copy statistic ID {sid}" hidden>Copy</button></td><td>{name}</td><td>{category}</td><td>{subcategory}</td></tr>')
    parts.extend(['</tbody></table></div>', '<p data-empty hidden>No matching statistics. Try another search or clear the filters.</p>', '</div>'])
    return markdown.replace(marker, "\n".join(parts))
