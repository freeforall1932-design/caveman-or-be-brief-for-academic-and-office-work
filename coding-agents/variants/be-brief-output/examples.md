# Worked examples

## Professional email

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

## Report summary

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

## Where code appears

**Source:** "The build fails with `ModuleNotFoundError: No module named 'skillopt'`.
I already ran `pip install -e skillopt-integration`."

**Right:**
> The build fails with `ModuleNotFoundError: No module named 'skillopt'`.
> The editable install did not provide the package. Check that
> `skillopt-integration/` contains a `pyproject.toml`, then retry
> `pip install -e skillopt-integration`.

The error string is byte-exact. Only the surrounding prose was compressed.
