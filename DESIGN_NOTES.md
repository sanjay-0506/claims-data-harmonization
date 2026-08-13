# Design Notes

## 1. What I Built

I built a multi-source claims data harmonization pipeline that takes claims
data from three vendors and converts them into one consistent structure.

The pipeline has separate stages for:

1. Loading the source files
2. Standardizing column names
3. Cleaning and validating records
4. Handling Source C claim versions
5. Normalizing diagnosis codes
6. Expanding multiple diagnosis codes into separate rows
7. Looking up diagnosis descriptions
8. Combining the three sources
9. Removing duplicates at the required grain
10. Validating the final output

Each stage records the number of rows entering and leaving the stage,
along with the reason for dropped records.

I also built a small FastAPI application around the pipeline. A run gets a
unique run ID, and the API provides the stage information, acceptance
checks, summary information, and a download of the final dataset.

---

## 2. What Problem It Solves

The three vendors contained the same general claims information, but they
did not use the same column names or data formats.

For example, the patient identifier appeared as:

- patient_id in Source A
- member_id in Source B
- pt_ref in Source C

The same happened with claim IDs, service dates, diagnosis codes,
provider identifiers, gender, plans and billing amounts.

The diagnosis representation was also different.

Source A had multiple diagnosis columns:

diagnosis_code_1 through diagnosis_code_8.

Source B had one diagnosis column.

Source C stored multiple diagnosis codes in one string separated by `|`.

Simply concatenating the three files would therefore produce inconsistent
columns and inconsistent diagnosis records.

The pipeline first converts these different representations into one
canonical structure and then combines the data.

---

## 3. Why I Did It This Way

### Standardization

I standardized the source-specific column names into a common naming scheme
before combining the sources.

This makes the later processing independent of which vendor produced the
record.

### Missing patients

Rows without a patient identifier are removed because the assignment
explicitly requires this.

I applied this before the final combination so invalid records do not
enter the final dataset.

### Date filtering

I kept only records whose service date falls between:

2018-01-01 and 2025-02-28.

The date is converted into a proper datetime value before the final output.

### Gender

The vendors use different representations.

Source A already uses M/F.

Source B uses numeric values.

Source C uses Male/Female.

These are normalized to M/F.

### Diagnosis codes

Diagnosis codes are converted to uppercase and dots are removed.

For example:

E11.9

becomes:

E119

This is done before the dictionary lookup so the same diagnosis code has
the same representation across all vendors.

### Source C versions

Source C contains multiple versions of some claims.

I found that Source C contains 24,186 rows, but only 20,001 unique latest
claim versions.

I chose to keep the latest version of each claim because the version field
represents revisions of the same claim.

This reduced Source C from 24,186 rows to 20,001 rows.

I made this a separate tracked stage so the dropped 4,185 rows are visible
instead of silently disappearing.

### Diagnosis expansion

The final grain required by the assignment is one row per:

source + claim + diagnosis code.

Therefore multiple diagnosis codes have to become separate rows.

For Source A, the eight diagnosis columns are converted into rows.

For Source B, the diagnosis column becomes one diagnosis row.

For Source C, the `|` separated diagnosis values are split into individual
diagnosis rows.

### Diagnosis dictionary

The diagnosis dictionary is used to populate DIAGNOSIS_DESC.

If a diagnosis code is not present in the dictionary, I keep the diagnosis
record and leave the description missing rather than dropping the claim.

I chose this because the assignment says that not every code appears in
the dictionary, and dropping a valid claim because the description is
missing would lose source data.

### Final grain

The final duplicate check uses:

SRC + CLAIM_ID + DIAGNOSIS_CODE

because this is the grain specified by the assignment.

---

## 4. What Went Wrong Along the Way

My first implementation of the diagnosis enrichment logic had a problem
when the dictionary was merged more than once.

The merge created columns such as `dx_code_x` and `dx_code_y`, which caused
the cleanup code to try to remove a column that no longer existed.

I fixed this by making the diagnosis enrichment step consistent about
which diagnosis column is retained.

I also changed Source C version handling to return information about how
many rows were removed. This allowed the pipeline tracker to show the
version-resolution stage separately.

The final pipeline currently produces:

- 159,704 final rows
- 68,205 distinct claims
- 11,963 distinct patients
- 44 distinct diagnosis codes

For P00042, the final output contains 7 rows and 7 distinct diagnosis
codes.

These values match the acceptance values provided in the assignment.

---

## 5. What I Was Not Sure About

The main ambiguity I found was how Source C's version field should be
interpreted.

There are multiple versions of the same claim, so keeping every version
would retain superseded records.

I tested the behavior and found that keeping the latest version produces
the expected final row and claim counts.

I therefore chose latest-version processing.

If this were a production pipeline, I would confirm this rule with the
data owner rather than relying only on the observed data.

Another assumption is that diagnosis codes missing from the dictionary
should remain in the output with a missing description. I chose this to
avoid losing otherwise valid claims.

---

## 6. What I Would Do Differently

The current implementation is designed for the assignment and moderate
data volumes.

For a much larger dataset, I would avoid keeping the entire pipeline
output in application memory.

I would also consider:

- streaming or chunked file processing
- persistent storage for run information
- storing pipeline outputs in object storage
- database-backed run metadata
- structured logging
- more detailed data-quality metrics
- configuration-driven source mappings
- better monitoring and error handling

The current API stores runs in memory because persistence was not required
for this assignment.

I also added lazy CSV generation. The final CSV is only created when the
user requests a download. Once created, later downloads reuse the existing
file.

---

## 7. Final Pipeline Result

The final pipeline currently produces:

| Metric | Result |
|---|---:|
| Final rows | 159,704 |
| Distinct claims | 68,205 |
| Distinct patients | 11,963 |
| Distinct diagnosis codes | 44 |
| P00042 diagnosis codes | 7 |
| P00042 total rows | 7 |

The pipeline also reports stage-level row counts and drop reasons through
the API.

The acceptance endpoint checks the final output against the required
acceptance criteria and also checks that two pipeline executions produce
identical output.