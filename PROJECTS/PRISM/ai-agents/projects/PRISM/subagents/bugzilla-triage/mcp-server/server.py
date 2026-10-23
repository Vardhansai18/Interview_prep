#!/usr/bin/env python3
"""
Bugzilla MCP Server for F5 BIG-IP Bugzilla and Review Board.

Wraps the Bugzilla REST API and Review Board API into MCP tools so that
agents never handle API keys directly. The API keys are read once at startup
from environment variables:

    BUGZILLA_API_KEY      — Bugzilla REST API key
    REVIEWBOARD_API_KEY   — Review Board API token (optional)

Install dependencies:
    pip install mcp httpx

Run (stdio transport, used by VS Code):
    python server.py
"""

import os
import sys
import httpx
from mcp.server.fastmcp import FastMCP

# ---------------------------------------------------------------------------
# Configuration — read from environment, never from user input
# ---------------------------------------------------------------------------
BUGZILLA_BASE = "https://bugzilla.olympus.f5net.com"
REVIEWBOARD_BASE = "https://reviewboard.olympus.f5net.com"

BUGZILLA_API_KEY = os.environ.get("BUGZILLA_API_KEY", "")
REVIEWBOARD_API_KEY = os.environ.get("REVIEWBOARD_API_KEY", "")

if not BUGZILLA_API_KEY:
    print(
        "ERROR: BUGZILLA_API_KEY environment variable is not set.",
        file=sys.stderr,
    )
    sys.exit(1)

# ---------------------------------------------------------------------------
# MCP server instance
# ---------------------------------------------------------------------------
mcp = FastMCP("bugzilla-f5")

# ---------------------------------------------------------------------------
# Shared HTTP helpers
# ---------------------------------------------------------------------------

def _bugzilla_get(path: str, params: dict | None = None) -> dict:
    """Make an authenticated GET request to the Bugzilla REST API."""
    p = dict(params or {})
    p["api_key"] = BUGZILLA_API_KEY
    url = f"{BUGZILLA_BASE}/rest/{path.lstrip('/')}"
    response = httpx.get(url, params=p, timeout=30)
    response.raise_for_status()
    return response.json()


def _reviewboard_get(path: str, params: dict | None = None) -> dict:
    """Make an authenticated GET request to the Review Board API."""
    if not REVIEWBOARD_API_KEY:
        raise RuntimeError("REVIEWBOARD_API_KEY environment variable is not set.")
    headers = {"Authorization": f"token {REVIEWBOARD_API_KEY}"}
    url = f"{REVIEWBOARD_BASE}/api/{path.lstrip('/')}"
    response = httpx.get(url, params=params or {}, headers=headers, timeout=30)
    response.raise_for_status()
    return response.json()


# ---------------------------------------------------------------------------
# Bugzilla tools
# ---------------------------------------------------------------------------

@mcp.tool()
def bugzilla_get_bug(bug_id: int) -> dict:
    """
    Fetch full metadata for a single Bugzilla bug.

    Returns a dict containing: id, summary, status, resolution, component,
    product, assigned_to, creator, qa_contact, severity, priority, see_also,
    blocks, depends_on, and all other bug fields.

    Args:
        bug_id: The numeric Bugzilla bug ID.
    """
    data = _bugzilla_get(f"bug/{bug_id}")
    bugs = data.get("bugs", [])
    if not bugs:
        raise ValueError(f"Bug {bug_id} not found.")
    return bugs[0]


@mcp.tool()
def bugzilla_get_comments(bug_id: int) -> list[dict]:
    """
    Fetch all comments for a Bugzilla bug.

    Returns a list of comment dicts, each containing: id, text, creator,
    creation_time, is_private.

    Args:
        bug_id: The numeric Bugzilla bug ID.
    """
    data = _bugzilla_get(f"bug/{bug_id}/comment")
    return data.get("bugs", {}).get(str(bug_id), {}).get("comments", [])


@mcp.tool()
def bugzilla_search_by_content(
    term: str,
    product: str = "BIG-IP",
    include_fields: str = "id,summary",
    limit: int = 100,
) -> list[dict]:
    """
    Full-text search Bugzilla (bug descriptions AND comments) for a single term.

    Uses the REST `content=` parameter which performs full-text search across
    summary, description, and all comments. To perform an AND search across
    multiple terms, call this tool once per term and intersect the returned
    ID sets yourself.

    Args:
        term:           The search term (a distinctive function name, error
                        message fragment, source file name, etc.).
                        Do NOT include line numbers — they change per release.
        product:        Bugzilla product to restrict search to (default: BIG-IP).
        include_fields: Comma-separated list of fields to return
                        (default: "id,summary").
        limit:          Maximum number of results to return (default: 100).

    Returns:
        List of dicts with the requested fields for each matching bug.
    """
    params = {
        "product": product,
        "content": term,
        "include_fields": include_fields,
        "limit": limit,
    }
    data = _bugzilla_get("bug", params)
    return data.get("bugs", [])


@mcp.tool()
def bugzilla_search_by_summary(
    keywords: str,
    product: str = "BIG-IP",
    include_fields: str = "id,summary",
    limit: int = 100,
) -> list[dict]:
    """
    Search Bugzilla bug summaries (title only) for keywords.

    This is an indexed, fast search — use it to quickly find bugs whose
    title contains the given keywords. For full-text search including
    descriptions and comments, use bugzilla_search_by_content instead.

    Args:
        keywords:       Space-separated keywords to search in the summary.
        product:        Bugzilla product to restrict search to (default: BIG-IP).
        include_fields: Comma-separated list of fields to return
                        (default: "id,summary").
        limit:          Maximum number of results to return (default: 100).

    Returns:
        List of dicts with the requested fields for each matching bug.
    """
    params = {
        "product": product,
        "summary": keywords,
        "include_fields": include_fields,
        "limit": limit,
    }
    data = _bugzilla_get("bug", params)
    return data.get("bugs", [])


# ---------------------------------------------------------------------------
# Review Board tools
# ---------------------------------------------------------------------------

@mcp.tool()
def reviewboard_get_diffs(review_request_id: int) -> dict:
    """
    Fetch the list of diffs for a Review Board review request.

    Returns the raw Review Board API response containing all diff revisions
    for the specified review request.

    Args:
        review_request_id: The numeric Review Board review request ID.
    """
    return _reviewboard_get(f"review-requests/{review_request_id}/diffs/")


@mcp.tool()
def reviewboard_get_patched_file(
    review_request_id: int,
    diff_num: int,
    file_id: int,
) -> str:
    """
    Fetch the patched (post-change) content of a specific file from a
    Review Board diff.

    Args:
        review_request_id: The numeric Review Board review request ID.
        diff_num:          The diff revision number (1-based).
        file_id:           The numeric file ID within the diff.

    Returns:
        The patched file content as a string.
    """
    path = (
        f"review-requests/{review_request_id}/diffs/{diff_num}"
        f"/files/{file_id}/patched-file/"
    )
    if not REVIEWBOARD_API_KEY:
        raise RuntimeError("REVIEWBOARD_API_KEY environment variable is not set.")
    headers = {"Authorization": f"token {REVIEWBOARD_API_KEY}"}
    url = f"{REVIEWBOARD_BASE}/api/{path}"
    response = httpx.get(url, headers=headers, timeout=30)
    response.raise_for_status()
    return response.text


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    mcp.run(transport="stdio")
