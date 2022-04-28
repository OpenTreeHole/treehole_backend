-- upgrade --
ALTER TABLE `floor`
    ADD `dislike_data` JSON NOT NULL;
update floor
set dislike_data = '[]'
where id > 0;
-- downgrade --
ALTER TABLE `floor`
    DROP COLUMN `dislike_data`;
