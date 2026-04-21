# Git Interview Prep

## 📑 Table of Contents

1. [Git Merge vs Rebase](#git-merge-vs-rebase)
   - [Git Merge](#git-merge)
   - [Git Rebase](#git-rebase)
   - [Direct Comparison](#direct-comparison)
   - [Interview Explanation](#interview-explanation)

---

## Git Merge vs Rebase

### Git Merge

**📌 What it does**

- Combines two branches
- Keeps original history
- Creates a merge commit (NC)

**🧩 Diagram (Simplified)**

**Before merge:**

```
main:     C1 ── C2 ── C3
             \
feature:      F1 ── F2
```

**After merge:**

```
main:     C1 ── C2 ── C3 ── NC
             \             /
feature:      F1 ── F2 ───
```

**🔍 Key Points**

- History is non-linear
- Merge commit = NC
- Safe for team usage
- Easy to track branches

---

### Git Rebase

**📌 What it does**

- Moves feature commits on top of latest main
- Rewrites history
- No merge commit

**🧩 Diagram (Simplified)**

**Before rebase:**

```
main:     C1 ── C2 ── C3
             \
feature:      F1 ── F2
```

**After rebase:**

```
main:     C1 ── C2 ── C3 ── F1' ── F2'
```

👉 **Note:**

- F1 → F1′
- F2 → F2′ (new commit IDs)

**🔍 Key Points**

- History becomes linear
- Cleaner git log
- Old commits are replaced ❌
- Risky if used on shared branches

---

### Direct Comparison

| Feature | Merge | Rebase |
|---------|-------|--------|
| History | Preserved | Rewritten |
| Structure | Branching | Linear |
| Extra commit | Yes (NC) | No |
| Commit IDs | Same | Changed |
| Safety | Safe | Risky |
| Use case | Team collaboration | Clean history |

---

### Interview Explanation

**🎯 Interview Explanation (short)**

👉 "Merge combines branches and preserves history with a merge commit, while rebase rewrites the feature branch commits on top of the latest main branch, creating a clean linear history."
