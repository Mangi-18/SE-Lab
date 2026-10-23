# Lab 5 — Issues Found in bike_share_stations.py

| Issue | Type | Line(s) | Description | Fix Approach |
|-------|------|---------|-------------|--------------|
| SQL injection (Bandit B608) | Security (Medium) | 9 | `addStation` builds the INSERT query by concatenating `name` into the SQL string. A name containing a quote (e.g. `O'Brien Sq`) crashes the query, and a crafted name can run arbitrary SQL. | Use a parameterised query with `?` placeholders and pass the values as a tuple. |
| Insecure random for PIN (Bandit B311) | Security (Low, but security-relevant) | 22 | `random.randint` is a predictable pseudo-random generator; unlock PINs should not be guessable. | Use `secrets.randbelow(9000) + 1000`. |
| Mutable default argument (Pylint W0102) | Bug | 8 | `log=[]` is created once and shared across all calls, so the log keeps growing between unrelated calls. | Default to `None` and create a new list inside the function. |
| Try/except/pass + broad exception (Bandit B110, Pylint W0718) | Bug / Quality | 32–35 | `resetStation` catches every exception and silently ignores it, hiding real failures. | Catch only `sqlite3.Error`, report it, and return `False`. |
| Crash on unknown station | Bug | 39–40 | `hasBikes` indexes `row[0]` without checking `row`; an unknown id gives `row = None` → `TypeError`. | Check `row is None` before indexing. |
| Inconsistent return (Pylint R1710) | Quality | 14–18 | `rentBike` returns `True` or implicitly `None`. | Add an explicit `return False`. |
| Comparison to None (Flake8 E711, Pylint C0121) | Style | 40 | `== None` instead of `is None`. | Use `is None`. |
| Unused variable (Flake8 F841, Pylint W0612) | Quality | 27 | `summary` is computed but never used. | Remove it. |
| Naming convention (Pylint C0103) | Style | 8, 14, 21, 25, 31, 38 | Function names are camelCase; PEP 8 wants snake_case. | Rename (`add_station`, `rent_bike`, ...). |
| Missing docstrings (Pylint C0114/C0116) | Style | 1, all functions | No module or function docstrings. | Add docstrings. |
| Long lines / trailing whitespace (Flake8 E501, W291; Pylint C0301, C0303) | Style | 5, 9, 15, 17, 26, 27, 33, 39 | Lines exceed 79 chars; trailing spaces on line 27. | Wrap lines; delete trailing spaces. |
