# Repository Baseline

Captured on 2026-10-03 before feature implementation.

## Git state

| Item | Recorded value |
| --- | --- |
| Current local branch | `productions-a2` |
| Parent integration branch | `New-module-development` |
| Baseline commit | `8bcfd30a2292f8fb4626eb33cbd6fbc21e9b8f71` (`skeleton construction`) |
| Remote push target | `Dloperity/tinshed-players` only after user approval |
| Upstream repository | `ThirstyCoco/tinshed-players` - read-only; no changes permitted |

## Preservation rule

The files present at the baseline are not to be deleted or edited during the current feature work. New functionality is implemented only by adding routes, templates, tests, and documentation. Any future need to edit a baseline file must be identified to the user and approved before the edit occurs.

## File checksums

SHA-256 values below identify the initial content of every file present at capture time, excluding `.git`, virtual environments, and Python cache files.

| Path | SHA-256 |
| --- | --- |
| `.env.example` | `E2A8E890851802EDC9F87B2731B355D1E6EE1FFC067436A406205DE64979B628` |
| `.github/workflows/ci.yml` | `3A543FC768B56F8D3FC9E31FC59B71A36D61EEF7B24FE22D105DF7AE3BDB4B43` |
| `.gitignore` | `4184CA120D7F097246EDB0AB00035006FBA11B524A6F0DFF50AEDBEFCC1E7AB1` |
| `app/__init__.py` | `77027FCB20A0CD0768879EDE43BBDB5E7C28510EDB30F0368753939A42B4AA60` |
| `app/assignments/__init__.py` | `E3B0C44298FC1C149AFBF4C8996FB92427AE41E4649B934CA495991B7852B855` |
| `app/assignments/routes.py` | `2512B9FEFEE8F9FF6567FEF61B4564106C15362FA666391CE4736BAD7A3F38CA` |
| `app/models.py` | `424BD176257B3C135B6A9E6EEEFAF778A59D615007662DCB12F527B1DBBB16CD` |
| `app/productions/__init__.py` | `E3B0C44298FC1C149AFBF4C8996FB92427AE41E4649B934CA495991B7852B855` |
| `app/productions/routes.py` | `ADAAD93A4FCE7F442B317A363EC94FE9B0B98CBD128EDB2BB745D0950F9E6312` |
| `app/templates/assignments/form.html` | `BB217E6933B68D68A470470E4BC9D1C78CB099D1969278754BE91DD79A28AF09` |
| `app/templates/assignments/list.html` | `5F7E3C29C0098F65C92B1C66977FB91A8DB1C343114769B3A9B9B77F99E210E8` |
| `app/templates/base.html` | `7DFF7EFB2E86EC8B1FE63A18D4D7C5CB50DF35FAC3CBEA5C3DC51BB6CD9FD12E` |
| `app/templates/index.html` | `63CC04ADB31BECCB619AEE50DEF53EEDABC5D6CA1E40160541793DF0E4D910` |
| `app/templates/productions/detail.html` | `7D6926A1427FFD030712CC520DAC64CEE9D018C52E92D8BF2BF9ABE019572714` |
| `app/templates/productions/form.html` | `9D0CB729412E26C7996B7F98B7D8E9487433A5F3A707B09E4F3572320BC0C4CB` |
| `app/templates/productions/list.html` | `0C29B71E73AD7A97D7FA481ECFB9812197F52161571337380BF37B6FE6FEF927` |
| `app/templates/productions/performance_form.html` | `77E434A32D9D71DFE0DA76E987A4D9407F28004C3F8D4DC0C61B18FF99B1E5F7` |
| `app/templates/volunteers/form.html` | `53E455174A54842D5E526173F2C2A609A76CC748AE4EF15310B7B9A0E099216B` |
| `app/templates/volunteers/list.html` | `12C8FAAFD86F1FCA9E0A27CD134D4D8543B08B736A7D70CE168C59C579984DB9` |
| `app/volunteers/__init__.py` | `E3B0C44298FC1C149AFBF4C8996FB92427AE41E4649B934CA495991B7852B855` |
| `app/volunteers/routes.py` | `262A66BAA4397DFAAEEA1CCA4E951760B883F7981C32355C8E974BE3BDFA7518` |
| `docs/evidence/.gitignore` | `8FCC7636115F18ECECFC57CABD8C6F770BBB2E75BCBC824545D6B0DF6CCCC112` |
| `docs/evidence/README.md` | `9DE9FB13C73B5E08AE4B270786C700587560839C9A60770B28FDC3030C4094C9` |
| `README.md` | `D8A9CB9BEF3F2F7D1140CFED91584ECCAF4DF26A32973114834309C89D7C4C8C` |
| `render.yaml` | `971C0E6E33BAA2CDE424F94DFE05769A33C30EDFBEE93D4770063539730324CE` |
| `requirements.txt` | `EFF941C0D9C540A4B90E8C94A4CA724737E61B8E0AD8ACF41EFDB6C0C364E266` |
| `run.py` | `F748F4F70F58B60E0E2090E0A60DAF1ADC342FEEF9984AD834D04B8C8CE8C09E` |
| `tests/conftest.py` | `69D5D2B7B0BC23061752100F78E76C578EC41622B3A67B0501EBD848D63A0E4D` |
| `tests/test_assignments.py` | `034EC0BFA08600808D6433AB8B57E2C83455C95EF24746EBD81BBED61BD9D305` |
| `tests/test_productions.py` | `E972BF684388869C058B763EFA2BE072C2667812F958EBEE61496A2D05353515` |
| `tests/test_volunteers.py` | `99AAD421CB8085A2E410D3D8077E1CD85B938BE1E2C76156BDAF7A36F48CE4DA` |
