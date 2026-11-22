-- Step 1: add the column as nullable so API instances still running the previous
-- version keep inserting rows without it.
ALTER TABLE "Incident" ADD COLUMN "priority" INTEGER;

-- Step 2: backfill existing rows from severity.
UPDATE "Incident"
SET "priority" = CASE "severity" WHEN 'SEV1' THEN 1 WHEN 'SEV2' THEN 2 ELSE 3 END
WHERE "priority" IS NULL;

-- Step 3: enforce the constraint.
ALTER TABLE "Incident" ALTER COLUMN "priority" SET NOT NULL;
