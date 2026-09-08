-- Optional one-time backfill for records that predate portfolio_category.
-- These two cases are unambiguous because link is the website URL and
-- instagram_url is the social profile URL. Review all remaining NULL values
-- in the admin panel; content must not be guessed from an image alone.
UPDATE main_projects_example
SET portfolio_category = 'website'
WHERE portfolio_category IS NULL AND link IS NOT NULL AND TRIM(link) <> '';

UPDATE main_projects_example
SET portfolio_category = 'social_media'
WHERE portfolio_category IS NULL
  AND instagram_url IS NOT NULL AND TRIM(instagram_url) <> '';
