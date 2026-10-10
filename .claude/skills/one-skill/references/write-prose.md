# Write prose — text a human reads

**Read this when:** thesis, journal, report, memo, professional email, landing copy, docs, PR/issue bodies

**Layer:** be-brief writes; antislop-copywriting de-sloppens

Loaded on demand: the always-on rules live in the skill's `SKILL.md`. The
bodies below are upstream text carried verbatim, with the per-section
provenance and every declared edit listed in `SOURCES.md` beside this file.

| section | from | load |
|---|---|---|
| [Be brief — professional prose with zero wasted words](#be-brief-professional-prose-with-zero-wasted-words) | `local` | always |
| [Caveman be brief — document modes, intensity, Indonesian](#caveman-be-brief-document-modes-intensity-indonesian) | `local` | always |
| [antislop-copywriting — tone, rhythm, honesty of claims](#antislop-copywriting-tone-rhythm-honesty-of-claims) | `anti-slop-fork` | always |
| [Phrase catalog — EN + ID filler to cut](#phrase-catalog-en-id-filler-to-cut) | `local` | always |

---

## Be brief — professional prose with zero wasted words

> `local` / `be-brief-output` / anything a human reads as a finished artifact

> *(not carried here: Reference material, Language. Stated once for the whole skill, in SKILL.md, instead of repeated per section. The links those sections carried now resolve inside this file.)*

The documented evidence base for "be brief" is the project itself, plus a trigger
phrase in official caveman's frontmatter. Everything below is this repo's contract,
tuned for prose whose reader is a human being who was not in the room.

### The one rule

> **Short. But complete sentences. Professional register.**

Not broken grammar. Not telegraph style. Not caveman fragments. This is the
register the SkillOpt evaluator scores under `be_brief`.

### The deletion test

For every sentence: *if I delete this, does the reader lose a fact, a number, a
name, a decision, or a logical link?*

- No loss → cut it.
- Real loss → keep it, exactly as precise as it was.

### Output contract

- Complete sentences. Professional register. **Never broken grammar.**
- No pleasantries, no "Sure!", no process commentary, no note on what was cut.
- Preserve every number, name, date, unit and citation **exactly**.
- Preserve genuine hedges — "may", "is associated with", "in this sample".
- Preserve logical connectors that carry real meaning.
- Never invent abbreviations (`cfg`/`impl`/`req`/`res`/`fn`) and never use `→`
  in prose. This is a hard rule from official caveman and it applies here too.
- No emoji, no markdown decoration, no table where a sentence works.

### Feedback loop — self-check before you answer

- [ ] Every number, name, date, unit and citation from the source is still present?
- [ ] Every genuine hedge survived?
- [ ] Every logical connector that carries real meaning survived?
- [ ] Code, commands, paths, LaTeX and error strings byte-identical?
- [ ] No invented abbreviation, no `→`?
- [ ] Shorter than the source, without any loss?

If a check fails, fix it first. Do not announce the check.

### Scope — where this applies

1. **Document focus** — emails, memos, theses, papers, personnel/utility
   reports, summaries. Be brief applies fully, in full prose.
2. **No-code** — applies fully wherever no code is involved.
3. **Coding sessions** — apply to the prose *around* code. Code, commands, paths
   and errors stay byte-exact.

### Intensity

| Level | Use |
|---|---|
| **lite** | Obvious filler only. Emails, journal submissions, formal reports. |
| **full** | Full deletion test. *(default)* |
| **ultra** | Maximum density, all facts kept. Summaries, token-limited contexts. |

### Cut lists (be-brief-output)

> carried verbatim from `upstream/local/variants/be-brief-output/references/cut-lists.md`, the same upstream directory as `be-brief-output`.

### English — cut

| Cut | Example → result |
|---|---|
| Pleasantries | "Sure! I'd be happy to help." → *(delete)* |
| Process commentary | "Let me check the file." → *(delete)* |
| Tool narration | "I ran the test suite." → *(delete)* |
| Meta-commentary | "I trimmed this for brevity." → *(delete)* |
| Qualifiers | "It is important to note that" → *(delete)* |
| Wordy connectives | "in order to" → "to" |
| Redundant framing | "The reason is that" → "Because" |
| False urgency | "Careful — don't skip this" → *(state the risk plainly)* |
| Hedged filler | "It seems like maybe" → *(state it, or drop it)* |
| Restating the question | *(delete)* |

### Indonesian — cut

| Potong | Contoh → hasil |
|---|---|
| Basa-basi | "Baik, saya akan membantu." → *(hapus)* |
| Narasi proses | "Mari saya cek filenya." → *(hapus)* |
| Narasi tool | "Saya sudah menjalankan test." → *(hapus)* |
| Komentar meta | "Saya ringkas agar hemat token." → *(hapus)* |
| Pengisi | "perlu diketahui bahwa", "dapat dikatakan" → *(hapus)* |
| Sambung panjang | "dengan tujuan untuk" → "untuk" |
| Bingkai ulang | "Alasannya adalah karena" → "Karena" |
| Urgensi palsu | "Hati-hati ya, jangan sampai" → *(nyatakan risikonya)* |

### Never cut

- Numbers, units, dates, magnitudes
- Names, identifiers, versions
- Citations and citation keys
- Genuine hedges: "may", "is associated with", "in this sample", "kemungkinan"
- Logical connectors that carry real meaning: therefore, because, however
- Code, commands, file paths, LaTeX
- Exact error strings
- The decision itself, and the reason for it

### Never invent abbreviations

The official caveman set is: `cfg` · `impl` · `req` · `res` · `fn`

If the user did not write the abbreviation, do not use it. **No `→` in prose** —
write "to", "becomes", "yields".

### Before / after (be-brief-output)

> carried verbatim from `upstream/local/variants/be-brief-output/examples.md`, the same upstream directory as `be-brief-output`.

### Professional email

**Source request:** "Draft an email telling Dr. Rahman the ethics review document
needs revision before the 15 Nov deadline, and I'm available Wednesday."

**Wrong — too long:**
> I hope this email finds you well. I am writing to bring to your attention the
> fact that the ethics review document that you submitted will require some
> revisions before we are able to move forward with the approval process. The
> deadline for this is the 15th of November. Please let me know if you would
> like to discuss — I am available on Wednesday.

**Right:**
> The ethics review document needs revision before the 15 Nov deadline. I'm
> available Wednesday if you'd like to discuss the required changes.

Every fact survives: the document, the action, the date, the availability.
The pleasantries did not carry any of them.

### Report summary

**Source:**
> The pump at Station 4 failed on 3 March after roughly 1,240 operating hours.
> Maintenance records indicate that the seals were replaced in January, which
> suggests that the failure is probably related to the installation procedure
> rather than to the age of the component itself.

**Right:**
> Pump at Station 4 failed 3 March after ~1,240 operating hours. Seals were
> replaced in January, so the failure is probably related to the installation
> procedure rather than component age.

**Wrong:** dropping "probably" — that hedge is a real fact about confidence, and
the evaluator counts it as a lost hedge.

### Where code appears

**Source:** "The build fails with `ModuleNotFoundError: No module named 'skillopt'`.
I already ran `pip install -e skillopt-integration`."

**Right:**
> The build fails with `ModuleNotFoundError: No module named 'skillopt'`.
> The editable install did not provide the package. Check that
> `skillopt-integration/` contains a `pyproject.toml`, then retry
> `pip install -e skillopt-integration`.

The error string is byte-exact. Only the surrounding prose was compressed.

## Caveman be brief — document modes, intensity, Indonesian

> `local` / `caveman-be-brief-app` / thesis / journal / report drafting and review in the app

> *(not carried here: THE CORE RULE: Deletion Test, LANGUAGE, INTENSITY LEVELS, RALPH WIGGUM LOOP (separate skill — optional), AUTO-CLARITY. Stated once for the whole skill, in SKILL.md, instead of repeated per section. The ralph loop is carried once, in think-first.)*

All-in-one daily-driver for thesis, journals, reports, and office documents.

Three layers working together:
1. **Grug thinking** (internal) — plan, fear, simplify
2. **Caveman speaking** (external) — cut the fluff, keep the facts
3. **Ralph loop** (optional, separate skill) — iterative polish when you have time

### TWO MODES — NEVER MIX

#### MODE 1: INTERNAL REASONING (GRUG VOICE)
- Used for: planning, risk assessment, tool selection, strategy
- Voice: lowercase, broken grammar, blunt, caveman-style
- Audience: yourself only (internal monologue)
- NEVER shown to user directly

#### MODE 2: EXTERNAL OUTPUT (PROFESSIONAL VOICE)
- Used for: all user-facing responses, document edits, summaries
- Voice: formal, academic, polite, precise, nuanced
- Audience: the user
- ALWAYS what the user sees
- Style: professional prose with zero wasted words — NOT broken grammar, NOT cartoon caveman speech

### GRUG INTERNAL REASONING RULES

- lowercase, broken grammar, "grug" not "I"
- short sentences, max 3 per thought beat
- simple words only. No markdown emphasis internally.
- Length budgets: simple query <80 words internal; typical task 120–250 (aim 150); complex up to 400. Over 400 = recapping, cut.
- Process flow for every task: **SNIFF** (what user want?) → **FEAR** (what go wrong?) → **PLAN** (small steps) → **ACT** (execute, verify) → **SPEAK** (professional output)
- Abbreviation warning: never invent prose abbreviations (cfg/impl/req) — tokenizer splits them same as full word = zero savings. Standard acronyms OK (API, HTTP, PDF, APA, MLA, DOI, SQL). No arrows (→) — own token, save nothing.

### WHAT TO CUT (English)

- **Throat-clearing openers:** "It is important to note that...", "This paper aims to...", "As we all know..."
- **Stacked hedges:** "could possibly perhaps" → "may"; keep at most one hedge per claim
- **Empty transitions:** "Moving forward,", "That being said,", "At the end of the day,"
- **Restated conclusions:** saying a finding, then repeating it as "In conclusion..."
- **Nominalizations:** "conduct an analysis of" → "analyze"; "make a decision on" → "decide"; "provide assistance to" → "help"
- **Vague qualifiers:** "a significant number of" → the actual figure, if known (never invent one)
- **Redundant pairs:** "each and every", "full and complete", "past history", "end result", "completely eliminate" → one word
- **Padding passive voice:** "It was determined by the team that..." → "The team found..." (leave passive when actor unknown or field convention)
- **Writing-about-the-writing:** "As mentioned previously,", "This section will now discuss..."
- **Verbal-tic intensifiers:** "very", "really", "quite", "basically", "actually" as reflex; upgrade real emphasis ("very important" → "critical")

### APA YANG DIPOTONG (Bahasa Indonesia)

- **Pembuka basi:** "Perlu diketahui bahwa...", "Perlu dicatat bahwa...", "Dapat disimpulkan...", "Pada dasarnya..."
- **Hedge bertumpuk:** "mungkin bisa jadi", "diduga kemungkinan besar" → satu hedge saja
- **Transisi kosong:** "Ke depannya,", "Dengan kata lain,", "Pada akhirnya,", "Tidak perlu dikatakan lagi..."
- **Nominalisasi:** "melakukan analisis terhadap" → "menganalisis"; "mengambil keputusan" → "memutuskan"; "memberikan bantuan" → "membantu"
- **Kata ganda:** "benar-benar menghilangkan", "sangat penting sekali", "hasil akhir", "mulai dari awal" → satu kata
- **Intensifier:** "sangat", "sekali", "sebenarnya", "pokoknya" bila tanpa makna tambahan
- **Menulis-tentang-tulisan:** "Seperti yang telah disebutkan sebelumnya,", "Bagian ini akan membahas..."

### WHAT NEVER TO CUT

- **Facts** — numbers, names, dates, citations, specific findings. Never invent figures.
- **Genuine hedges** in technical, medical, legal, financial claims. "May cause", "is associated with" carry real information. When in doubt, keep the hedge.
- **Real logical connectors** — "because", "although", "therefore", "however" (and "tetapi", "karena", "oleh karena itu").
- **Required structure** — headings, citation formats, methodology sections.
- **The author's voice** when editing someone's draft. Cut padding, don't sand off their phrasing.

### CODE PRESERVATION (critical for file generation)

When generating code to assemble files (Python with python-docx, R, Pandoc pipelines, etc.):
- **Code blocks must remain byte-for-byte exact. Never compress code.**
- Surrounding prose may be compressed; the code itself is a technical artifact, not prose.
- Inline code, file paths, LaTeX equations, citation keys: preserved exactly.

### GRUG BELIEFS (guide internal thinking)

- **Complexity is the eternal enemy.** Simple beats clever. Say "no" to features/sections that add complexity without value.
- **80/20 is the way.** 80 percent of want with 20 percent of effort. Good enough beats perfect.
- **Respect the fence.** Understand why a section exists before removing it (Chesterton's Fence).
- **Done > perfect.** Ugly draft exist > perfect draft in head. Fix later.
- **Trust but verify.** AI output looks right but isn't always. Check every number, citation, claim. LLM good at first 70%, last 30% takes long — verify.
- **Small chunk strategy.** One section at a time, not whole thesis at once.
- **Premature polish very bad.** Draft first. Polish after content exists.
- **Documents fragile.** Save a copy before big edits. Never overwrite originals (use _v2, _backup).
- **Citations are anchors.** Drop one, ship sink. Check every ref.
- **Fear FOLD** (Fear Of Looking Dumb). Admit confusion. Complex = bad, not clever.
- **Meetings like salt.** Agenda or no meet. Too many reviewer feed the demon.
- **File naming simple.** YYYY-MM-DD prefix. v1, v2, final.

### WORKED EXAMPLE (English)

**Input (61 words):** It is important to note that, over the course of the observation period, a significant number of the shipments that were processed experienced delays which could possibly be attributed to a variety of different factors, including but not limited to handover procedures between shifts. In conclusion, it can be seen that handover procedures were found to be a major contributing factor.

**Output (16 words):** Many shipments processed during the observation period were delayed, mainly due to gaps in shift-handover procedures.

### WORKED EXAMPLE (Bahasa Indonesia)

**Input:** Perlu diketahui bahwa selama periode observasi, sejumlah besar pengiriman yang diproses mengalami keterlambatan yang kemungkinan besar bisa disebabkan oleh berbagai macam faktor yang berbeda, termasuk namun tidak terbatas pada prosedur serah terima antar shift. Sebagai kesimpulan, dapat dilihat bahwa prosedur serah terima merupakan faktor utama.

**Output:** Banyak pengiriman selama periode observasi terlambat, terutama karena celah prosedur serah terima antar shift.

### PROCESS FLOW

1. **SNIFF** — what does the user want? (Fix? Summarize? Create? Review?)
2. **FEAR** — what could go wrong? (Data loss? Wrong tone? Miss citation? Overwrite file?)
3. **PLAN** — small steps. Read which part? Save backup where?
4. **ACT** — execute one step. Check result. Verify tool success.
5. **SPEAK** — translate Grug plan to professional output. Full grammar. Proper terms.

### SAFETY PROTOCOLS

1. NEVER overwrite original files — create `_v2`, `_fixed`, `_backup`.
2. NEVER output Grug voice to user. Internal only.
3. NEVER strip scientific hedging unless explicitly asked.
4. ALWAYS verify tool success before claiming completion.
5. PRESERVE nuance in external output.
6. CHECK citations before marking document complete.
7. PRESERVE code blocks exactly when generating file-assembly scripts.

### PERSISTENCE

Active until "stop caveman" / "stop grug" / "normal mode". Default intensity: full.

*Think like Grug. Speak like a Professor. Ralph off unless you need polish.*

## antislop-copywriting — tone, rhythm, honesty of claims

> `anti-slop-fork` / `antislop-copywriting` / product copy, landing text, and any persuasive or marketing-flavoured prose

> Anti Slop: Rules for AI Coding Agents. Copy & Text skill

> Part of the antislop system. Read together with `antislop.md` (the core). This skill deep-dives the copy and text concern: headlines, CTAs, tone, value propositions, and the patterns that make AI-written prose easy to spot. It references core rules by number and never duplicates or renumbers them. Load it when the task writes or edits marketing copy, product copy, landing-page text, or any prose meant for people to read.

### How to use this skill

- Load together with `antislop.md` whenever the task is copy or text work. The core holds the mechanism (the purpose test, the three tiers, the Delivery Gate) and the hard bans (R-02, R-15, R-16, R-17, R-18, R-36, R-38). This skill holds copy-specific depth that the core does not.
- Every pattern has the same shape: **The pattern**, **Why it reads as AI**, **Before** (the slop), **After** (the fix), with the governing core rule cited as R-XX.
- Two rules apply to everything below:
  - **Never invent facts** (R-17, R-36, R-38). A rewrite adds no fact, name, number, date, quote, or citation that is not in the source text or supplied by the user. Specificity comes from the source or the user, not from the rewrite. If a sentence needs real detail to work, ask for it or write the plain version without it.
  - **Do not over-sterilize.** Avoiding AI patterns is half the job. Copy with no voice is as obviously machine-made as copy full of AI tells (R-37). When a user supplies a voice, keep it.
- The Delivery Gate in the core remains the gate. The "Copywriting Skill Checklist" at the end of this file is the copy-specific supplement to run alongside it.

### Tone & Voice

#### Empty AI Vocabulary

- **The pattern:** verbs and abstract nouns stacked to sound impressive without saying anything: *unlock, elevate, empower, delve, showcase, testament, landscape (abstract), journey, robust, game-changer, next-level, seamless, cutting-edge, revolutionary*.
- **Why it reads as AI:** these words appear far more often in machine-written text. They signal intent to impress, not intent to inform, and they are the fastest way to mark a page as AI-generated.
- **Before:**
  > Unlock the power of seamless collaboration to elevate your team's journey to the next level.
- **After:**
  > Work with your team in one shared space.
- **Rule:** R-16 (buzzwords), R-36 (no fabricated claims).

#### Significance Inflation

- **The pattern:** "the future of X", "marking a pivotal moment", "a testament to", "revolutionizing", "a new era of".
- **Why it reads as AI:** the claim has no evidence behind it, and the sentence reads the same no matter what the product does. It is ceremony where content should be.
- **Before:**
  > Our platform is marking a pivotal moment in the evolution of team productivity, ushering in a new era of work.
- **After:**
  > Our platform cuts the time your team spends on status meetings.
- **Rule:** R-36 (no fabricated claims), C-5 (evidence over claims).

#### Empty Claims and Social Proof with No Evidence

- **The pattern:** "Trusted by thousands of teams", "industry-leading", "world-class", "loved by customers everywhere", with nothing named or verifiable.
- **Why it reads as AI:** a trust claim without evidence is a confession. It fills the space a real customer name, a real number, or a real use case should occupy.
- **Before:**
  > Trusted by thousands of teams worldwide. Industry-leading technology loved by customers everywhere.
- **After:**
  > Used by the support teams at [customer names, only if real]. If there are no real customers to name, cut the claim entirely.
- **Rule:** R-17 (data and numbers), R-18 (testimonials), R-36 (no fabricated claims), C-5.

#### Weasel Attributions

- **The pattern:** "Experts say", "industry observers", "people report", "leading analysts believe", with no one named.
- **Why it reads as AI:** the attribution exists to make an unsourced claim feel authoritative. If the authority is real, name it; if not, the claim does not get a costume.
- **Before:**
  > Experts say this approach dramatically improves conversion.
- **After:**
  > [Name the source or cut the sentence. Example with a real source: "In a 2024 study by [named firm], this approach improved conversion by [real figure]."]
- **Rule:** R-36, C-5.

#### Persuasive Authority Tropes

- **The pattern:** "at its core", "the real question is", "what really matters", "fundamentally", "the deeper issue", "the heart of the matter".
- **Why it reads as AI:** these phrases pretend to cut through noise to a deeper truth, then restate an ordinary point with extra ceremony.
- **Before:**
  > At its core, what really matters is whether your team can move faster.
- **After:**
  > Whether your team can move faster depends on how quickly you can merge changes.
- **Rule:** R-36.

#### Chatbot Closers

- **The pattern:** "I hope this helps!", "Let me know if you have any questions", "Would you like me to expand on this?", "You're welcome!".
- **Why it reads as AI:** these are conversation artifacts, not copy. They appear when model chat output is pasted straight into a deliverable.
- **Before:**
  > Here is an overview of our pricing. I hope this helps! Let me know if you'd like me to break down any tier.
- **After:**
  > Here is our pricing. The Starter tier includes three seats and community support.
- **Rule:** R-36.

#### Fake-Candid Openers

- **The pattern:** "Honestly?", "Let's be honest", "Here's the thing", "Real talk", as a theatrical pause before an ordinary point.
- **Why it reads as AI:** a person being honest usually just says the thing. The pause-and-reveal is manufactured intimacy.
- **Before:**
  > Is it worth the price? Honestly? It depends on how often you'll use it.
- **After:**
  > Whether it is worth the price depends on how often you'll use it.
- **Rule:** R-36.

#### Signposting Announcements

- **The pattern:** "Let's dive in", "Here's what you need to know", "In this article we'll explore", "Without further ado".
- **Why it reads as AI:** announcing what you are about to do instead of doing it is meta-commentary. It slows the reader and gives the text a tutorial-script feel.
- **Before:**
  > Let's dive into how caching works in Next.js. Here's what you need to know.
- **After:**
  > Next.js caches data at multiple layers, including request memoization, the data cache, and the router cache.
- **Rule:** R-36.

#### All-Caps Emphasis

- **The pattern:** a whole sentence, clause, or phrase in ALL CAPS inside a paragraph to shout emphasis: "The launch is ready and WE NEED TO MOVE NOW before the window closes."
- **Why it reads as AI:** caps-as-emphasis is a blunt instrument the model reaches for to manufacture urgency instead of writing emphasis into the sentence. In long text it reads as shouting, and it flattens the real peaks by making everything loud.
- **Before:**
  > This is our last chance to win this customer, and WE MUST ACT IMMEDIATELY before they choose a competitor.
- **After:**
  > This is our last chance to win this customer. If we do not respond today, they will choose a competitor.
- **Rule:** R-36. (R-06 covers uppercase labels with wide tracking as a design choice; this pattern is the prose case: caps inside a paragraph doing the emphasis work.)
- **Not a ban:** a genuine headline, a deliberately shouted line in a voice that shouts, or a single all-caps word used once as an accent can keep its caps. The tell is caps used sentence after sentence to do the emphasis the words should do. Minimize, do not strip every cap.

#### Actorless Passive

- **The pattern:** the passive voice with the actor deleted: "the decision was made to sunset the free tier", "the pricing page has been updated", "mistakes were made".
- **Why it reads as AI:** the model does not know who acted, so it writes around it. The team that shipped the thing does know, and says so. Deleting the actor also quietly removes accountability from the sentence, which is why the shape survives in corporate copy and nowhere else.
- **Before:**
  > The pricing page was updated to reflect the new tiers.
- **After:**
  > We rewrote the pricing page to show the new tiers.
- **Rule:** R-02 (text must feel natural and human).
- **Not a ban:** passive is the right choice when the actor is unknown, irrelevant, or deliberately withheld ("the server was restarted at 03:00"), and when the object is the real subject of the paragraph. The tell is passive chosen by default, page after page, with an actor that was available the whole time.

#### Inanimate Subject, Human Verb

- **The pattern:** an abstraction given agency: "the data tells us", "the design decides", "the complaint becomes a fix", "the roadmap wants to focus on retention".
- **Why it reads as AI:** it sounds active while naming nobody, so it passes a passive-voice check and still hides the actor. It also flatters the product, since a dashboard that "understands" is doing something no dashboard does.
- **Before:**
  > The dashboard understands what your team needs and surfaces the right numbers.
- **After:**
  > The dashboard opens on the three metrics your team checks every morning.
- **Rule:** R-02, R-16 (specific language over claims).
- **Not a ban:** ordinary product verbs are fine, and so are established idioms. "The report shows", "the form submits", "the filter narrows the list" describe what the thing does. The tell is a verb that needs a mind behind it: understands, knows, decides, wants, believes, cares.

### Rhythm & Structure

#### Rule of Three Overuse

- **The pattern:** every idea forced into a group of three to sound complete: "innovation, inspiration, and insights".
- **Why it reads as AI:** real lists have the number of items the content requires. A forced trio is a rhythm tell, and it appears across every section at once.
- **Before:**
  > Attendees can expect keynote sessions, panel discussions, and networking opportunities. They'll leave with innovation, inspiration, and industry insights.
- **After:**
  > The event includes talks, panels, and time for informal networking between sessions.
- **Rule:** R-05 (page structure), R-36.

#### Negative Parallelism and Tailing Negations

- **The pattern:** "It's not just X, it's Y", "Not only X, but also Y", and clipped fragments tacked on as emphasis: "no guessing", "no wasted motion".
- **Why it reads as AI:** the construction is a formula the model reaches for to sound emphatic, whether or not the emphasis is earned.
- **Before:**
  > It's not just a dashboard, it's a command center. The options come from the selected item, no guessing.
- **After:**
  > The dashboard shows the data you select. The options come from the selected item without forcing you to guess.
- **Rule:** R-36.

#### Aphorism Formulas

- **The pattern:** "X is the language of Y", "X is the currency of Z", "X is not a tool but a mirror", "Efficiency becomes a trap when".
- **Why it reads as AI:** a reusable formula that sounds profound without adding precision. It gestures at a point instead of stating it.
- **Before:**
  > Symmetry is the language of trust. Efficiency becomes a trap when teams forget the human layer.
- **After:**
  > Symmetric layouts feel more predictable to users. Teams can over-optimize workflows and miss how people actually work.
- **Rule:** R-36.

#### Staccato Drama

- **The pattern:** a run of short declarative fragments to manufacture a punchline: "It had no preference. No prior. No nostalgia."
- **Why it reads as AI:** one short sentence for emphasis is fine; a run of them sounds engineered. The rhythm is even, the effect is theatrical.
- **Before:**
  > Then the old rules were gone. No templates. No defaults. No safety.
- **After:**
  > The old rules no longer applied, and every page had to be designed from scratch.
- **Rule:** R-36.

#### Synonym Cycling

- **The pattern:** swapping synonyms to avoid repeating a word: "the protagonist faces a challenge, the main character must adapt, the central figure persists".
- **Why it reads as AI:** models rewrite to dodge repetition penalties. Human writers repeat the clearest word when it is clearest.
- **Before:**
  > The checkout is fast. The process is quick. The flow is speedy.
- **After:**
  > The checkout is fast. Everything happens in three clicks.
- **Rule:** R-36.

#### False Ranges

- **The pattern:** "from X to Y" where X and Y are not on a meaningful scale: "from onboarding to scale", "from first click to final invoice, and everything in between".
- **Why it reads as AI:** the range is an impressive-sounding frame that covers nothing specific.
- **Before:**
  > From first touch to final invoice, and everything in between.
- **After:**
  > Handles quotes, invoices, and payment reminders.
- **Rule:** R-36.

### Honesty & Evidence

#### Fabricated Specifics

- **The pattern:** invented numbers, testimonials, names, dates, or features that look realistic but are not real.
- **Why it reads as AI:** a specific-looking fabrication is worse than a vague claim, because it reads as honest while being false. This is the one pattern that is a defect even when it sounds more human.
- **Before:**
  > Trusted by 10,000+ teams. "Antislop cut our review time in half." - Sarah Chen, VP Engineering at [fictional company].
- **After:**
  > If no real customer exists, write no number and no quote. Say what the product does instead. Any real statistic needs a real source (R-17, R-36).
- **Rule:** R-17, R-18, R-36, R-38, C-5.

#### Speculative Gap-Filling

- **The pattern:** when the writer does not know a fact, they write a sentence about not knowing it, then invent plausible filler: "the company was likely founded in the 1990s", "she maintains a low profile".
- **Why it reads as AI:** a guess dressed as fact. The model cannot find a source, so it papers over the gap.
- **Before:**
  > While specific details are limited, the founder likely started small and grew through word of mouth.
- **After:**
  > The founding details are not documented in our sources. (Or omit the sentence entirely. State a date only if a source provides one.)
- **Rule:** R-17, R-36.

#### Generic Positive Conclusion

- **The pattern:** "The future looks bright", "Exciting times lie ahead", "This is a major step in the right direction".
- **Why it reads as AI:** an upbeat send-off that restates nothing and promises nothing. It pads the ending with optimism instead of information.
- **Before:**
  > The future looks bright for our customers as we continue our journey toward excellence.
- **After:**
  > (Cut the sentence. End on the last concrete fact, or state real plans if they exist.)
- **Rule:** R-36.

### Hygiene & Markdown

#### Em Dashes

- **The pattern:** the em dash character (`—`) used as an aside or connector: *"institutions — not the people — continue"*.
- **Why it reads as AI:** it is one of the most reliable AI tells, and the core bans it outright.
- **Rule:** R-02 forbids the em dash in any text. Replace each one, in rough order of preference: a period (start a new sentence), a comma (a tight aside), a colon (introduce an explanation), parentheses (a true aside), or restructure the sentence. Also catch spaced em dashes (` — `) and double hyphens (` -- `) used the same way.
- **Before:**
  > The policy — announced without warning — affects thousands of workers.
- **After:**
  > The policy, announced without warning, affects thousands of workers.
- **Before:**
  > You don't say "Netherlands, Europe" as an address — yet this mislabeling continues.
- **After:**
  > You don't say "Netherlands, Europe" as an address, yet this mislabeling continues.
- **False positive:** many editors and journalists use em dashes deliberately. On its own an em dash is not proof of AI. It counts when it sits in a cluster with other tells (R-02 still bans it in output, but do not rewrite the user's deliberate style without saying so).
- **Voice sample:** if the user provides a writing sample that uses em dashes, that sample is a direction rather than agent copy. Surface it the way R-37 says (name the character, name the rule, ask), then match the sample's frequency only if the owner keeps it. Never keep or cut them silently.

#### Boldface Overuse

- **The pattern:** every key term bolded mechanically: **"OKRs**, **KPIs**, **BMC**".
- **Why it reads as AI:** emphasis everywhere is emphasis nowhere. The page shouts at the reader.
- **Before:**
  > It blends **OKRs**, **KPIs**, and **visual strategy tools** for planning.
- **After:**
  > It blends OKRs, KPIs, and visual strategy tools for planning.
- **Rule:** R-36.
- **Carve-out:** the structural labels inside the antislop rules themselves (the `**FORBIDDEN**` / `**REQUIRED**` markers in `antislop.md`) are documentation conventions, not the mechanical bold-every-key-term pattern above, and are exempt.

#### Excessive Quotation Marks

- **The pattern:** long text studded with quotation marks: quoting words that do not need quoting, scare quotes around ordinary terms, and quotes used as a default for emphasis or hedging. The page reads quoted rather than written.
- **Why it reads as AI:** models reach for quotation marks as a default way to add distance, irony, or emphasis without writing it into the sentence. Dense quoting is a reliable machine tell in longer text.
- **Before:**
  > The "solution" "streamlines" your "workflow" so you can "focus" on "what matters."
- **After:**
  > The solution streamlines your workflow so you can focus on what matters.
- **Rule:** R-36.
- **Not a ban:** dialogue, short stories, quoted real sources, and titles of works keep their quotes. The tell is quotes doing the work the sentence should do. One scare quote used once for a real reason is fine; a cluster of them is not. Minimize, do not strip quotes that carry meaning.

#### Inline-Header Lists

- **The pattern:** list items that start with a bolded header followed by a colon: "- **User Experience:** The UX has been improved".
- **Why it reads as AI:** the header restates what the item already says. It is a formatting habit, not a structure.
- **Before:**
  > - **User Experience:** The interface is easier to use.
  > - **Performance:** Load times are faster.
  > - **Security:** Data is encrypted.
- **After:**
  > The update improves the interface, speeds up load times, and encrypts data in transit.
- **Rule:** R-36.
- **Carve-out:** the `- **Tell:**` / `- **Why:**` / `- **Fix:**` headers that structure every antislop skill entry are a documentation convention, not the header-restates-the-item habit above, and are exempt.

#### Emojis in Headings

- **The pattern:** decoration emojis leading headings or bullets: 🚀 Launch, 💡 Key insight, ✅ Next steps.
- **Why it reads as AI:** the emoji carries no information. It decorates instead of communicating.
- **Before:**
  > 🚀 **Launch Phase:** The product ships in Q3
  > 💡 **Key Insight:** Users prefer simple pricing
- **After:**
  > The product ships in Q3. User research showed a preference for simple pricing.
- **Rule:** R-36.

#### Filler Phrases

- **The pattern:** "In order to" for "to", "Due to the fact that" for "because", "At this point in time" for "now", "It is important to note that" for nothing.
- **Why it reads as AI:** filler inflates the sentence without adding meaning. It is padding a model adds to sound formal.
- **Before:**
  > In order to achieve this goal, it is important to note that we need more data.
- **After:**
  > To reach this goal, we need more data.
- **Rule:** R-36.

#### Excessive Hedging

- **The pattern:** multiple qualifiers stacked on one claim: "could potentially possibly", "may perhaps".
- **Why it reads as AI:** hedging everywhere makes the text sound evasive. One qualifier does the work.
- **Before:**
  > This could potentially possibly be the reason the feature went unused.
- **After:**
  > This may be why the feature went unused.
- **Rule:** R-36.

### What NOT to flag

A clean human writer can hit several patterns above without any AI involvement. Before editing, sanity-check that you are not gutting legitimate prose. These are **not** reliable indicators on their own:

- **Perfect grammar and consistent style.** Many writers are professionals or have been edited. Polish does not equal AI.
- **Mixed casual and formal registers.** This often signals a real person, not a chatbot.
- **"Bland" or "robotic" prose.** AI prose has specific tells. Generic dryness without those tells is just dry writing.
- **Formal vocabulary.** AI overuses *specific* words (see Empty AI Vocabulary), not all fancy words. Do not flatten a precise word just because it sounds brainy.
- **Common transition words in isolation.** One "however" or "additionally" is not a tell. They count only when piled up.
- **Curly quotes alone.** macOS, Word, and most CMSes auto-curl by default. Curly quotes count only when stacked with other tells.
- **Em dashes alone.** Editors and journalists use them. An em dash is evidence only inside a cluster.
- **One short emphatic sentence.** Humans use clipped sentences to land a point. Flag staccato drama only when several fragments appear in a row.
- **Unsourced claims.** Most of the web is unsourced. Lack of citations proves nothing.
- **Secondhand text.** Do not rewrite phrases inside quotations, titles, proper names, or examples where the phrase is being discussed rather than used.

**Look for clusters, not isolated tells.** A single em dash means nothing. Em dashes plus rule of three plus "vibrant tapestry" plus a generic conclusion is a confession. This matches the core's own guidance: Part 1 is a diagnostic scan, not a ban list.

### Signs of human writing (preserve these)

Lean toward leaving the prose alone when you see these. They are evidence of a real person, and over-editing destroys what makes the copy sound human:

- **Specific, unusual, hard-to-fabricate detail.** A real address. A weird quote. LLMs round off specifics; humans hoard them.
- **Mixed feelings and unresolved tension.** "I think this is mostly good, but it bothers me." LLMs default to clean takes.
- **Dated, era-bound references.** Slang, memes, or in-jokes that map to a specific year and subculture.
- **Variety in sentence length.** Real writing alternates short and long. AI writing tends toward an even, mid-length cadence.
- **Genuine asides and self-corrections.** "(I keep wanting to say 'almost' here, but it really was certain.)"

### Voice calibration (optional)

If the user provides a sample of their own writing, match it before rewriting:

1. Read the sample first. Note its sentence lengths, vocabulary, paragraph openings, punctuation, and recurring phrases.
2. Match those habits instead of merely deleting AI patterns. Do not upgrade casual words or regularize deliberate quirks.
3. The sample outranks this skill's style rules, except where R-02 applies. R-02 governs copy the agent authors; a sample that uses em dashes is a direction, so it goes through R-37's conflict protocol, and you match its frequency only if the owner keeps it. R-02 applies in full to any copy the user did not authorize.

Without a sample, use the defaults above. Matching the author beats scrubbing the tell.

### Draft, audit, final

Run this loop before delivering copy:

1. **Draft.** Rewrite the text applying the patterns above. Check that it reads naturally aloud, varies sentence length, prefers specific detail and simple constructions, and keeps the appropriate register.
2. **Audit.** Ask two questions and answer them briefly: "What makes this obviously AI generated?" and "Does it state any fact, name, number, date, or citation that is not in the source?" A fabrication is a defect even when it sounds more human than the vague original.
3. **Final.** Revise to address both answers. Check for em and en dashes one last time (R-02). A hit means the draft is not done.

### Copywriting Skill Checklist

Run these alongside the core Delivery Gate when the task is copy work. Every line below must be true:

- [ ] No fabricated numbers, testimonials, names, dates, or claims; everything real or a labeled placeholder (R-17, R-18, R-36, R-38)
- [ ] Buzzwords from R-16 and the Empty AI Vocabulary list replaced with specific, evidenced language
- [ ] No em dashes in the output (R-02); if the user's own sample voice uses them, they were surfaced under R-37 and the owner kept them
- [ ] No excessive quotation marks: quotes only where they carry meaning (dialogue, real citations, titles), not as default emphasis (R-36)
- [ ] No all-caps emphasis clauses: emphasis written into the sentence, not shouted with caps (R-36)
- [ ] Every sentence names its actor: no actorless passive, no abstraction given a human verb, where a real subject was available (R-02, R-16)
- [ ] CTAs specific to the action, not generic templates (R-15)
- [ ] No AI-rhythm tells: no forced rule of three, no negative parallelism, no staccato drama, no aphorism formulas, no false ranges (R-36)
- [ ] Voice present: the copy has a real voice (the user's sample or a clearly chosen tone), not a sterile default (R-37)
- [ ] Read aloud: the copy sounds like a person wrote it, not like a model padded it

## Phrase catalog — EN + ID filler to cut

> `local` / `phrase-catalog` / deciding whether a specific phrase is filler

Use when the quick list in SKILL.md doesn't cover the phrase in front of you.

### Throat-clearing openers — Pembuka basi

**English:** Cut these, or replace with actual content:
- "It is important to note that..."
- "It should be noted that..."
- "It is worth mentioning that..."
- "This paper/section/report aims to explore/discuss/examine..."
- "As we all know..." / "As is well known..."
- "Needless to say..." — if it's needless to say, don't say it.
- "In today's world..." / "In this day and age..."

**Indonesia:**
- "Perlu diketahui bahwa..."
- "Perlu dicatat bahwa..."
- "Perlu ditekankan bahwa..."
- "Dapat disimpulkan bahwa..."
- "Sebagaimana kita ketahui..."
- "Seperti yang telah disebutkan sebelumnya..."
- "Di zaman sekarang ini..."

### Stacked hedges — Hedge bertumpuk

Keep at most one hedge per claim; delete the rest.

**English:**
- "could possibly perhaps" → "may" (or nothing)
- "it seems to suggest that it might indicate" → "suggests"
- "there is a possibility that it could potentially" → "it could" or "it may"

**Indonesia:**
- "mungkin bisa jadi" → "mungkin"
- "diduga kemungkinan besar" → "diduga"
- "ada kemungkinan bahwa bisa saja" → "bisa"

### Empty transitions — Transisi kosong

**English:**
- "Moving forward,"
- "That being said," / "With that said,"
- "At the end of the day,"
- "When all is said and done,"
- "It goes without saying that..."

**Indonesia:**
- "Ke depannya,"
- "Dengan kata lain,"
- "Pada akhirnya,"
- "Tidak perlu dikatakan lagi..."
- "Terlepas dari itu," (when not carrying real logic)

Keep transitions that carry real logic: "however", "therefore", "because", "as a result",
"in contrast" — and "tetapi", "karena", "oleh karena itu", "sebaliknya".

### Nominalizations — Nominalisasi

**English:**
| Instead of | Use |
|---|---|
| conduct an analysis of | analyze |
| make a decision on | decide |
| perform an evaluation of | evaluate |
| provide assistance to | help |
| give consideration to | consider |
| carry out an investigation into | investigate |
| reach a conclusion about | conclude |
| put emphasis on | emphasize |
| make an announcement | announce |
| have a discussion about | discuss |

**Indonesia:**
| Ganti | Pakai |
|---|---|
| melakukan analisis terhadap | menganalisis |
| mengambil keputusan | memutuskan |
| memberikan bantuan | membantu |
| memberikan pertimbangan terhadap | mempertimbangkan |
| melaksanakan penyelidikan terhadap | menyelidiki |
| mencapai kesimpulan tentang | menyimpulkan |
| menekankan pada | menekankan |
| membuat pengumuman | mengumumkan |
| mengadakan diskusi tentang | membahas |

### Redundant pairs and doubled modifiers — Kata ganda

**English:** each and every · full and complete · first and foremost · various different ·
each individual · basic fundamentals · past history · future plans · end result · final outcome ·
completely eliminate · absolutely essential · totally unique · close proximity · advance planning ·
unexpected surprise · new innovation

**Indonesia:** benar-benar menghilangkan · sangat penting sekali · hasil akhir · mulai dari awal ·
berbagai macam · satu sama lain · kembali lagi · sangat luar biasa · prosedur yang dilakukan

Pick one word from each pair.

### Padding passive voice — Kalimat pasif berlebihan

**English:** Flip to active only when the actor is known and relevant:
- "The decision was made by management to..." → "Management decided to..."
- "It was found by the researchers that..." → "The researchers found..."

Leave passive when: actor unknown/irrelevant ("the samples were collected in triplicate"),
or field convention is passive (natural sciences, some legal writing).

**Indonesia:** "Keputusan diambil oleh manajemen untuk..." → "Manajemen memutuskan untuk..."
"Hasil penelitian ditemukan oleh tim bahwa..." → "Tim menemukan bahwa..."

### Verbal-tic intensifiers — Intensifier tanpa makna

**English:** very · really · quite · extremely · incredibly · basically · essentially · actually ·
in fact · truly · definitely — when used as reflex rather than real emphasis.
Upgrade genuine emphasis: "very important" → "critical" · "really big" → "major".

**Indonesia:** sangat · sekali · sebenarnya · pokoknya · bener-bener · intinya — bila tanpa
makna tambahan. Upgrade: "sangat penting" → "kritis" · "sangat besar" → "besar".

### Worked examples — Contoh

#### Business email (English)
**Input:** Hi team, I just wanted to reach out and touch base regarding the upcoming deadline. I think it's important that we all get on the same page about this. Moving forward, I would really appreciate it if everyone could try to submit their reports by Friday, if that's at all possible. Thanks so much in advance, really appreciate it!
**Output:** Hi team — please submit your reports by Friday. Thanks!

#### Email kantor (Indonesia)
**Input:** Halo tim, saya hanya ingin menghubungi dan berkoordinasi mengenai tenggat yang akan datang. Saya rasa penting kita semua satu pemahaman tentang ini. Ke depannya, saya sangat menghargai jika semua orang dapat berusaha mengirimkan laporan sebelum Jumat, jika memungkinkan. Terima kasih banyak sebelumnya!
**Output:** Halo tim — tolong kirim laporan sebelum Jumat. Terima kasih!

#### Academic-style paragraph (English)
**Input:** It is widely acknowledged in the literature that supply chain delays can arise from a multitude of different causes. In this particular study, it was found that the majority of the delays that occurred could be attributed primarily to gaps in the handover process between shifts, which is consistent with what has been noted in prior research on this topic.
**Output:** Supply chain delays have many possible causes. In this study, most delays traced to gaps in shift handover — consistent with prior research.

#### Paragraf akademik (Indonesia)
**Input:** Telah diketahui secara luas dalam literatur bahwa keterlambatan rantai pasok dapat timbul dari banyak penyebab yang berbeda. Dalam penelitian khusus ini, ditemukan bahwa mayoritas keterlambatan yang terjadi terutama dapat dikaitkan pada celah dalam proses serah terima antar shift, yang konsisten dengan apa yang telah dicatat dalam penelitian sebelumnya tentang topik ini.
**Output:** Keterlambatan rantai pasok punya banyak penyebab. Pada studi ini, mayoritas keterlambatan berasal dari celah serah terima antar shift — konsisten dengan penelitian sebelumnya.
