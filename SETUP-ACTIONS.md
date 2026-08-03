# Enable wow-factor widgets (one-time setup)

Your profile README is live. The **3D graph** and **snake animation** need GitHub Actions.

## Option A — GitHub website (easiest)

1. Open https://github.com/Mohammad-Raees/Mohammad-Raees
2. Create file `.github/workflows/profile-3d.yml` with the contents below
3. Create file `.github/workflows/snake.yml` with the snake contents below
4. Go to **Actions** → allow workflows → run each workflow once (**Run workflow**)

### `.github/workflows/profile-3d.yml`

```yaml
name: GitHub-Profile-3D-Contrib

on:
  schedule:
    - cron: "0 0 * * *"
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Generate 3D Contrib
        uses: yoshi389111/github-profile-3d-contrib@0.7.1
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          USERNAME: Mohammad-Raees
      - name: Commit & Push
        run: |
          git config user.name github-actions
          git config user.email github-actions@github.com
          git add -A profile-3d-contrib
          git diff --staged --quiet || (git commit -m "chore: update 3D contribution graph" && git push)
```

### `.github/workflows/snake.yml`

```yaml
name: Generate Snake

on:
  schedule:
    - cron: "0 0 * * *"
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-latest
    permissions:
      contents: write
    steps:
      - uses: actions/checkout@v4
      - uses: Platane/snk/svg-only@v3
        with:
          github_user_name: Mohammad-Raees
          outputs: |
            dist/github-contribution-grid-snake.svg
            dist/github-contribution-grid-snake-dark.svg?palette=github-dark
      - uses: crazy-max/ghaction-github-pages@v3
        with:
          target_branch: output
          build_dir: dist
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

## Option B — New PAT with `workflow` scope

Create a classic PAT that includes **workflow**, then ask the assistant to push the workflow files.

Until the 3D workflow runs once, the 3D image may show broken — stats/trophies/streak still work immediately.
