# Origins — the three philosophies and their quarrel

**Read this when:** you need to know why a rule reads the way it does, or want the upstream source behind a layer

**Layer:** the repository's own analysis, quoted rather than summarised

Loaded on demand: the always-on rules live in the skill's `SKILL.md`. The
bodies below are upstream text carried verbatim, with the per-section
provenance and every declared edit listed in `SOURCES.md` beside this file.

| section | from | load |
|---|---|---|
| [Grug — the full text of the site](#grug-the-full-text-of-the-site) | `grug` | always |
| [Where grug, caveman and be-brief disagree](#where-grug-caveman-and-be-brief-disagree) | `local` | always |

---

## Grug — the full text of the site

> `grug` / `grug-canonical` / the user asks why the rules are shaped this way, or a decision needs the complexity argument in grug's own words

> **Merge note.** The site's markdown source, so it carries page furniture: an empty anchor before each heading and a link to that anchor. The four `markup` transforms remove that scaffolding and nothing else; no word of grug's prose is changed. Read this instead of the compressed summary when the argument matters more than the rule.

The Grug Brained Developer
## Introduction

this collection of thoughts on software development gathered by grug brain developer

grug brain developer not so smart, but grug brain developer program many long year and learn some things
although mostly still confused

grug brain developer try collect learns into small, easily digestible and funny page, not only for you, the young grug, but also for him
because as grug brain developer get older he forget important things, like what had for breakfast or if put pants on

big brained developers are many, and some not expected to like this, make sour face

*THINK* they are big brained developers many, many more, and more even definitely probably maybe not like this, many
sour face (such is internet)

(note: grug once think big brained but learn hard way)

is fine!

is free country sort of and end of day not really matter too much, but grug hope you fun reading and maybe learn from
 many, many mistake grug make over long program life

## The Eternal Enemy: Complexity
apex predator of grug is complexity

complexity bad

say again:

complexity *very* bad

_you_ say now:

complexity *very*, *very* bad

given choice between complexity or one on one against t-rex, grug take t-rex: at least grug see t-rex

complexity is spirit demon that enter codebase through well-meaning but ultimately very clubbable non grug-brain
developers and project managers who not fear complexity spirit demon or even know about sometime

one day code base understandable and grug can get work done, everything good!

next day impossible: complexity demon spirit has entered code and very dangerous situation!
grug no able see complexity demon, but grug sense presence in code base

demon complexity spirit mocking him make change here break unrelated thing there what!?! mock mock mock ha ha so funny 
grug love programming and not becoming shiney rock speculator like grug senior advise

club not work on demon spirit complexity and bad idea actually hit developer who let spirit in with club: sometimes grug
himself!

sadly, often grug himself

so grug say again and say often: complexity *very*, *very* bad

### Saying No
best weapon against complexity spirit demon is magic word: "no"

"no, grug not build that feature"

"no, grug not build that abstraction"

"no, grug not put water on body every day or drink less black think juice you stop repeat ask now"

note, this good engineering advice but bad career advice: "yes" is magic word for more shiney rock and put in
charge of large tribe of developer

sad but true: learn "yes" then learn blame other grugs when fail, ideal career advice

but grug must to grug be true, and "no" is magic grug word.  Hard say at first, especially if you nice grug and don't like
disappoint people (many such grugs!) but  easier over time even though shiney rock pile not as high as might otherwise be

is ok: how many shiney rock grug really need anyway?

### Saying ok
sometimes compromise necessary or no shiney rock, mean no dinosaur meat, not good, wife firmly remind grug
about young grugs at home need roof, food, and so forth, no interest in complexity demon spirit rant by grug for
fiftieth time

in this situation, grug recommend "ok"

"ok, grug build that feature"

then grug spend time think of [80/20 solution](https://en.wikipedia.org/wiki/Pareto_principle) to problem and build that instead.
80/20 solution say "80 want with 20 code"  solution maybe not have all bell-whistle that project manager want, maybe a 
little ugly, but work and deliver most value, and keep demon complexity spirit at bay for most part to extent

sometimes probably best just not tell project manager and do it 80/20 way.  easier forgive than permission, project managers
mind like butterfly at times overworked and dealing with many grugs.  often forget what even feature supposed to do or move on or 
quit or get fired grug see many such cases

anyway is in project managers best interest anyway so grug not to feel too bad for this approach usually

### Factoring Your Code
next strategy very harder: break code base up properly (fancy word: "factor your code properly")  here is hard give general
advice because each system so different.  however, one thing grug come to believe: not factor your application too early!

early on in project everything very abstract and like water: very little solid holds for grug's struggling brain to hang 
on to.  take time to develop "shape" of system and learn what even doing.  grug try not to factor in early part of project
and then, at some point, good cut-points emerge from code base

good cut point has narrow interface with rest of system: small number of functions or abstractions that hide complexity
demon internally, like trapped in crystal

grug quite satisfied when complexity demon trapped properly in crystal, is best feeling to trap mortal enemy!

grug try watch patiently as cut points emerge from code and slowly refactor, with code base taking shape over time along
with experience.  no hard/ fast rule for this: grug know cut point when grug see cut point, just take time to build 
skill in seeing, patience

sometimes grug go too early and get abstractions wrong, so grug bias towards waiting

big brain developers often not like this at all and invent many abstractions start of project

grug tempted to reach for club and yell "big brain no maintain code!  big brain move on next architecture committee
leave code for grug deal with!"

but grug learn control passions, major difference between grug and animal

instead grug try to limit damage of big brain developer early in project by giving them thing like
UML diagram (not hurt code, probably throw away anyway) or by demanding working demo tomorrow

working demo especially good trick: force big brain make something to actually work to talk about and code to look at that do
thing, will help big brain see reality on ground more quickly

remember!  big brain have big brain!  need only be harness for good and not in service of spirit complexity demon on 
accident, many times seen

(best grug brain able to herd multiple big brain in right direction and produce many complexity demon trap crystals, large
shiney rock pile awaits such grug!)

also sometimes call demo approach "prototype", sound fancier to project manager

grug say prototype early in software making, _especially_ if many big brains

## Testing
grug have love/hate relationship with test: test save grug many, many uncountable time and grug love and respect test
unfortunately also many test shamans exist.  some test shaman make test idol, demand things like "first test" before grug
even write code or have any idea what grug doing domain!
how grug test what grug not even understand domain yet!?

"Oh, don't worry: the tests will show you what you need to do."

grug once again catch grug slowly reaching for club, but grug stay calm

grug instead prefer write most tests after prototype phase, when code has begun firm up

but, note well: grug must here be very disciplined!
easy grug to move on and not write tests because "work on grugs machine"!

this very, very bad: no guarantee work on other machine and no guarantee work on grug machine in future, many times

test shaman have good point on importance of test, even if test shaman often sometimes not complete useful
feature in life and talk only about test all time, deserve of club but heart in right place

also, test shaman often talk unit test very much, but grug not find so useful.  grug experience that ideal tests are not 
unit test or either end-to-end test, but in-between test

[unit tests](https://en.wikipedia.org/wiki/Unit_testing) fine, ok, but break as implementation change (much compared api!)
and make refactor hard and, frankly, many bugs anyway often due interactions other code.  often throw away when code change.
grug write unit test mostly at start of project, help get things going but not get too attached or expect value long time

[end to end](https://smartbear.com/solutions/end-to-end-testing/) tests good, show whole system work, but! hard to 
understand when break and drive grug crazy very often, sometimes grugs just end up ignoring because "oh, that break all 
time"  very bad!

in-between tests, grug hear shaman call ["integration tests"](https://en.wikipedia.org/wiki/Integration_testing) sometime 
often with sour look on face. but grug say integration test sweet spot according to grug: high level enough test correctness 
of system, low level enough, with good debugger, easy to see what break

grug prefer some unit tests especially at start but not 100% all code test and definitely not "first test".  "test along
the way" work pretty well for grug, especially as grug figure things out

grug focus much ferocious integration test effort as cut point emerge and system stabilize!  cut point api hopefully stable
compared implementation and integration test remain valuable many long time, and easy debug

also small, well curated end-to-end test suite is created to be kept working religiously on pain of clubbing. focus of important 
end-to-end test on most common UI features and few most important edge cases, but not too many or become impossible maintain
and then ignored

this ideal set of test to grug

you may not like, but this peak grug testing

also, grug dislike [mocking](https://en.wikipedia.org/wiki/Mock_object) in test, prefer only when absolute necessary
to (rare/never) and coarse grain mocking (cut points/systems) only at that

one exception "first test" dislike by grug: when bug found.  grug always try first reproduce bug with regression test 
_then_ fix bug, this case only for some reason work better

## Agile
grug think agile not terrible, not good

end of day, not worst way to organize development, maybe better than others grug supposes is fine

danger, however, is agile shaman!  many, many shiney rock lost to agile shaman!

whenever agile project fail, agile shaman say "you didn't do agile right!"  grug note this awfully convenient for agile
shaman, ask more shiney rock better agile train young grugs on agile, danger!

grug tempted reach for club when too much agile talk happen but always stay calm

prototyping, tools and hiring good grugs better key to success software: agile process ok and help some but sometimes hurt taken
too seriously

grug say [no silver club](https://en.wikipedia.org/wiki/No_Silver_Bullet) fix all software problems no matter what agile
shaman say (danger!)

## Refactoring
refactoring fine activity and often good idea, especially later in project when code firmed up

however, grug note that many times in career "refactors" go horribly off rails and end up causing more harm than good

grug not sure exactly why some refactors work well, some fail, but grug notice that larger refactor, more
likely failure appear to be

so grug try to keep refactors relatively small and not be "too far out from shore" during refactor.  ideally system work
entire time and each step of finish before other begin.
end-to-end tests are life saver here, but often very hard understand why broke... such is refactor life.

also grug notice that introducing too much abstraction often lead to refactor failure and system failure.  good example
was [J2EE](https://www.webopedia.com/definitions/j2ee/) introduce, many big brain sit around thinking too much abstraction, nothing good came of it many project hurt

another good example when company grug work for introduce [OSGi](https://www.techtarget.com/searchnetworking/definition/OSGi) to help 
manage/trap spriit complexity demon in code base.  not only OSGi not help, but make complexity demon much more powerful!
took multiple man year of best developers to rework as well to boot!  more complex spirit and now features impossible 
implement! very bad!

## Chesterton's Fence
wise grug shaman [chesterton](https://en.wikipedia.org/wiki/G._K._Chesterton) once say
> here exists in such a case a certain institution or law; let us say, for the sake of simplicity, a fence or gate erected across a road. The more modern type of reformer goes gaily up to it and says, “I don’t see the use of this; let us clear it away.” To which the more intelligent type of reformer will do well to answer: “If you don’t see the use of it, I certainly won’t let you clear it away. Go away and think. Then, when you can come back and tell me that you do see the use of it, I may allow you to destroy it.”

many older grug learn this lesson well not start tearing code out willy nilly, no matter how ugly look

grug understand all programmer platonists at some level wish music of spheres perfection in code.  but danger is here,
world is ugly and gronky many times and so also must code be

humility not often come big brained or think big brained 
easily or grug even, but grug often find "oh, grug no like look of this, grug fix" lead many hours pain grug and no better or system
worse even

grug early on in career often charge into code base waving club wildly and smash up everything, learn not good

grug not say no improve system ever, quite foolish, but recommend take time understand system first especially bigger system is and
is respect code working today even if not perfect

here tests often good hint for why fence not to be smashed!

## Microservices
grug wonder why big brain take hardest problem, factoring system correctly, and introduce network call too

seem very confusing to grug

## Tools
grug love tool.  tool and control passion what separate grug from dinosaurs!  tool allow grug brain to create code that 
not possible otherwise by doing thinking for grug, always good relief! grug always spend time in new place learning 
tools around him to maximize productivity: learn tools for two weeks make development often twice faster and often
have dig around ask other developers help, no docs

code completion in IDE allow grug not have remembered all API, very important!
java programming nearly impossible without it for grug!

really make grug think some time

good debugger worth weight in shiney rocks, in fact also more: when faced with bug grug would often trade all shiney rock and
perhaps few children for good debugger and anyway debugger no weigh anything far as grug can tell
grug always recommend new programmer learn available debugger very deeply, features like conditional break points, expression
evaluation, stack navigation, etc teach new grug more about computer than university class often!

grug say never be not improving tooling

## Type Systems
grug very like type systems make programming easier.  for grug, type systems most value when grug hit dot on keyboard and
list of things grug can do pop up magic.  this 90% of value of type system or more to grug

big brain type system shaman often say type correctness main point type system, but grug note some big brain type system 
shaman not often ship code.  grug suppose code never shipped is correct, in some sense, but not really what grug mean
when say correct

grug say tool magic pop up of what can do and complete of code major most benefit of type system, correctness also good but not 
so nearly so much

also, often sometimes caution beware big brains here!

some type big brain think in type systems and talk in lemmas, potential danger!

danger abstraction too high, big brain type system code become astral projection of platonic generic turing model of 
computation into code base.  grug confused and agree some level very elegant but also very hard do anything like 
record number of club inventory for Grug Inc. task at hand

generics especially dangerous here, grug try limit generics to container classes for most part where most value add

temptation generics very large is trick!  spirit demon complex love this one trick! beware!

always most value type system come: hit dot see what grug can do, never forget!

## Expression Complexity
grug once like to minimize lines of code much as possible.  write code like this:

```js
  if(contact && !contact.isActive() && (contact.inGroup(FAMILY) || contact.inGroup(FRIENDS))) {
    // ...
  }
```

over time grug learn this hard debug, learn prefer write like so:

```js
  if(contact) {
    var contactIsInactive = !contact.isActive();
    var contactIsFamilyOrFriends = contact.inGroup(FAMILY) || contact.inGroup(FRIENDS);
    if(contactIsInactive && contactIsFamilyOrFriends) {
        // ...
    }
  }
```

grug hear screams from young grugs at horror of many line of code and pointless variable and grug prepare defend self with club

club fight start with other developers attack and grug yell: "easier debug!  see result of each expression more clearly and good name!  easier
understand conditional expression!  EASIER DEBUG!"

definitely easier debug and once club fight end calm down and young grug think a bit, they realize grug right

grug still catch grug writing code like first example and often regret, so grug not judge young grug

## DRY
[DRY](https://en.wikipedia.org/wiki/Don%27t_repeat_yourself) mean Don't Repeat Self, powerful maxim over mind of most
developers

grug respect DRY and good advice, however grug recommend balance in all things, as gruggest big brain aristotle recommend

grug note humourous graph by Lea Verou correspond with grug passion not repeat:
over time past ten years program grug not as concerned repeat code.  so long as repeat code simple enough and obvious 
enough, and grug begin feel repeat/copy paste code with small variation is better than many callback/closures passed arguments
or elaborate object model: too hard complex for too little benefit at times

hard balance here, repeat code always still make grug stare and say "mmm" often, but experience show repeat code
sometimes often better than complex DRY solution

note well!  grug encourage over literal developer not take does work line too serious, is joke

## Separation of Concerns (SoC)
[Separation of Concern (SoC)](https://en.wikipedia.org/wiki/Separation_of_concerns) another powerful idea over many developer
mind, idea to separate different aspects of system into distinct sections code

canonical example from web development: separation of style (css file), markup (html file) and logic (javascript file)

here grug much more sour faced than DRY and in fact write big brained essay on alternative design principle
[locality of behavior (LoB)](https://htmx.org/essays/locality-of-behaviour/) against SoC

grug much prefer put code on the thing that do the thing.  now when grug look at the thing grug know the thing what the
thing do, alwasy good relief!

when separate of concern grug must often all over tarnation many file look understand what how button do, much confuse 
and time waste: bad!

## Closures
grug like closures for right job and that job usually abstracting operation over collection of objects

grug warn closures like salt, type systems and generics: small amount go long way, but easy spoil things too much use
give heart attack

javascript developers call very special complexity demon spirit in javascript "callback hell" because too much closure 
used by javascript libraries very sad but also javascript developer get what deserved let grug be frank

## Logging
grug huge fan of logging and encourage lots of it, especially in cloud deployed.  some non-grugs say logging expensive
and not important.  grug used think this way no more

funny story: grug learn idol [rob pike](https://en.wikipedia.org/wiki/Rob_Pike) working on logging at google and decide: 
"if rob pike working on logging, what grug do there?!?" so not pursue.  turn out logging _very_ important to google so
of course best programmer work on it, grug!
don't be such grug brain, grug, much less shiney rock now!

oh well, grug end up at good company anyway and rob pike dress habit 
[increasingly erratic](https://www.youtube.com/watch?v=KINIAgRpkDA), so all work out in end, but 
point stand: logging very important!

grug tips on logging are:

* log all major logical branches within code (if/for)
* if "request" span multiple machine in cloud infrastructure, include request ID in all so logs can be grouped
* if possible make log level dynamically controlled, so grug can turn on/off when need debug issue (many!)
* if possible make log level per user, so can debug specific user issue

last two points are especially handy club when fighting bugs in production systems very often

unfortunately log libraries often very complex (java, [why you do?](https://stackify.com/logging-java/)) but worth investing 
time in getting logging infrastructure "just right" pay off big later in grug experience

logging need taught more in schools, grug think

## Concurrency
grug, like all sane developer, fear concurrency

as much as possible, grug try to rely on simple concurrency models like stateless web request handlers and simple
remote job worker queues where jobs no interdepend and simple api

[optimistic concurrency](https://en.wikipedia.org/wiki/Optimistic_concurrency_control) seem work well for web stuff

occasionally grug reach for [thread local variable](https://en.wikipedia.org/wiki/Thread-local_storage), usually when 
writing framework code

some language have good concurrent data structure, like java [ConcurrentHashMap](https://docs.oracle.com/javase/8/docs/api/java/util/concurrent/ConcurrentHashMap.html)
but still need careful grug work to get right

grug has never used [erlang](https://en.wikipedia.org/wiki/Erlang_(programming_language)), hear good things, but language 
look wierd to grug sorry

## Optimizing
ultra biggest of brain developer once say:

> premature optimization is the root of all evil

this everyone mostly know and grug in humble violent agreement with ultra biggest of big brain

grug recommend always to have concrete, real world perf profile showing specific perf issue before begin optimizing.
never know what actual issue might be, grug often surprise!  very often!

beware only cpu focus: easy to see cpu and much big o notation thinking having been done in school,
but often not root of all slowness, surprise to many including grug

hitting network equivalent of many, many millions cpu cycle and always to be minimized if possible, note well big brain
microservice developer!

inexperienced big brain developer see nested loop and often say "O(n^2)?  Not on my watch!"

complexity demon spirit smile

## APIs
grug love good apis.  good apis not make grug think too much

unfortunately, many apis very bad, make grug think quite a bit.  this happen many reasons, here two:

* API creators think in terms of implementation or domain of API, rather than in terms of use of API
* API creators think too abstract and big brained

usually grug not care too deeply about detail of api: want write file or sort list or whatever, just want to call
`write()` or `sort()` or whatever

but big brain api developers say:

"not so fast, grug!  is that file *open for write*? did you define a *Comparator* for that sort?"

grug find self restraining hand reaching for club again

not care about that stuff right now, just want sort and write file mr big brain!

grug recognize that big brain api designer have point and that _sometime_ these things matter, but often do not.
big brain api developers better if design for simple cases with simple api, make complex cases possible
with more complex api

grug call this "layering" apis: two or three different apis at different level complexity for various grug needs

also, if object oriented, put api on thing instead of elsewhere. java worst at this!
grug want filter list in java

"Did you convert it to a stream?"

fine, grug convert to stream

"OK, now you can filter."
OK, but now need return list!  have stream!
"Well, did you collect your stream into a list?"

what?

"Define a Collector&lt;? super T, A, R&gt; to collect your stream into a list"

grug now swear on ancestor grave he club every single person in room, but count two instead and remain calm

put common thing like `filter()` on list and make return list, listen well big brain java api developer!
nobody care about "stream" or even hear of "stream" before, is not networking api, all java grugs use list mr big brain!
## Parsing
grug love make programming language at drop of hat and 
say [recursive descent](https://en.wikipedia.org/wiki/Recursive_descent_parser)
most fun and beautiful way create parser

unfortunately many big brain school teach only parser generator tool.  here grug usual love of tool is not: parser 
generator tool generate code of awful snakes nest: impossible understand, bottom up, what?  hide recursive nature of 
grammar from grug and debug impossible, very bad according grug!

grug think this because while complexity demon bad for code base and understand, complexity demon very good for generation
of much academic papers, sad but true

production parser almost always recursive descent, despite ignore by schools!  grug furious when learn how simple parse 
is! parsing not big brain only magic: so can you!

grug very elated find big brain developer Bob Nystrom redeem the big brain tribe and write excellent book on recursive
descent: [Crafting Interpreters](https://craftinginterpreters.com/)

book available online free, but grug highly recommend all interested grugs purchase book on general principle, provide
much big brain advice and grug love book _very_ much except visitor pattern (trap!)

## The Visitor Pattern
[bad](https://en.wikipedia.org/wiki/Visitor_pattern)
## Front End Development
some non-grugs, when faced with web development say:
"I know, I'll split my front end and back end codebase up and use a hot new SPA library talking to a GraphQL JSON API back end
over HTTP (which is funny because I'm not transferring hypertext)"

now you have two complexity demon spirit lairs

and, what is worse, front end complexity demon spirit even more powerful and have deep spiritual hold on entire front end
industry as far as grug can tell

back end developers try keep things simple and can work ok, but front end developers make very complex very quickly and 
introduce lots of code, demon complex spirit

even when website just need put form into database or simple brochure site!
everyone do this now!
grug not sure why except maybe facebook and google say so, but that not seem very good reason to grug

grug not like big complex front end libraries everyone use

grug make [htmx](https://htmx.org) and [hyperscript](https://hyperscript.org) to avoid

keep complexity low, simple HTML, avoid lots javascript, the natural ether of spirit complexity demon

maybe they work for you, but no job post, sorry

react better for job and also some type application, but also you become alcolyte of complexity demon whether you like 
or no, sorry such is front end life

## Fads
grug note lots of fads in development, especially front end development today

back end better more boring because all bad ideas have tried at this point maybe (still retry some!)

still trying all bad ideas in front end development so still much change and hard to know

grug recommend taking all revolutionary new approach with grain salt: big brains have working for long 
time on computers now, most ideas have tried at least once

grug not saying can't learn new tricks or no good new ideas, but also much of time wasted on recycled bad ideas, lots of
spirit complexity demon power come from putting new idea willy nilly into code base

## Fear Of Looking Dumb
note!  very good if senior grug willing to say publicly: "hmmm, this too complex for grug"!

many developers Fear Of Looking Dumb (FOLD), grug also at one time FOLD, but grug learn get over: very important senior 
grug say "this too complicated and confuse to me"

this make it ok for junior grugs to admit too complex and not understand as well, often such case!  FOLD major source of 
complexity demon power over developer, especially young grugs!
take FOLD power away, very good of senior grug!

note: important to make thinking face and look big brained when saying though.  be prepare for big brain or, worse and
much more common, *thinks* is big brain to make snide remark of grug

be strong! no FOLD!
club sometimes useful here, but more often sense of humor and especially last failed project by big brain very useful, 
so collect and be calm

## Impostor Syndrome
grug note many such impostor feels in development

always grug one of two states: grug is ruler of all survey, wield code club like thor OR grug have no idea what doing

grug is mostly latter state most times, hide it pretty well though

now, grug make softwares of much work and [moderate open source success](https://star-history.com/#bigskysoftware/htmx&bigskysoftware/_hyperscript&Date)
, and yet grug himself often feel not any idea what doing!  very often!  grug still fear make mistake break everyone code and 
disappoint other grugs, imposter!

is maybe nature of programming for most grug to feel impostor and be ok with is best: nobody imposter if everybody imposter

any young grug read this far probably do fine in program career even if frustrations and worry is always to be there, sorry

## Reads
grug like these:

* [Worse is Better](https://www.dreamsongs.com/WorseIsBetter.html)
* [Worse is Better is Worse](https://www.dreamsongs.com/Files/worse-is-worse.pdf)
* [Is Worse Really Better?](https://www.dreamsongs.com/Files/IsWorseReallyBetter.pdf)
* [A Philosophy of Software Design](https://www.goodreads.com/en/book/show/39996759-a-philosophy-of-software-design)

## Conclusion
_you_ say: complexity *very*, *very* bad

## Where grug, caveman and be-brief disagree

> `local` / `philosophies` / the merged precedence table is a ruling; this is the evidence behind it

> **Merge note.** Verbatim, with the paths updated for where those files now live: the merge moved the per-variant skills under `legacy/`, and a skill that tells an agent to run a script at a path that no longer exists is a defect. Each substitution is a declared literal, checked at build time. A pointer that left the skill folder for its own build tooling cannot resolve once installed, so it became plain text.

The three philosophies in this repo are usually presented as a stack — grug
thinks, caveman speaks, be-brief writes. That story is *mostly* true, but it
glosses over real contradictions. This document states them plainly, because
"just combine them" produces a skill that fails in both directions at once.

---

### The short version

| | Grug | Caveman | Be Brief |
|---|---|---|---|
| **Domain** | Reasoning / deciding | Output to an agent user | Output to a document reader |
| **Register** | lowercase, blunt, deliberately ungrammatical | terse, fragments OK, articles optional | professional prose, full grammar |
| **Grammar** | broken, on purpose | broken, if shorter | **never** broken |
| **Articles** | n/a | dropped when cheap | kept |
| **Audience** | the model itself | the developer driving the agent | a human reading a finished artifact |
| **Persisted files** | n/a | code/comments/commits = normal prose | documents = compressed prose |
| **Failure mode** | over-abstraction, FOLD | ambiguity from over-compression | timidity — not cutting enough |

The single hardest conflict: **caveman says "fragments OK, drop articles";
be-brief says "professional prose, never broken grammar".** These cannot both
govern the same sentence. One of them has to win, and *which* one depends on
where the text is going.

---

### Conflict 1 — Output register (the big one)

**Caveman** (`skills/caveman/SKILL.md`, upstream):

> Drop: articles (a/an/the), filler… Fragments OK. Short synonyms…
>
> Never add word to sound caveman. **Compression only style never grow output.**
> No inserted pronoun or copula to fake broken grammar: "when it not" cost one
> token more than "when not" and say same thing.

**Be Brief** (this repo, `caveman-be-brief`):

> ### MODE 2: EXTERNAL OUTPUT (PROFESSIONAL VOICE)
> Voice: formal, academic, polite, precise, nuanced
> Style: professional prose with zero wasted words — **NOT broken grammar,
> NOT cartoon caveman speech**

**Why both are right.** They optimise for different readers. A developer
watching an agent stream tool calls wants the diagnosis in nineteen tokens. A
thesis examiner reading chapter four does not. Caveman's own upstream README
says the quiet part out loud: *"Caveman no make brain smaller. Caveman make
mouth smaller."* It is a mouth, not a pen.

**Resolution.** Pick by destination, not by vibe:

| Destination | Winner |
|---|---|
| Chat reply to a developer | caveman |
| Thesis, journal, report, memo, professional email | be-brief |
| Code, commands, paths, error strings | neither — untouched |
| Persisted artifacts (comments, commits, docs, issue bodies) | neither — normal prose |

**Do not** put both in one skill without this table. An unqualified "be terse"
next to "never break grammar" is a coin flip on every sentence.

---

### Conflict 2 — Verbosity vs completeness

**Caveman** cuts articles and conjunctions. **Be Brief** keeps every logical
connector:

> **Real logical connectors** — "because", "although", "therefore", "however"
> tell the reader how two ideas relate. That's information, not filler.

**Why it matters.** "Inline obj prop, new ref, re-render. `useMemo`." is
perfect for a developer who can reconstruct the causality. The same sentence
in a methodology section is a defect — the reader cannot tell whether the
re-render causes the new ref or the reverse.

**Resolution.** Caveman is allowed to drop a conjunction **only where
cause-and-effect stays unambiguous** (that is literally its `ultra` level).
Be Brief never does. When in doubt, keep the connector — it is one token, and
ambiguity costs a reader minutes.

---

### Conflict 3 — Grug's voice: internal or not at all

**Grug** is written to be *read*. It is a published essay in a deliberately
broken register: "complexity very bad", "grug no able see complexity demon".
Its whole rhetorical power comes from that voice.

**Be Brief** says the grug voice must never reach the user:

> NEVER output Grug voice to user. Internal only.

**Caveman** is adjacent to grug but is not grug — it is about *mouth*, not
about *simplicity as a decision rule*. Caveman will happily emit a long
technical explanation in fragments; grug would first ask whether you need the
feature at all.

**Resolution.** Three layers, one boundary:

```
grug      → reasoning   (never emitted)
caveman   → how much    (how terse the emitted text is)
be-brief  → how it reads (register of the emitted text)
```

Grug is a **layer**, not a style you can mix into prose. This is why
`variants/grug-reasoning.md` ships as a reasoning-only document with no output
rules at all, and why the reward function in
`skillopt-integration/` treats any grug token in visible output as a hard
failure.

---

### Conflict 4 — "Say no" vs "just answer"

**Grug**: *"No, grug not build that feature."* Complexity is the enemy; the
answer to most requests is a smaller version of the request.

**Caveman/Be Brief**: both are **output** philosophies. Neither has an opinion
on whether the work should be done. They will compress a twenty-page design
doc for a feature that should not exist.

**Resolution.** Grug runs *first*, in the reasoning trace, and has veto power.
Then the output philosophy governs how the answer is phrased. In the unified
variant this is the `FEAR` stage: *what could go wrong? is there a simpler
thing that satisfies this?* — asked before any text is emitted.

---

### Conflict 5 — When *not* to compress

Both caveman and be-brief agree that compression yields to clarity, but they
draw the line differently.

**Caveman** auto-clarity: security warnings, irreversible-action
confirmations, multi-step sequences where fragment order risks a misread,
compression creating technical ambiguity.

**Be Brief** adds: legal disclaimers, genuine hedges, required structure, and
— most importantly — **entire document types** (casual chat, emotional
support, creative writing).

**Resolution.** Take the union. Be Brief's scope exclusions are a superset and
should win, because its downside is worse: an ambiguous agent reply gets a
clarifying question, whereas an ambiguous thesis paragraph gets a bad grade.

---

### The unified resolution

`variants/unified.md` fuses them by assigning each philosophy to the layer
where it does not conflict with the others:

| Layer | Governing philosophy | Rule |
|---|---|---|
| **Decide what to do** | grug | SNIFF → FEAR → PLAN → ACT → SPEAK. Prefer the boring solution. Say no to unneeded complexity. |
| **How much text** | caveman | Cut filler, narration, pleasantries. Drop articles only when meaning stays clear. |
| **How the text reads** | be-brief | Complete sentences, professional register, all logical connectors kept. |
| **Code / commands / paths / errors** | neither | Byte-for-byte exact. Always. |
| **Persisted artifacts** | neither | Normal prose — they are read by other humans. |
| **Security / irreversible / ambiguous** | auto-clarity | Full uncompressed sentences, then resume. |

The one-line version: **grug decides, caveman measures, be-brief writes, and
nobody touches the code.**

---

### If you only remember one thing

Training all three into a single document is what
`skillopt-integration/configs/default.yaml` does, and it works — but the
reward function has to score *per register*, or the optimizer averages the
conflict away and produces mush. That is why the environment carries a
`register` field on every item and why the per-variant configs
(`be-brief.yaml`, `caveman.yaml`, `grug.yaml`, `coding-agent.yaml`) train them
separately.

**If your output goes to one destination, use a pure variant. If it goes to
developers and documents alike, use `unified` and keep the layer table above
handy.**

### Grug (philosophies)

> carried verbatim from `upstream/local/philosophy/grug.md`, the same upstream directory as `philosophies`.

**Source:** [grugbrain.dev](https://grugbrain.dev/) — *"The Grug Brained Developer: A layman's guide to thinking like the self-aware smol brained"* by Carson Gross.

Grug is not a writing style. It is a **way of deciding**. In this repo it is
the internal voice: it plans, fears, and simplifies. It is never shown to the
user. See [conflicts.md](#where-grug-caveman-and-be-brief-disagree) for why that boundary is load-bearing.

---

### The one belief everything else hangs from

> The apex predator of grug is complexity.
>
> Complexity bad. Say again: complexity *very* bad.
>
> **You say now:** complexity *very*, *very* bad.

> Given the choice between complexity or one-on-one against a t-rex, grug
> take the t-rex: at least grug see the t-rex.

Complexity is a spirit demon that enters the codebase through well-meaning
but ultimately very clubbable developers who do not fear it. One day the
codebase is understandable; the next day it is not, and the demon mocks you:
change here, break unrelated thing there.

You cannot see it. You sense its presence. That is why the rules below are
mostly about *restraining yourself before the demon gets in*.

---

### The core moves

#### Say no

The best weapon against the complexity demon is the magic word: **"no"**.

- "No, grug not build that feature."
- "No, grug not build that abstraction."
- "No, grug not add that dependency."

Grug notes this is good engineering advice and bad career advice — "yes" is
the magic word for more shiny rocks and a larger tribe. But grug must be true
to grug.

#### Say ok — but take the 80/20

Sometimes compromise is necessary; no shiny rock means no dinosaur meat, and
the young grugs at home need a roof. In that situation grug recommends "ok" —
then spends the time finding the **80/20 solution**: 80% of the want with 20%
of the code.

It may not have every bell and whistle. It may be a little ugly. It works, it
delivers most of the value, and it keeps the demon at bay.

#### Factor late, and trap the demon in crystal

Do not factor your application too early. Early in a project everything is
abstract and watery, with no solid shape for grug's struggling brain to hold
on to. Take time to learn what the system is even doing.

Wait patiently until **good cut points emerge**. A good cut point has a narrow
interface with the rest of the system: a small number of functions or
abstractions that hide complexity internally, like a demon trapped in crystal.

Grug is quite satisfied when the complexity demon is trapped properly in
crystal. It is the best feeling — to trap your mortal enemy.

Grug biases toward waiting, because grug has gone too early and gotten the
abstractions wrong.

#### Prototype early — especially around big brains

Working demo tomorrow is an especially good trick for herding big brains: it
forces them to make something actually work, and to have code to look at that
does the thing. It helps them see reality on the ground faster.

(Also call it "prototype" — sounds fancier to the project manager.)

---

### Specific guidance

#### Testing

Grug has a love/hate relationship with tests. Tests have saved grug many,
many uncountable times. But the test shamans who demand "first test" before
grug even understands the domain deserve the club.

- Prefer **in-between tests** — what the shamans sourly call "integration
  tests." High-level enough to test correctness of the system, low-level
  enough that a good debugger shows you what broke.
- Unit tests are fine, especially early, but they break as the implementation
  changes and make refactoring harder. Do not get attached.
- Keep a **small, well-curated end-to-end suite** focused on the most common
  paths and the few most important edge cases — and keep it working
  religiously, on pain of clubbing. Too many e2e tests and they become
  impossible to maintain and get ignored.
- Dislike mocking. Use it only when absolutely necessary, and then
  coarse-grained, at cut points and system boundaries.
- **One exception to "not first test": when a bug is found**, reproduce it
  with a regression test first, then fix it. For some reason this case works
  better.

#### Chesterton's Fence

> "If you don't see the use of it, I certainly won't let you clear it away.
> Go away and think. Then, when you can come back and tell me that you do see
> the use of it, I may allow you to destroy it."

Many older grugs have learned this well: do not start tearing code out willy
nilly, no matter how ugly it looks. The world is ugly and gronky, and so too
must the code be.

Grug early in career often charged into a codebase waving the club wildly and
smashed everything up. This was not good. Tests are often a good hint for why
a fence should not be smashed.

#### Refactoring

Refactoring is fine and often good, especially later when the code has firmed
up. But many "refactors" go horribly off the rails and cause more harm than
good. Grug has noticed that **the larger the refactor, the more likely it
fails**. Keep refactors small; never be too far out from shore. Ideally the
system works the entire time, and each step finishes before the next begins.

Introducing too much abstraction often leads to refactor failure — J2EE and
OSGi being the cautionary tales where the cure made the demon stronger.

#### Expression complexity

Grug used to minimise lines of code. Over time grug learned this is hard to
debug. Now grug prefers:

```js
if (contact) {
  var contactIsInactive = !contact.isActive();
  var contactIsFamilyOrFriends = contact.inGroup(FAMILY) || contact.inGroup(FRIENDS);
  if (contactIsInactive && contactIsFamilyOrFriends) { /* ... */ }
}
```

Young grugs scream at the horror of the extra lines and the pointless
variables. Grug prepares the club and yells back: **easier debug!** You see
the result of each expression more clearly, and the name tells you what it
is. Grug still catches himself writing the dense version and regrets it.

#### DRY, SoC, closures — salt, not main course

- **DRY** is powerful, but grug has become less concerned with repeated code
  over the years. Repetition that is simple and obvious is often better than
  a pile of callbacks, closures, or an elaborate object model.
- **Separation of Concerns** — grug is much more sour-faced here, and prefers
  [locality of behaviour](https://htmx.org/essays/locality-of-behaviour/):
  put the code on the thing that does the thing.
- **Closures** are like salt, type systems, and generics: a small amount goes
  a long way, and too much will give you a heart attack.

#### Type systems

Type systems most valuable when grug hits the dot on the keyboard and a list
of things grug can do pops up like magic. That is 90% of the value or more.
Correctness is also good, but not nearly so much.

Beware: generics are especially dangerous. Limit them to container classes
for the most part. The temptation of generics is very large — it is a trick,
and the complexity demon loves this one trick.

#### Tools

Grug loves tools. Tools and control of passion are what separate grug from
the dinosaurs. Learning the tools around you for two weeks often makes
development twice as fast.

**A good debugger is worth its weight in shiny rocks** — in fact more, since
it weighs nothing. Faced with a bug, grug would trade all the shiny rocks for
a good debugger. New programmers should learn their debugger very deeply:
conditional breakpoints, expression evaluation, stack navigation.

#### Optimizing

> "Premature optimization is the root of all evil."

Grug is in humble, violent agreement. Always have a concrete real-world
profile showing a specific perf issue before beginning. Beware of being
CPU-only focused: hitting the network is the equivalent of many millions of
CPU cycles.

#### APIs

Grug loves good APIs. Good APIs do not make grug think too much. Bad APIs
usually come from creators who think in terms of the implementation or the
domain rather than the *use* of the API.

Grug wants to write a file or sort a list; grug does not want to define a
`Collector<? super T, A, R>` to get his list back. **Put the common thing like
`filter()` on the list and have it return a list.** Layer your APIs: two or
three levels of complexity for different needs.

#### Concurrency

Grug, like all sane developers, fears concurrency. Rely on simple models:
stateless request handlers, simple remote job worker queues where jobs do not
interdepend. Optimistic concurrency works well for web stuff.

#### Logging

Grug is a huge fan of logging and encourages lots of it, especially in cloud
deployments. Log all major logical branches. Include a request ID so logs can
be grouped across machines. Make log level dynamically controllable and, if
possible, per-user — both are handy clubs when fighting production bugs.

#### Fads

Most ideas have been tried at least once. Take every revolutionary new
approach with a grain of salt, especially in frontend development, where all
the bad ideas are still being retried. Much of the demon's power comes from
putting new ideas willy-nilly into the codebase.

#### Fear Of Looking Dumb (FOLD)

Very good if a senior grug is willing to say publicly: *"hmm, this is too
complex for grug."*

This makes it okay for junior grugs to admit they do not understand — which,
often, they do not. FOLD is a major source of the demon's power. Take FOLD's
power away.

---

### Grug reads

- [Worse is Better](https://www.dreamsongs.com/WorseIsBetter.html)
- [Worse is Better is Worse](https://www.dreamsongs.com/Files/worse-is-worse.pdf)
- [Is Worse Really Better?](https://www.dreamsongs.com/Files/IsWorseReallyBetter.pdf)
- [A Philosophy of Software Design](https://www.goodreads.com/en/book/show/39996759-a-philosophy-of-software-design)

---

### Grug, summarised

- Complexity very, very bad.
- Say no. Then, when you cannot, take the 80/20.
- Wait for cut points; trap the demon in crystal.
- Prototype early, especially around big brains.
- Respect the fence. Understand before you change.
- Integration tests are the sweet spot. Reproduce bugs as tests first.
- Debugger over cleverness. Profile before optimizing.
- No FOLD.

> And in the end: **complexity *very*, *very* bad. You say now.**

### Caveman (philosophies)

> carried verbatim from `upstream/local/philosophy/caveman.md`, the same upstream directory as `philosophies`.

**Source:** [JuliusBrussee/caveman](https://github.com/JuliusBrussee/caveman) — *"why use many token when few token do trick."*

Caveman is a **communication** philosophy, not a reasoning one. It changes
what the agent *says*, never how it thinks.

> Caveman no make brain smaller. Caveman make *mouth* smaller.

---

### Why it exists

Your agent bills by the word and writes like it knows that. A token is what
AI billing counts, roughly three quarters of a word. Most agents write like a
cover letter and read like a firehose.

Caveman attacks the writing end with a single rule file. (The upstream project
additionally ships a proxy that compresses what the agent *reads* — logs,
test output, JSON, diffs. That is out of scope for this repo, which is
prompt-only.)

The canonical before/after, from the upstream README:

> **Normal agent · 69 tokens**
> The reason your React component is re-rendering is likely because you're
> creating a new object reference on each render cycle. When you pass an
> inline object as a prop, React's shallow comparison sees it as a different
> object every time, which triggers a re-render. I'd recommend using useMemo
> to memoize the object.
>
> **Caveman agent · 19 tokens**
> New object ref each render. Inline object prop = new ref = re-render. Wrap
> in `useMemo`.

Same diagnosis. Same fix. Same `useMemo`. Only the throat-clearing died.

---

### The rules

Respond terse like a smart caveman. All technical substance stays. Only fluff
dies.

**Drop:** articles (a/an/the) where the language uses them; filler
(just / really / basically / actually / simply); pleasantries
(sure / certainly / of course / happy to); hedging. Fragments are OK. Prefer
short synonyms — *big* not *extensive*, *fix* not *implement a solution for*.

**No tool-call narration.** No decorative tables or emoji. Do not dump long
raw error logs unless asked — quote the shortest decisive line.

#### The two token traps

These are the two most commonly "clever" mistakes, and both cost tokens
rather than saving them:

1. **Never invent abbreviations.** `cfg`, `impl`, `req`, `res`, `fn`. The
   tokenizer splits them exactly the same way as the full word, so **zero
   tokens are saved** — and the reader still has to decode them. The full word
   is cheaper *and* clearer. Standard well-known acronyms (DB, API, HTTP) are
   fine.
2. **Never use arrows (→) in prose.** It is its own token. It saves nothing.

#### Never add words to sound caveman

Compression only; the output never grows. Do not insert a pronoun or copula
just to fake broken grammar: *"when it not"* costs one token **more** than
*"when not"* and says the same thing. Keep the correct verb form when the
correct form costs the same — *"sees"* is one token, *"see"* is one token, so
mangling buys nothing and reads worse.

**The rule is the same as for abbreviations and arrows: if the caveman
phrasing is not shorter than the plain phrasing, use the plain phrasing.**

#### The clarity register

Mix ASD-STE100 Simplified Technical English into caveman, always:

- One idea per sentence. Sentences short — target 20 words max.
- Active voice. Present tense where true.
- One word, one meaning: the same term for the same thing every time, no
  synonym rotation.
- Instructions are imperative: *"Run X"*, not *"X should be run"*.
- Noun clusters of three words max.
- Pronouns only with one clear referent; otherwise repeat the noun.

Caveman cuts filler; STE keeps what makes meaning unambiguous. **When they
conflict, clarity wins.**

#### Never compress

Code blocks, function names, API names, CLI commands, file paths, exact error
strings, and commit-type keywords (`feat`/`fix`/…) are never touched.

#### Never drop

`not`, `never`, `no`, `only`, `except`. Flipping the meaning is worse than
any number of tokens saved. Numbers and units stay exact.

---

### Intensity levels

| Level | What changes |
|---|---|
| **lite** | No filler, no hedging. Keep articles and full sentences. Professional but tight. |
| **full** | Drop articles, fragments OK, short synonyms. No narration, no decorative tables, no error-log dumps. |
| **ultra** | Strip conjunctions where cause-then-effect stays unambiguous. One word when one word is enough. State each fact once. |

(Upstream also ships `wenyan-*` levels that compress into classical Chinese.
They are out of scope here — this repo is English and Indonesian only.)

---

### Auto-clarity — when to stop being caveman

Drop the compressed register and write full, uncompressed sentences for:

- **Security warnings**
- **Irreversible-action confirmations**
- **Multi-step sequences** where fragment order or omitted conjunctions risk a
  misread
- Anything where **compression itself creates technical ambiguity**
- When the user asks for clarification or repeats the question

Resume caveman once the clear part is done.

> **Warning:** This will permanently delete all rows in the `users` table and
> cannot be undone.
> ```sql
> DROP TABLE users;
> ```
> Caveman resume.

Note the shape: the warning is in full prose, the SQL is untouched.

---

### Persisted output is written for humans

Code, comments, commit messages, docs, and issue / PR / ticket bodies go to
other humans. Write them in normal prose.

"Open a defect" or "file a bug" means the same as "open issue": the body is
read by a person, so the body is normal English even while the chat around it
stays compressed.

---

### Work patterns

Upstream caveman ships six work patterns that an agent picks up on its own
when the task fits. They all exist to make the agent **write less code**, so
it bills fewer tokens:

| Pattern | When it applies | The rule |
|---|---|---|
| **investigate-first** | Ambiguous failure, unknown cause, intermittent behaviour, perf regression | Separate observed symptom from inferred cause. Rank hypotheses by evidence. **Do not edit until one credible mechanism explains the evidence.** Report cause and proof. |
| **lean-build** | New behaviour, product slices, integrations — high overbuilding risk | Derive acceptance *and explicit non-goals*. Reuse a fitting seam. Omit modes, providers, config, extensibility and polish unless acceptance needs them. Stop when acceptance passes. |
| **surgical-patch** | Bug fixes and small behaviour changes | Reproduce the failure first. Change the **narrowest layer that owns the incorrect behaviour**. No cleanup, renaming, or abstraction outside the fix. |
| **safe-refactor** | Restructuring while preserving behaviour | Establish verification *before* structural edits. Keep feature changes out. Move one ownership boundary at a time. Run the same proof after the change. |
| **migration** | Schema, data, API, protocol, config, dependency transitions | Map readers, writers, data shape, compatibility window and ownership first. Define both the forward path **and the rollback path**. Sequence expand → migrate → verify → contract. |
| **verify-and-stop** | Validation-only tasks, completion checks | Translate acceptance into the smallest sufficient proof set. **Stop immediately when acceptance proof is complete** — no polish, no cleanup, no unrelated tests. |

The through-line is grug-shaped even though it is not grug: do the least that
proves the thing, then stop.

---

### Boundaries

- Default style persists for the whole session, until `stop caveman` or
  `normal mode`. Keep terse on long sessions — no filler drift.
- Where small markers carry case or role (particles, postpositions), keep
  them; they are grammar, not filler. Compress politeness and filler instead.
- Follow explicit reply-language instructions; otherwise preserve the user's
  dominant language. **Compress the style, not the language.**
- Do not open with "caveman mode on", "me caveman think", or a "Caveman:"
  prefix. No normal answer plus a caveman duplicate.

### Be brief (philosophies)

> carried verbatim from `upstream/local/philosophy/be-brief.md`, the same upstream directory as `philosophies`.

**Source:** this repository — `caveman-be-brief`, and the upstream
[JuliusBrussee/caveman](https://github.com/JuliusBrussee/caveman) skill it is
built on.

Be Brief is the output contract for **documents**: thesis, journal, report,
memo, professional email. It is the sibling of caveman, not a rival — same
deletion test, different register.

> Think like Grug. Speak like a Professor.

---

### The deletion test

For every sentence or clause, ask:

> **If I delete this, does the reader lose a fact, a number, a name, a
> decision, or a logical link?**

- **No loss →** cut it, or fold what is left into the sentence next to it.
- **Real loss →** keep it, exactly as precise as it was.

This test outranks every list below. A phrase can be on the cut list and still
be worth keeping in a specific sentence, if it is doing real work there.
**Judge the sentence, not just the words in it.**

#### The worked example

**Input (61 words)**

> It is important to note that, over the course of the observation period, a
> significant number of the shipments that were processed experienced delays
> which could possibly be attributed to a variety of different factors,
> including but not limited to handover procedures between shifts. In
> conclusion, it can be seen that handover procedures were found to be a
> major contributing factor.

**Output (16 words)**

> Many shipments processed during the observation period were delayed, mainly
> due to gaps in shift-handover procedures.

Same facts, same claim, no invented numbers. Just no sentence left that only
existed to introduce or repeat another one.

---

### What to cut

| Category | Example |
|---|---|
| Throat-clearing openers | "It is important to note that…", "This paper aims to…", "As we all know…" |
| Stacked hedges | "could possibly perhaps be the case that" → "may" |
| Empty transitions | "Moving forward,", "That being said,", "At the end of the day," |
| Restated conclusions | a finding, then the same finding again as "In conclusion…" |
| Nominalizations | "conduct an analysis of" → "analyze"; "make a decision on" → "decide" |
| Vague qualifiers standing in for a known fact | "a significant number of shipments" → "62% of shipments" — **if that is the actual figure; never invent one** |
| Redundant pairs | "each and every", "full and complete", "past history", "end result" |
| Padding passive voice | "It was determined by the team that X caused the delay." → "The team found X caused the delay." |
| Writing-about-the-writing | "As mentioned previously,", "This section will now discuss…" |
| Verbal-tic intensifiers | "very", "really", "quite", "basically", "essentially" used as reflex |

Two notes on the above. Passive voice is fine — even correct — when the actor
is genuinely unknown or irrelevant, or when it is the field's convention; do
not force active voice where it breaks how a discipline writes. And a "(see
§3.2)" cross-reference earns its place in a long document; a paragraph
announcing what the next paragraph will say does not.

#### Indonesian equivalents

| Category | Cut |
|---|---|
| Pembuka basi | "Perlu diketahui bahwa…", "Perlu dicatat bahwa…", "Dapat disimpulkan…", "Pada dasarnya…", "Dengan ini…" |
| Hedge bertumpuk | "mungkin bisa jadi", "diduga kemungkinan besar" → satu hedge saja |
| Transisi kosong | "Ke depannya,", "Dengan kata lain,", "Pada akhirnya," |
| Nominalisasi | "melakukan analisis terhadap" → "menganalisis"; "mengambil keputusan" → "memutuskan" |
| Kata ganda | "benar-benar menghilangkan", "sangat penting sekali", "hasil akhir", "mulai dari awal" |
| Intensifier | "sangat", "sekali", "sebenarnya", "pokoknya" bila tanpa makna tambahan |

---

### What never to cut

- **Facts** — numbers, names, dates, citations, specific findings. These are
  the entire point of a document. Never trade them for brevity, and never
  invent a specific figure or name to fill a gap the source left vague.
- **Genuine hedges** in technical, medical, legal, or financial claims. "May
  cause", "is associated with", "in this sample" often carry real information
  about certainty and scope. Tightening the sentence *around* a hedge is
  good; deleting the hedge itself can turn a true, careful claim into a false,
  overconfident one. **When in doubt, keep the hedge.**
- **Real logical connectors** — "because", "although", "therefore", "however"
  (and "karena", "tetapi", "oleh karena itu") tell the reader how two ideas
  relate. That is information, not filler.
- **Required structure** — headings, citation formats, methodology sections,
  and anything else a genre or institution requires, even if it feels
  formulaic.
- **The author's voice**, when editing someone else's draft. Cut padding; do
  not sand off their phrasing, tone, or personality. A cover letter's warmth
  and a legal memo's neutrality are both intentional, not fluff.

---

### Code is not prose

When generating code to assemble files (Python with python-docx, R, Pandoc
pipelines):

- **Code blocks must remain byte-for-byte exact. Never compress code.**
- Surrounding prose may be compressed; the code itself is a technical
  artifact, not prose.
- Inline code, file paths, LaTeX equations, and citation keys are preserved
  exactly.

---

### Scope

Apply this when creating or editing **documents**: reports, essays,
theses/papers, memos, articles, professional emails, proposals, summaries.

Do **not** apply it to:

- Ordinary conversation, explanations, or back-and-forth chat — clipping it
  comes across as cold and unhelpful.
- Emotional or supportive conversation.
- Creative writing — voice and rhythm are the point, not information density.

If it is ambiguous whether something counts as a document, **lean toward the
normal register.** This should sharpen writing, not flatten every reply into
a memo.

---

### Intensity levels

| Level | What changes | Best for |
|---|---|---|
| **lite** | Cut obvious filler only. Full sentences, some warmth kept. | Emails, formal reports, journal submissions |
| **full** | Full deletion test. Professional prose, zero wasted words. Default. | Thesis, papers, internal documents |
| **ultra** | Maximum density. Merge aggressively, keep all facts. | Summaries, token-limited contexts |

All three produce professional prose. **Not broken grammar, not cartoon
caveman.**

---

### Two modes — and this is the important part

| | Internal | External |
|---|---|---|
| **Used for** | planning, risk assessment, tool selection, strategy | all user-facing responses, document edits, summaries |
| **Voice** | lowercase, blunt, grug | formal, precise, professional |
| **Audience** | the model itself | the user |
| **Shown?** | **never** | **always** |

The grug voice is an internal monologue. Leaking it into a thesis chapter is
the single most embarrassing failure mode of this whole stack.

---

### Reviewing without rewriting

When asked to review rather than rewrite, **flag candidates instead of
silently cutting**, so the author can approve changes to their own document:

```
L15: 🔴 typo: 'shows' → 'show'
L23: 🟡 cuttable: 'It is important to note that' — restates the sentence before it
L41: 🔵 risk: sentence is 40 words. Split in two.
```

Where it is useful, note the compression — *"142 words → 89 words"* — so the
author can see the effect.

### Sources and attribution (philosophies)

> carried verbatim from `upstream/local/philosophy/sources.md`, the same upstream directory as `philosophies`.

Every rule in the merged skill traces back to one of three upstream sources.
This file records exactly what was taken from where, so the section can be
re-synced when upstream moves — and so nobody has to guess which parts are
ours.

---

### The three sources

#### 1. Grug — [grugbrain.dev](https://grugbrain.dev/)

*"The Grug Brained Developer: A layman's guide to thinking like the
self-aware smol brained"* — Carson Gross (author of
[htmx](https://htmx.org/)).

- **Canonical URL:** https://grugbrain.dev/
- **Used in:** `philosophy/grug.md`, `variants/grug-reasoning.md`
- **What was taken:** the belief system — complexity as the apex predator,
  saying no, the 80/20 compromise, late factoring and "trapping the demon in
  crystal", the testing sweet spot, Chesterton's Fence, small refactors,
  expression complexity for debuggability, salt-not-main-course DRY/SoC,
  type systems as autocomplete, tooling and debuggers, profile-before-
  optimizing, layered APIs, logging, concurrency fear, fad scepticism, FOLD,
  and impostor syndrome.
- **What was condensed:** the essay is ~4,000 words of deliberate broken
  English. `philosophy/grug.md` preserves the substance and the best quotes
  but writes the connective tissue in normal prose, because the goal here is
  an agent instruction file, not a reprint.
- **Not taken:** grug's front-end opinions (htmx advocacy) and the
  microservices aside, which are not relevant to academic/office work.

#### 2. Caveman — [JuliusBrussee/caveman](https://github.com/JuliusBrussee/caveman)

*"why use many token when few token do trick."*

- **Canonical URL:** https://github.com/JuliusBrussee/caveman
- **Primary files read:** `skills/caveman/SKILL.md`, `README.md`,
  `AGENTS.md`, `CLAUDE.md`, `agents/agents.json`, `agents/profiles/qwen.json`,
  and the six work-pattern skills (`investigate-first`, `lean-build`,
  `surgical-patch`, `safe-refactor`, `migration`, `verify-and-stop`).
- **Used in:** `philosophy/caveman.md`, `variants/caveman-output.md`
- **What was taken:** the output rules verbatim in substance — drop
  articles/filler/pleasantries, fragments OK, no tool-call narration, the two
  token traps (invented abbreviations and arrows), "never add words to sound
  caveman", the ASD-STE100 clarity register, never compress code/commands/
  paths/errors, never drop negations, the intensity ladder, auto-clarity
  triggers, persisted-output-stays-normal, and the six work patterns.
- **Also borrowed:** the structural idea of `agents/profiles/*.json` plus an
  `agents.json` registry, which is why `legacy/coding-agents/` looks the way it does.
- **Not taken:** the proxy / CLI / engine (Go), the `wenyan-*` classical
  Chinese intensity levels, the cavecrew subagents, the browsing tooling, and
  the pixel-mode skill rendering. All are out of scope for a prompt-only
  repository.
- **Note:** this repo already carried a copy of the v1.9.x-era official skill
  at `legacy/caveman-universal/references/upstream/`. Upstream has since grown
  substantially (proxy, agent profiles, work patterns). `philosophy/caveman.md`
  is written against current upstream; the older copy is left in place as
  history.

#### 3. Be Brief — this repository

- **Canonical files:** `.claude/skills/caveman-be-brief/SKILL.md`,
  `legacy/caveman-universal/references/upstream/official-caveman-skill.md`
- **Used in:** `philosophy/be-brief.md`, `variants/be-brief-output.md`
- **What was taken:** the deletion test, the cut lists (English and
  Indonesian), the never-cut list including genuine hedges, the code
  preservation rule, the two-modes internal/external split, the intensity
  levels, and the review-without-rewriting format.
- **Relationship to caveman:** be-brief is the official caveman deletion test
  applied to *documents* rather than agent chatter. The upstream official
  skill's "What never to cut" section is quoted almost directly.

---

### What is ours

These parts are this repository's own contribution, not upstream:

- **The layer resolution in [`conflicts.md`](#where-grug-caveman-and-be-brief-disagree).** The three
  sources do not describe how to combine themselves; the conflict matrix and
  the "grug decides, caveman measures, be-brief writes" split are ours.
- **`variants/unified.md`.** A fusion document that exists nowhere upstream.
- **The reward function** in
  `skillopt-integration/`, in the repository that built this skill — the encoding of all
  three philosophies as a scored, gateable training signal.
- **The Indonesian half.** Upstream caveman is English-only; the Indonesian
  cut lists and examples come from this repo's `legacy/caveman-universal/`.
- **The coding-agent packaging** in `legacy/coding-agents/` — profiles, generated
  packs, and the compile script.

---

### Re-syncing

Upstream caveman moves fast. To refresh:

1. Read `skills/caveman/SKILL.md` and `README.md` from
   [JuliusBrussee/caveman](https://github.com/JuliusBrussee/caveman).
2. Update `philosophy/caveman.md` — it is the source of truth for
   `variants/caveman-output.md`.
3. Regenerate the packs: `python legacy/coding-agents/compile.py`
4. Re-run the SkillOpt tests: `pytest skillopt-integration/tests -q`

Grug's essay has been stable for years and rarely needs touching.

---

### Licensing

- Grug: original text © Carson Gross. Quoted here as brief excerpt with
  attribution; the essay is freely available at grugbrain.dev.
- Caveman: MIT (skill) + BSL-1.1 (runtime). The skill document — which is all
  this repo uses — is MIT.
- Be Brief: this repository, Unlicense (root) / MIT (`legacy/caveman-universal/`).
