CREATE TABLE IF NOT EXISTS `ad_events` (
  `id` INT PRIMARY KEY AUTO_INCREMENT,
  `event_type` ENUM('click', 'view', 'impression') NOT NULL,
  `location` VARCHAR(25) NOT NULL DEFAULT 'Unknown',
  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);