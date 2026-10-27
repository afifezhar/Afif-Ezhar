# Afif-Ezhar

Afif's content workspace. Reply to him in Malay (casual register); write code, commits and PRs in English.

## Talking-head video edits

Every talking-head / selfie video edit for TikTok, Reels or Shorts follows the house process and style in
`.claude/skills/talking-head-edit/` (`SKILL.md` for the steps and his standing preferences, `style.md` for the
design spec). Load that skill before planning, storyboarding, captioning, adding b-roll, making a cover or
rendering.

- Reference edit: `video-edit/` ("Orang masih percaya ke?").
- Reusable scripts: `video-edit/scripts/` (retouch, voice, transcribe, safe-zone and cut checks).
- Large media (raw takes, renders, final MP4s) stays out of git. The raw takes come from his Google Drive.
- `ELEVENLABS_API_KEY` is in the environment (and `.env.local`, which is gitignored). Never print or commit it.
