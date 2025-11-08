from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "users_points" (
    "id" UUID NOT NULL PRIMARY KEY,
    "created" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "last_updated" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "created_by" UUID,
    "last_update_by" UUID,
    "points" INT NOT NULL DEFAULT 0,
    "action_type" VARCHAR(100) NOT NULL,
    "c02_emission" DOUBLE PRECISION,
    "user_id_id" UUID NOT NULL REFERENCES "users" ("id") ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS "idx_users_point_created_4ce168" ON "users_points" ("created_by");
CREATE INDEX IF NOT EXISTS "idx_users_point_last_up_06c9e5" ON "users_points" ("last_update_by");
CREATE INDEX IF NOT EXISTS "idx_users_point_user_id_06c633" ON "users_points" ("user_id_id");
CREATE INDEX IF NOT EXISTS "idx_users_point_action__1adc61" ON "users_points" ("action_type");
        ALTER TABLE "basemodel" ADD "created" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP;
        ALTER TABLE "basemodel" ADD "created_by" UUID;
        ALTER TABLE "basemodel" ADD "last_update_by" UUID;
        ALTER TABLE "basemodel" DROP COLUMN "id_tenant";
        ALTER TABLE "basemodel" DROP COLUMN "created_at";
        ALTER TABLE "basemodel" DROP COLUMN "active";
        ALTER TABLE "basemodel" ALTER COLUMN "last_updated" TYPE TIMESTAMPTZ USING "last_updated"::TIMESTAMPTZ;
        ALTER TABLE "users" ALTER COLUMN "balance" TYPE INT USING "balance"::INT;
        CREATE INDEX IF NOT EXISTS "idx_basemodel_created_8dd2d9" ON "basemodel" ("created_by");
        CREATE INDEX IF NOT EXISTS "idx_basemodel_last_up_e02b71" ON "basemodel" ("last_update_by");"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP INDEX IF EXISTS "idx_basemodel_last_up_e02b71";
        DROP INDEX IF EXISTS "idx_basemodel_created_8dd2d9";
        ALTER TABLE "users" ALTER COLUMN "balance" TYPE VARCHAR(128) USING "balance"::VARCHAR(128);
        ALTER TABLE "basemodel" ADD "id_tenant" UUID NOT NULL;
        ALTER TABLE "basemodel" ADD "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP;
        ALTER TABLE "basemodel" ADD "active" BOOL NOT NULL DEFAULT True;
        ALTER TABLE "basemodel" DROP COLUMN "created";
        ALTER TABLE "basemodel" DROP COLUMN "created_by";
        ALTER TABLE "basemodel" DROP COLUMN "last_update_by";
        ALTER TABLE "basemodel" ALTER COLUMN "last_updated" TYPE TIMESTAMPTZ USING "last_updated"::TIMESTAMPTZ;
        DROP TABLE IF EXISTS "users_points";"""


MODELS_STATE = (
    "eJztm21v4jgQgP8KyqdW6lUtpWy1Oq0ElGq5baGisHfaqopMYqjVxMnGTrtoxX8/23l3Qk"
    "oodEPJFwTjmcR+xi8zI/NbMS0dGuS4BR2kPSqfa78VDEzIvkgtRzUF2HYk5wIKJoZQBZHO"
    "hFAHaJRJp8AgkIl0SDQH2RRZmEmxaxhcaGlMEeFZJHIx+ulClVozSB+hwxruH5gYYR3+gi"
    "T4aT+pUwQNPdFVpPN3C7lK57aQ9TC9Eor8bRNVswzXxJGyPaePFg61EaZcOoMYOoBC/njq"
    "uLz7vHf+OIMReT2NVLwuxmx0OAWuQWPDXZGBZmHOj/WGiAHO+Fv+qp82PjUuzpqNC6Yieh"
    "JKPi284UVj9wwFgf5IWYh2QIGnITBG3J6hQ3iXUvA6j8DJphczkRCyjssIA2B5DANBBDGa"
    "OBuiaIJfqgHxjPIJXj8/z2H2vTXsfG0ND5jWoYAXweLTvwAoX303IZ2enKwAiWnJkNhTKf"
    "TWUhLUP3eDfjaomIkEa4zZIO51pNGjmoEIfSgnuhxSfNS80yYhPw0u6Afsblr/HfIWi+2W"
    "3iba71wP2oKCRejMEU8RD2gzxnzrmz7FFjEXTID29AIcXU21WHVrmW66yaybsgRgMBOs+I"
    "j5+PzDoA0IvOFfs06KqDH3sJgwNTNUK815MR73LgscGK6L9GNus86cfP3cUP6euljjDGri"
    "Tfyj8UXZyiQV8/GseSjPPTG6/ANEc6AYdormJRNTZMIlSz4yk7Dqvt1x8KWcS15hA9AH2J"
    "j7vsuhO+rddO9GrZvbxD5w2Rp1eUtdSOeS9KAp7Q3hQ2r/9kZfa/xn7ceg35VdFuqNfii8"
    "T8ClloqtFxXosWkWSAMwiR3cAISqrq2v41fZtnLuH3Wu3/nUclUn8yL7X9LqDfug38McV2"
    "44fn7Lppe5IgqSS1vuB72SRCsjiEGwpqVYJWjKjVRoTKmKU3Y5TkHsWcKZxXjGjDaJdZUj"
    "rFRg0ycIyCC5UsznW1aRQbkigyrq+zC+TYf07NxCzzDt1rZlGRDgJfWr0Ejy54RZbcuF4f"
    "my6S2uPRhcJ7zV7o2k8sv4pt0dHpwKNzElRL0ysl9EjdHUdeYaUqgWGJmsVQ98PfTbbjnw"
    "/LS+QjmQaaVqpt7AGQrL0ddBFrPcSXJnq4A7S3HTEbENMFfF7wLUZLudZFY/b65UoW+mi8"
    "96IVqB/k5SajZWgNRsHJYnHRsT6GQmY17DUV4q5oYqVSJWJWJVIlYlYh8jWK8SsY/r2yoR"
    "qxKxDQd9VSJWJWI7kIjxaL0osbjNRmht/XLeJuYXNAEyimAKDXaQUYGUNc7IBoS8sM2nCK"
    "a4zU6uvdP6xSo38OoXMq0pclgUWHT1Ja32i5gIm4sCSxjtFy/bQSZw5ip7Mia25WRkoDkL"
    "M8t4v/hNgAGwljHbll5Zj1m8fm+9HKg2cnM9YkZc5xnOGRLTNmBmapybQ2WZv2M2VbRS+W"
    "7pVIHKcGz9W7xjqgO17Fyi7dtffRtCA9DsfwvES7+34oHlrEYsgqkUSP3ltNh6pdynsqxe"
    "HkF7pWqu2pHmNovn9+J1KtIV1nAvyhaBvx+qwnp1E7uqFlY3sffVudVN7DdsetVN7M3Qi+"
    "KAFdOOyGCtrGOtDePkDbvFhnOOeASTgpZTME+a7dsfQE/qKjQRyf5f8ZVhgSWTTTaUuE25"
    "ZSlT3RxOl4Nx+7pbux12O727nv9X0PAUEo3JrGzYbV1n1NJZUK0Wi5STVu99Z+JP7XapdD"
    "aFMWNKWg5EM/wNzgXJHuvKklqLfFuptORSySoTO+AlTL+k2cGGyAYGvRnYad11WpddZfGe"
    "d8QW/wPFJ38N"
)
