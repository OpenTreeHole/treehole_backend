-- upgrade --
ALTER TABLE `user` ALTER COLUMN `config` SET;
ALTER TABLE `division` ALTER COLUMN `description` SET DEFAULT '';
ALTER TABLE `division` MODIFY COLUMN `description` VARCHAR(100) NOT NULL  DEFAULT '';
ALTER TABLE `division` MODIFY COLUMN `pinned` JSON NOT NULL  COMMENT '置顶帖';
-- downgrade --
ALTER TABLE `user` ALTER COLUMN `config` SET;
ALTER TABLE `division` MODIFY COLUMN `description` VARCHAR(100);
ALTER TABLE `division` ALTER COLUMN `description` DROP DEFAULT;
ALTER TABLE `division` MODIFY COLUMN `pinned` JSON NOT NULL;
