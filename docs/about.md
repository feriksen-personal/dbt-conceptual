# Why I Built This

<div align="center">
  <img src="assets/author-photo.jpg" alt="Fridthjof Eriksen" width="140" style="border-radius: 50%; margin-bottom: 16px;" />
  <p><strong>Fridthjof Eriksen</strong><br/>
  <em>Data Architect · 30 years in the field</em></p>
</div>

---

Over the last decade, I've watched how our roles as data architects have shifted.

We went from modeling everything upfront — collaborating with the team during implementation, validating, coaching, guiding as we went along. That was the pattern. The architect owned the model, and the model came first.

Then things started to change. Data engineers began doing more of the modeling "on the fly," and our role became one of ensuring coherence: does this align with the existing model? Are we following the same patterns, naming conventions, metadata standards? We were no longer the only ones modeling — we became guides, but still with responsibility for the final outcome.

This pattern sped up delivery. We were no longer a bottleneck. And quite frankly, it felt right. Empowering your team to take individual ownership of the model is a good thing.

But in doing so, we found ourselves in a quandary: what about our typical ERD artifacts?

They lived outside the codebase. Outside the automated CI pipelines. It became a never-ending loop of trying to keep diagrams in sync with reality. The model said one thing; the code said another. And every quarter, someone would ask: "Is this diagram still accurate?" And the honest answer was usually: "Probably not."

---

## The Attempts

Many brave and good attempts have been made to resolve this disconnect.

Traditional ER tooling — ERwin, ER/Studio — with adapted processes. More modern tools like SqlDBM or dbdiagram.io with their DBML approach. These efforts are good, and they may work for your situation.

But I kept finding the same fundamental problem: **codebase here, models out-of-band there**. And in my experience, that disconnect will always allow drift to occur. It's not a question of discipline or process. It's structural. If the model lives somewhere else, it will eventually diverge from reality.

I've been outspoken about this being broken — within the community and in my work — for a long time now.

---

## What I Realized

Eventually, a few things became clear to me:

**The codebase is the reality.** Look at how dbt handles documentation — not as a standalone activity, but as a first-class citizen embedded in the code. That's the right pattern.

**The full conceptual→logical→physical cascade is less relevant for analytics.** In transactional systems, you might need the full ceremony. In analytics, dbt *is* your logical and physical layer. Trying to maintain all three separately creates more friction than value.

**The conceptual model is the most important one.** It's the bridge between the data team and business stakeholders. It's the shared vocabulary. If you can only keep one layer alive, keep that one.

**Lightweight matters.** It has to work both bottom-up (discover what exists) and top-down (define what should exist). If it's heavy, it won't get adopted.

**Automation is mandatory.** CI/CD, validation, drift reports — these aren't nice-to-haves anymore. If the model doesn't validate automatically, it will drift. That's just how teams work now.

**It has to live in the codebase.** Not beside it. Not linked to it. In it.

---

## The Idea

So I started thinking: what if you could unlock all of this by adding a single tag to any given model, plus a small configuration file for the conceptual layer?

No parallel workflows. No separate systems. No large time-consuming efforts.

Add an optional UI on top. A few additional features. And you have something that lets you keep the conceptual model alive — without being invasive, without requiring everyone to change how they work.

That was the basic idea that evolved into dbt-conceptual.

---

## Who I Am

I'm **Fridthjof Eriksen** — a data architect with three decades across telecom, consulting, and financial services. Nordic institutions, Swiss private banking, central banking infrastructure. Environments where data governance isn't optional and where architecture decisions compound over years.

I've seen models I built in 2005 still running in production. I've also seen beautifully documented conceptual models abandoned within months because they couldn't keep pace with delivery.

This tool is my attempt to bridge that gap — to keep the valuable part of conceptual modeling alive in a world that ships daily.

Maybe it helps.

---

## Connect

- [LinkedIn](https://www.linkedin.com/in/eriksenpl/)
- [GitHub](https://github.com/dbt-conceptual)
