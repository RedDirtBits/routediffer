# RouteDiffer

RouteDiffer is a utility I had need of for doing some Layer 3 dynamic routing migrations.  The overall goal is to simply pull the current routing table, store it, peform the migration and compare the new/updated routing table to the original to spot any changes, more specifically, any routes that did not make it over.

Admittedly, this is not a common task nor I suspect a common need for such a utility.  However, the migrations were taking place in the core devices where there were thousands of routes.  The potential was there that something was missed or some seldom used route did not make it through the migration and may not be noticed for some time.  Yes, you could use some Linux _diff_ tool or some other similar utility, but who wants to go cut and paste thousands of routes manually to perform such a thing.  Therefore, since there were no other tools available in the given environment in which to perform such a task, it was decided to create some kind of utility that could provide a source of truth (the original routing table) and use that to, as best as possible, determine if there were any routes missing post-migration.

# Usage

Simply run the `get_routing_table` function, passing in the required arguments to create the source of truth file.  Ideally, and perhaps obviously, this should be done prior to any migrations/changes are peformed.  If the function is run again, it will check for the source of truth file and if it is found it will simply return the TextFSM formatted routes and not re-write the file.

To peform a comparison run the `compare_routing_tables` function.  This will call the `get_routing_table` function to get the current routes the peform a comparison between the source of truth file (pre-migration/pre-changes) and look for any differences.  If no differences are detected, no actions will be taken (returns None).  However, if differences are found then those will be stored in JSON format and saved to file.

# Filenames

- Source of Truth file: **pre_migration_route_table.json**
- Differences file: **missing_routes.json**

# Platforms

As of this writing, the script has been tested only on the devices listed below.  This will be updated as more testing is done.

- Cisco Nexus 7k