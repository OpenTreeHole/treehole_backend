-- upgrade --
ALTER TABLE `floor` ADD `ip_location` VARCHAR(50) NOT NULL  DEFAULT '';
-- downgrade --
ALTER TABLE `floor` DROP COLUMN `ip_location`;
