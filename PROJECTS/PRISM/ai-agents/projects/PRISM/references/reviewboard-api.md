# Review Board API Reference

Base URL: `https://reviewboard.olympus.f5net.com`
Auth: `Authorization: token $REVIEWBOARD_API_KEY`

**Prerequisite:** `$REVIEWBOARD_API_KEY` must be set in the environment. Check with:
```bash
echo ${REVIEWBOARD_API_KEY:0:8}...
```
If unset, ask the user to provide it. Never hardcode or log the key.

---

## Fetching an Existing Review Request

### Get review request metadata
```bash
curl -s -H "Authorization: token $REVIEWBOARD_API_KEY" \
  "https://reviewboard.olympus.f5net.com/api/review-requests/<RB_ID>/" \
  | python3 -m json.tool
```
Key fields: `description`, `bugs_closed`, `branch`, `approved`, `changenum`

### Get the diff (raw patch)
```bash
# Step 1: list diffs, get diff ID
curl -s -H "Authorization: token $REVIEWBOARD_API_KEY" \
  "https://reviewboard.olympus.f5net.com/api/review-requests/<RB_ID>/diffs/" \
  | python3 -c "import sys,json; d=json.load(sys.stdin)['diffs']; print(d[-1]['id'])"

# Step 2: fetch raw patch using diff ID
curl -s -H "Authorization: token $REVIEWBOARD_API_KEY" \
     -H "Accept: text/x-patch" \
  "https://reviewboard.olympus.f5net.com/api/review-requests/<RB_ID>/diffs/<DIFF_ID>/"
```

### Get diff file list (see which files changed)
```bash
curl -s -H "Authorization: token $REVIEWBOARD_API_KEY" \
  "https://reviewboard.olympus.f5net.com/api/review-requests/<RB_ID>/diffs/<DIFF_ID>/files/" \
  | python3 -c "import sys,json; [print(f['dest_file']) for f in json.load(sys.stdin)['files']]"
```

### Get reviews/comments
```bash
curl -s -H "Authorization: token $REVIEWBOARD_API_KEY" \
  "https://reviewboard.olympus.f5net.com/api/review-requests/<RB_ID>/reviews/" \
  | python3 -m json.tool
```

---

## One-Liner: Full RB Summary for a Bug

```bash
RB_ID=343502
curl -s -H "Authorization: token $REVIEWBOARD_API_KEY" \
  "https://reviewboard.olympus.f5net.com/api/review-requests/$RB_ID/" \
  | python3 -c "
import sys, json
r = json.load(sys.stdin)['review_request']
print('Summary:', r['summary'])
print('Bugs:', r['bugs_closed'])
print('Branch:', r['branch'])
print('Approved:', r['approved'])
print('Changenum:', r['changenum'])
"
```

---

## When to Use This

**Phase 1 (Triage):** If Bugzilla bug has a `See Also` RB link or `depends_on` bug with a prior fix attempt:
1. Extract RB ID from the URL (e.g., `https://reviewboard.olympus.f5net.com/r/343502/` → `343502`)
2. Fetch the raw diff to understand what was tried before
3. Fetch reviews to see why it was rejected (open issues, ship-it status)

**Phase 3 (RCA):** Use prior RB diff to confirm or rule out previously identified root causes.

**Phase 6 (Test Plan):** After fix is verified, create a new RB using `rbt post` (see below).

---

## Creating a New Review Request

```bash
# Requires rbt (Review Board Tools) and .reviewboardrc in workspace root
rbt post \
  --server https://reviewboard.olympus.f5net.com \
  --repository tmos \
  --branch bugs-staging \
  --description "<test plan summary>" \
  --bugs-closed <bug_id>
```

If `rbt` is unavailable, guide user to upload patch manually at:
`https://reviewboard.olympus.f5net.com/r/new/`
