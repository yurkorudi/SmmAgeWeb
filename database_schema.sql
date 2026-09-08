CREATE TABLE IF NOT EXISTS contact_request (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(120) NOT NULL,
  phone VARCHAR(120) NOT NULL,
  business VARCHAR(180),
  category VARCHAR(80),
  budget VARCHAR(80),
  timeline VARCHAR(80),
  channels VARCHAR(255),
  message TEXT NOT NULL,
  created_at DATETIME NOT NULL
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS main_projects_example (
  id INT AUTO_INCREMENT PRIMARY KEY, title VARCHAR(180) NOT NULL, project_type VARCHAR(120) NOT NULL,
  description TEXT NOT NULL, duration VARCHAR(80) NOT NULL, budget VARCHAR(80) NOT NULL,
  link VARCHAR(500), image VARCHAR(300), portfolio_category VARCHAR(32), instagram_url VARCHAR(500),
  testimonial TEXT, is_featured BOOLEAN NOT NULL DEFAULT FALSE, is_active BOOLEAN NOT NULL DEFAULT TRUE,
  created_at DATETIME NOT NULL, INDEX ix_main_projects_example_portfolio_category (portfolio_category)
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS project_example (
  id INT AUTO_INCREMENT PRIMARY KEY,
  service_slug VARCHAR(80) NOT NULL,
  title VARCHAR(180) NOT NULL,
  category VARCHAR(120),
  description TEXT NOT NULL,
  image_url VARCHAR(500),
  result VARCHAR(180),
  link VARCHAR(500),
  is_featured BOOLEAN NOT NULL DEFAULT TRUE,
  created_at DATETIME NOT NULL,
  INDEX ix_project_example_service_slug (service_slug)
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
