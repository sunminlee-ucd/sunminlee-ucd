# Hi, I'm Sunmin Lee

**Backend-focused software developer based in Dublin, Ireland.**

I am completing an **MSc in Computer Science at University College Dublin**, where I received the **Global Excellence Scholarship**. I build applications that connect useful user workflows to backend services, cloud infrastructure, and browser or mobile clients.

My main interests are backend engineering, reliable background processing, API design, and making AI-backed features controllable and inspectable.

[LinkedIn](https://www.linkedin.com/in/sunmin-dev/) · [Email](mailto:sunmin.lee@ucdconnect.ie)

## Featured engineering projects

| Project | The need | What I am building | Main technologies |
| --- | --- | --- | --- |
| [Subtitle Companion](https://github.com/sunminlee-ucd/subtitle-companion-showcase) | Understand and study dialogue when preferred subtitles are unavailable | Timing-safe translation, authorized subtitle delivery, synchronized overlays, and study workflows across Chrome and Android | Python, FastAPI, JavaScript, Kotlin, Supabase, Docker, Cloud Run |
| [PointBuild](https://github.com/sunminlee-ucd/pointbuild-showcase) | Turn a visual UI correction into the intended source edit | DOM-to-source targeting, token-backed preview, bounded changes, isolated Git staging, verification, and Undo | TypeScript, React, Vite, Babel, Node.js, Git, Playwright |
| [SwitchAI](https://github.com/sunminlee-ucd/switchai-showcase) | Choose and execute AI requests with explicit cost and capability constraints | Policy-based routing, provider adapters, bounded fallback, idempotency, reconciliation, and execution audit | TypeScript, Node.js, provider APIs, JSONL persistence |

The project pages explain the problem, product rationale, architecture, technology choices, core engineering decisions, and current limitations. Subtitle Companion is under active development; PointBuild and SwitchAI are local prototypes.

## What I focus on

- **Correctness at system boundaries:** preserve subtitle timing outside the language model, connect rendered UI targets to source context, and validate requests before provider execution.
- **Explicit recovery behavior:** retain background-job progress, make edits reversible, and distinguish failed requests from uncertain provider completion.
- **Controlled AI integration:** apply task and budget constraints, use deterministic processing where appropriate, and keep decisions explainable.
- **Usable workflows:** help users understand, preview, and control the result without requiring knowledge of the implementation pipeline.

## Technical toolkit

| Area | Technologies used in my projects |
| --- | --- |
| Backend | Python, FastAPI, TypeScript, Node.js, HTTP APIs |
| Data and identity | PostgreSQL, Supabase Auth/Storage, access policies, local JSONL persistence |
| Clients | JavaScript, React, Chrome extensions, Kotlin/Android |
| Cloud and delivery | Docker, Google Cloud Run, Cloud Run Jobs, Cloud Build, GitHub Actions |
| Verification | pytest, Ruff, Vitest, Playwright, Node.js test runner, JUnit, Robolectric |

## More public work

[Dublin Bikes](https://github.com/sunminlee-ucd/Project) is a team project for real-time and predictive bike-station availability. Its repository includes the application overview, architecture, and local setup.

## Reviewing private projects

My active product implementations remain private. The linked public showcases provide technical case studies; a technical walkthrough and scoped source-code review can be arranged on request.

I am interested in **backend and software engineering opportunities**, especially work involving APIs, cloud services, background jobs, and reliable AI integration.
