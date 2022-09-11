# RouteDiffer

RouteDiffer is a utility I had need of for doing som Layer 3 dynamic routing migrations.  The overall goal is to simply pull the current routing table, store it, peform the migration and compare the new/updated routing table to the original to spot any changes, more specifically, any routes that did not make it over.

Admittedly, this is not a common task nor I suspect a common need for such a utility.  However, the migrations were taking place in the core devices where there were thousands of routes.  The potential was there that something was missed or some seldom used route did not make it through the migration and may not be noticed for some time.  Yes, you could use some Linux _diff_ tool or some other similar utility, but who wants to go cut and paste thousands of routes manually to perform such a thing.  Therefore, since there were no other tools available in the given environment in which to perform such a task, it was decided to create some kind of utility that could provide a source of truth (the original routing table) and use that to, as best as possible, determine if there were any routes missing post-migration.

More to come!