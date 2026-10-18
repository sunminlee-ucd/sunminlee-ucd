# Hi, I'm Sunmin Lee

**Backend-focused software developer · Dublin, Ireland**

I build applications that connect practical user needs with APIs, background jobs, and cloud services. My projects focus on keeping data trustworthy, making interrupted work recoverable, and integrating AI into workflows users can inspect and control.

**MSc Computer Science candidate, University College Dublin · Global Excellence Scholarship recipient**

Interested in **backend and software engineering opportunities**.

[LinkedIn](https://www.linkedin.com/in/sunmin-dev/) · [Email](mailto:sunmin.lee@ucdconnect.ie)

## Featured projects

### [Subtitle Companion](https://github.com/sunminlee-ucd/subtitle-companion-showcase)

**Watch and study with synchronized subtitles across Chrome and Android.**

When a preferred subtitle language is unavailable, viewers need translation that stays aligned with playback. I built the backend, browser extension, and Android client to connect subtitle requests, translation, authorized delivery, and study tools.

- **Core engineering:** preserve cue timing outside the language model; synchronize overlays with playback; separate background translation from customer requests.
- **Stack:** Python, FastAPI, JavaScript, Kotlin, Supabase, Docker, Google Cloud Run.
- **Stage:** implemented application workflows; active development.

[Architecture and decisions](https://github.com/sunminlee-ucd/subtitle-companion-showcase#core-engineering) · [Runnable cue-engine sample](https://github.com/sunminlee-ucd/subtitle-companion-showcase/tree/main/examples) · [Public-site screenshots and 20-second walkthrough](https://github.com/sunminlee-ucd/subtitle-companion-showcase#product-screenshots-and-public-ui-walkthrough)

### [Brand Lens / Bunjang](https://github.com/sunminlee-ucd/bunjang-showcase)

**Turn resale listing observations into evidence for product research.**

An asking price or a sold label alone cannot establish what sold, when, or for how much. I built a research workflow that preserves observation history, keeps sold and reserved states separate, and helps users review comparable listings.

- **Core engineering:** checkpoint collection for recovery; share progress and cancellation across web and worker processes; retain uncertain job submissions for reconciliation.
- **Stack:** Python, JavaScript, SQLite, Firestore, Cloud Run Jobs, Pillow.
- **Stage:** deployed web application; collection and analysis under active development.

[Deployed app — sign-in required](https://bunjang-web-x5omgavbua-du.a.run.app/) · [Architecture and decisions](https://github.com/sunminlee-ucd/bunjang-showcase#core-engineering) · [Runnable sample and visual output](https://github.com/sunminlee-ucd/bunjang-showcase#runnable-example)

## More engineering work

| Project | Problem and engineering focus | Stage |
| --- | --- | --- |
| [Dublin Bikes](https://github.com/sunminlee-ucd/Project) | Team application for live and predicted bike-station availability. Python, Flask, MySQL, SQLAlchemy, XGBoost. | Public team project |
| [PointBuild](https://github.com/sunminlee-ucd/pointbuild-showcase) | Connect a selected interface element to source code, preview supported edits, and make changes reversible. React, TypeScript, Vite, Babel, Git worktrees. | **Unfinished local prototype** |
| [SwitchAI](https://github.com/sunminlee-ucd/switchai-showcase) | Apply task and budget policies before AI-provider execution, with bounded fallback and request reconciliation. TypeScript, Node.js. | Local prototype; deterministic/mock demo |

## How I approach engineering

- **Keep critical rules explicit.** Subtitle timestamps stay deterministic; observed listing states remain separate from inferred transactions.
- **Design for interruption.** Persist progress, provide cancellation, and distinguish a definite failure from an operation whose outcome is still unknown.
- **Make decisions reviewable.** Pair implementation choices with their rationale, trade-offs, limitations, and small runnable examples.

## Technical toolkit

**Backend:** Python · FastAPI · TypeScript · Node.js · HTTP APIs  
**Data and identity:** PostgreSQL · SQLite · Firestore · Supabase Auth and Storage  
**Clients:** JavaScript · React · Chrome extensions · Kotlin / Android  
**Cloud and delivery:** Docker · Cloud Run · Cloud Run Jobs · Cloud Build · GitHub Actions

## Review code in a few minutes

Each showcase explains the problem, my role, architecture, and current limits. These focused samples run on synthetic inputs without product accounts, cloud credentials, or paid AI calls.

| Public sample | What to inspect | Automated checks |
| --- | --- | --- |
| [Subtitle cue engine](https://github.com/sunminlee-ucd/subtitle-companion-showcase/tree/main/examples) | Cue timing, overlaps, offsets, and playback boundaries | [Tests and demo](https://github.com/sunminlee-ucd/subtitle-companion-showcase/actions/workflows/sample-checks.yml) |
| [Image similarity](https://github.com/sunminlee-ucd/bunjang-showcase/tree/main/examples) | Color/layout/edge features, similarity scores, and invalid-input handling | [Tests and visual demo](https://github.com/sunminlee-ucd/bunjang-showcase/actions/workflows/sample-checks.yml) |
| [UI target identity](https://github.com/sunminlee-ucd/pointbuild-showcase/tree/main/examples) | Distinguish repeated elements while preserving identity across rerenders | [Tests and demo](https://github.com/sunminlee-ucd/pointbuild-showcase/actions/workflows/sample-checks.yml) |
| [AI route selection](https://github.com/sunminlee-ucd/switchai-showcase/tree/main/examples) | Enforce quality/reliability constraints before cost selection | [Tests and demo](https://github.com/sunminlee-ucd/switchai-showcase/actions/workflows/sample-checks.yml) |

The checks cover these public samples; they do not certify the full private applications or deployed services.

Full product implementations remain private. **Technical walkthroughs and scoped source-code reviews are available on request.**
