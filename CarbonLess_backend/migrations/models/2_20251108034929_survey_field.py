from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "users" ADD "survey_completed" BOOL NOT NULL DEFAULT False;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "users" DROP COLUMN "survey_completed";"""


MODELS_STATE = (
    "eJztmm1P2zAQgP9KlU9DYghC6dA0TWqBaZ3WdoJ2mzahyI3dYuHYme0AFeK/z3aa14asQW"
    "W0NF+q9Hzn+J7zy52Ve8tjEBGx10Ycu1fW+8a9RYGH1EOuZbdhAd9P5FogwZgYVZDojIXk"
    "wJVKOgFEICWCSLgc+xIzqqQ0IEQLmasUMZ0mooDiPwFyJJsieYW4avh9qcSYQnSHRPTXv3"
    "YmGBGYGSqG+t1G7siZb2RdKj8ZRf22seMyEng0UfZn8orRWBtTqaVTRBEHEunuJQ/08PXo"
    "5n5GHoUjTVTCIaZsIJqAgMiUu0sycBnV/NRohHFwqt/y1j5ovmseH7aax0rFjCSWvHsI3U"
    "t8Dw0Ngf7QejDtQIJQw2BMuN0gLvSQFuCdXAFeTC9lkkOoBp5HGAErYxgJEojJxFkRRQ/c"
    "OQTRqdQT3D46KmH2vX1+8rl9/kZp7Rh4CSw9/SuAmqtvJqSD/f0lICmtPCTVq0ThWsqC+n"
    "Ix6BeDSpnkYI2ocuI3xK7cbRAs5OV6oishpb3Wg/aE+EO0oB+x67V/7ugWpnbLcBPtn3wd"
    "dAwFJuSUm15MBx3FWG99k+vUItaCMXCvbwGHzkILs9ljuotNnu3lJYCCqWGlPdb+zQ+DDh"
    "Copx+LToqksfSwGCs1L1Zbm/NiNOqeVjgwggDDPW3zlDn573PD+jAJqKsZNMyb9E/zo/Us"
    "k9TMx8PWTn7uGe/KDxCs+kIUFC34Mp4po1ViXWaprxXY1L7JkXbUAQUkT1WLxB56ZPvMWO"
    "ZwwrnpXvSwnjuopXyAA0pm86VQwnTY7Z1dDNu9b5lt9bQ9PNMttpHOctI3rdxWG3fS+NEd"
    "fm7ov41fg/5ZPlCx3vCXpccEAskcym4dAFOrNpImg0/iSoCQTuBDg7tiZPO2dWxfNLYGTD"
    "YjVPvIDVoMa4cxggB9JC+MjXLxHCur5wphfL6seovrDAZfM9HqdIe5tGbU65ypXNGESSlh"
    "GZZnpjhZk7RmaI4jUZTURE2lKY1MKdUJTZ3Q1AlNndC8jkOvTmheb2zrhGb1CU2GJoQqNK"
    "LSpWFi8qSLwzmWF7s3PDqwl7g3VFoLl6uh4woF4/ApyFKWG0nucBlwhwvcIBY+ATPH/K9A"
    "LW+3kczso9ZSV/mtxVtqWIlWpL+RlFrNJSC1mjvrU46NBOKFxVjYsFtWigWxSl2I1YVYXY"
    "jVhdjrSNbrQuz1xrYuxOpCbMVJX12I1YXYBhRiOluvSixtsxJaz/4V3yrmF/IAJlUwxQYb"
    "yKhCyZpm5AMhbtXmUwVT2mYj196BfbzMp3r2cZ7WBHOVBVZdfVmr7SJm0uaqwDJG28XL59"
    "gDfOaonqnwGS+oQEsWZpHxdvEbAwKoW2m2pUy2i5UI+A2aKRKeT1BhSVxaOxWZ/8cqquoN"
    "5XZ8oPPwFz50Ve0="
)
