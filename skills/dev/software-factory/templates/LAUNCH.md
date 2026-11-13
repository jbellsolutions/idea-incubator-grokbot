# Launch checklist: <Product>

Do these in order. Each step should take a couple of minutes.

## 1. GitHub (repo + free website)
1. If needed, log in to GitHub in Terminal: `gh auth login`.
2. Publish yourself from the bot's build (the bot never does this): `/opt/incubator/builds/products/<slug>`. Create `<GITHUB_OWNER>/<slug>` (public only on your word), push, turn on GitHub Pages from `/docs`, and upload `<release file>` as a Release.
3. Website: `https://<GITHUB_OWNER>.github.io/<slug>/`

## 2. Gumroad
1. New product → paste everything from `marketing/listing.md`.
2. Check that the URL slug matches `CONFIG.gumroad` in `docs/index.html`.
3. Upload `<release file>`. Buy it once with a 100%-off code to test the download.

## 3. Zy AI Academy (Skool)
1. Add the release file (or a link to the GitHub Release) to the community's apps section.
2. Post `marketing/skool-post.md` with its screenshots.

## 4. Social
1. Record the video from `marketing/social.md` (shot list included).
2. Post it with one of the short posts. Link to the website.

## 5. Tell the factory
Move the item to **Launched** in `/opt/incubator/state/factory/board.md` (or add `> launched` under it and the next run will).
