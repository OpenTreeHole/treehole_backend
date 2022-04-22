-- upgrade --
ALTER TABLE `report`
    DROP FOREIGN KEY `fk_report_user_435a3506`;
ALTER TABLE `report` RENAME COLUMN `dealed` TO `dealt`;
ALTER TABLE `report` RENAME COLUMN `dealed_by_id` TO `dealt_by_id`;
ALTER TABLE `report`
    ADD CONSTRAINT `fk_report_user_2a3c14d2` FOREIGN KEY (`dealt_by_id`) REFERENCES `user` (`id`) ON DELETE CASCADE;
-- downgrade --
ALTER TABLE `report`
    DROP FOREIGN KEY `fk_report_user_2a3c14d2`;
ALTER TABLE `report` RENAME COLUMN `dealt` TO `dealed`;
ALTER TABLE `report` RENAME COLUMN `dealt_by_id` TO `dealed_by_id`;
ALTER TABLE `report`
    ADD CONSTRAINT `fk_report_user_435a3506` FOREIGN KEY (`dealed_by_id`) REFERENCES `user` (`id`) ON DELETE CASCADE;
