### How local changes become a new release on **PyPI**

Below is the typical workflow you use when you have finished a set of local changes (like the ones we just committed) and you want those changes to appear as a new version of the **logflash** package on PyPI.

| Step | Command | What it does | Why it matters |
|------|---------|--------------|----------------|
| **1. Bump the version** | Edit the `version` field in `pyproject.toml` (e.g. `0.2.0 → 0.2.1`). | PyPI only accepts a **new** version number; the same version cannot be uploaded twice. | Guarantees a clean, traceable release. |
| **2. (Optional) Verify the build locally** | `python -m pip install --upgrade build twine`<br>`python -m build` | Generates the source distribution (`.tar.gz`) and the binary wheel (`.whl`) in the `dist/` folder. | Lets you inspect the artefacts before publishing. |
| **3. Run the test‑suite** | `pytest -q` (or whatever test command you added) | Makes sure the new code still passes all checks. | Prevents accidental broken releases. |
| **4. Upload to the **Test PyPI** (sanity check)** | `python -m twine upload --repository testpypi dist/*` | Sends the wheels to <https://test.pypi.org> where you can install them with `pip install -i https://test.pypi.org/simple/ logflash`. | Gives you a safe “dry‑run” before the real release. |
| **5. Upload to the real PyPI** | `python -m twine upload dist/*` | Publishes the files to <https://pypi.org/project/logflash/>. | Makes the new version publicly available. |
| **6. Tag the commit (optional but recommended)** | `git tag -a v0.2.1 -m "Release 0.2.1"`<br>`git push origin v0.2.1` | Marks the exact commit that produced the release. | Helps trace the source of a PyPI version. |

#### Full command sequence you would run in the project root

```bash
# 1️⃣  bump version in pyproject.toml (manual edit)

# 2️⃣  make sure build tools are up‑to‑date
python -m pip install --upgrade build twine

# 3️⃣  create the distribution files
python -m build          # creates dist/*.tar.gz and dist/*.whl

# 4️⃣  run your test suite (already covered by CI, but you can do it locally)
pytest -q

# 5️⃣  (optional) upload to Test PyPI first
python -m twine upload --repository testpypi dist/*

# 6️⃣  upload to the official PyPI
python -m twine upload dist/*

# 7️⃣  tag the release in git (helps future debugging)
git tag -a v0.2.1 -m "Release 0.2.1"
git push origin v0.2.1
```

#### What each tool does

| Tool | Role |
|------|------|
| **`build`** (`python -m build`) | Calls *setuptools* (or *poetry*) under the hood to produce a **source distribution** and a **wheel** that are PEP‑517 compliant. |
| **`twine`** (`python -m twine upload`) | Securely authenticates with PyPI (using your `~/.pypirc` or environment variables) and uploads the artefacts. It never runs arbitrary code from the package, which makes it safe for publishing. |
| **`pytest`** | Runs the unit‑tests we added (`tests/…`). CI already does this, but a local run gives you immediate feedback. |
| **Git tags** | Provide a one‑to‑one mapping between a PyPI version and a git commit, making it easy to trace back to the exact source state. |

#### Quick checklist before you press **Enter**

1. **Version number updated** in `pyproject.toml`.  
2. All **tests pass** (`pytest` finishes with “0 failed”).  
3. `include_package_data = true` (already added) ensures the JSON/YAML rule files are packaged.  
4. `twine` is configured with your PyPI credentials (either via `~/.pypirc` or the `TWINE_USERNAME/TWINE_PASSWORD` environment variables).  

Once those conditions are satisfied, run the commands above and your new `logflash` release (with the extensibility improvements, YAML support, tests, docs, and CI) will be live on PyPI.