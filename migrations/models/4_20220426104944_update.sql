-- upgrade --
ALTER TABLE `user`
    DROP COLUMN `nickname`;
ALTER TABLE `user`
    DROP COLUMN `config`;
-- downgrade --
ALTER TABLE `user`
    ADD `nickname` VARCHAR(16) NOT NULL DEFAULT '';
ALTER TABLE `user`
    ADD `config` JSON NOT NULL;
