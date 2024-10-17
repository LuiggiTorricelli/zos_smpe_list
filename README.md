# Ansible z/OS SMP/E LIST role

The Ansible role `zos_smpe_list` will perform a sequence of steps to execute the SMP/E LIST command and return a formatted output, based on the SMP/E CSI data set, SMP/E LIST options, zone name and zone type informed by the user on the specified z/OS hosts.

## Requirements

Python and Z Open Automation Utilities must be installed on the remote z/OS system, since the modules `zos_find` and `zos_mvs_raw` from the collection `ibm.ibm_zos_core` are used along the role.

## Role Variables

This role has multiple variables. The descriptions and defaults for all these variables can be found in the **[`defaults/main.yml`](/defaults/main.yml)** file and **[`meta/argument_specs.yml`](/meta/argument_specs.yml)**:

| Variable | Description | Optional? |
| -------- | ----------- | :-------: |
| **[`show_output`](/defaults/main.yml)** | Display the parsed content at the end | Yes<br>(default: `true`) |
| **[`smpe_csi`](/meta/argument_specs.yml)** | SMP/E CSI data set name to be listed | No |
| **[`smpe_options`](/defaults/main.yml)** | Options to consider on the LIST statement | Yes<br>(default: `[]`) |
| **[`smpe_zone`](/meta/argument_specs.yml)** | SMP/E zone name | No |
| **[`smpe_zone_type`](/meta/argument_specs.yml)** | SMP/E zone type of the informed SMP/E zone (`DLIB`, `GLOBAL` or `TARGET`) | No |

## Dependencies

None.

## Example Playbook

    - hosts: zos_server
      roles:
        - role: zos_smpe_list
          smpe_zone: RSU2409
          smpe_zone_type: TARGET
          smpe_options:
            - TARGETZONE
            - DDDEF       
          smpe_csi: SMPE.GLOBAL.CSI
          show_output: true

## Sample Output

When this role is successfully executed, a fact named `zos_smpe_list_result` will be set. It is a dictionary, containing all entry types and subentries found on the specified zone, based on the informed variables and resulting SMP/E LIST output that was parsed:

    "zos_smpe_list_result": "zos_smpe_list_result": {
        "RSU2409": {
            "DDDEF": {
                "SMPLTS": {
                    "DATASET": "SMPE.SMPLTS",
                    "DISPOSITION_INIT": "SHR"
                },
                "SMPMTS": {
                    "DATASET": "SMPE.SMPMTS",
                    "DISPOSITION_INIT": "SHR"
                },
                "SMPOUT": {
                    "SYSOUT": "*"
                },
                "SMPPTS": {
                    "DATASET": "SMPE.SMPPTS",
                    "DISPOSITION_INIT": "SHR"
                },
                "SMPWRK1": {
                    "DIR": "500",
                    "DISPOSITION_FINAL": "DELETE",
                    "DISPOSITION_INIT": "NEW",
                    "SPACE": "(500 ,100 )",
                    "SPACE_UNIT": "CYL",
                    "UNIT": "SYSDA"
                },
                "SYSUT1": {
                    "DISPOSITION_FINAL": "DELETE",
                    "DISPOSITION_INIT": "NEW",
                    "SPACE": "(500 ,99  )",
                    "SPACE_UNIT": "CYL",
                    "UNIT": "SYSDA"
                }
            },
            "ZONE": {
                "RSU2409": {
                    "OPTIONS": "BUILD",
                    "RELATED": "SMPDLIB",
                    "SREL": [
                        "Z038"
                    ],
                    "TZONE": "RSU2409",
                    "UPGLEVEL": "SMP/E 37.12"
                }
            }
        }
    }

## License

This role is licensed under licensed under [Apache License, Version 2.0](http://www.apache.org/licenses/LICENSE-2.0).

## Author Information

This role was created in 2024 by Luiggi Torricelli.
