-- Run once on an existing MySQL database before deploying this release.
ALTER TABLE main_projects_example
  ADD COLUMN portfolio_category VARCHAR(32) NULL,
  ADD COLUMN instagram_url VARCHAR(500) NULL,
  ADD COLUMN testimonial TEXT NULL,
  ADD COLUMN is_featured BOOLEAN NOT NULL DEFAULT FALSE,
  ADD INDEX ix_main_projects_example_portfolio_category (portfolio_category);
