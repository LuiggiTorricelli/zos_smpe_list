from __future__ import absolute_import, division, print_function
from ansible.errors import AnsibleFilterTypeError

__metaclass__ = type
import re

class FilterModule(object):
    def filters(self):
        filters = {
            "parse_gimsmp": self.parse_gimsmp,
        }
        return filters
    
    def parse_entries_assembler(self, content):
        input_content = re.sub(r"\n+", r"\n", content)
        entries = re.findall(r"(^\S+ +[\s\S]+?)(?=^\S+|\n$)", input_content, flags=re.MULTILINE)
        tmp_content = {}
        for entry in entries:
            entry_name = re.findall(r"^([\S-]+)", entry)[0]
            entry_content = entry + "\n\n"
            entry_content = re.findall(r"^.{10}([\w /\(\)]+?)(?:\s+=\s+([\S\s]+?))?(?=\n\s{10}\w|\n{2})", entry_content, flags=re.MULTILINE)
            tmp_content[entry_name] = {}
            for opt in entry_content:
                key = opt[0]
                value = opt[1]
                
                if key not in tmp_content[entry_name]:
                    tmp_content[entry_name][key] = value

        return tmp_content

    def parse_entries_data(self, content):
        input_content = re.sub(r"\n+", r"\n", content)
        entries = re.findall(r"(^\S+ +[\s\S]+?)(?=^\S+|\n$)", input_content, flags=re.MULTILINE)
        tmp_content = {}
        for entry in entries:
            entry_name = re.findall(r"^([\S-]+)", entry)[0]
            entry_content = entry + "\n\n"
            entry_content = re.findall(r"^.{10}([\w /\(\)]+?)(?:\s+=\s+([\S\s]+?))?(?=\n\s{10}\w|\n{2})", entry_content, flags=re.MULTILINE)
            tmp_content[entry_name] = {}
            for opt in entry_content:
                key = opt[0]
                value = opt[1]
                if key in ["ALIAS"]:
                    value = re.sub(r"[ \n]+", "<sep>", value).split('<sep>')
                    value = [x for x in value if x]
                if key not in tmp_content[entry_name]:
                    tmp_content[entry_name][key] = value

        return tmp_content

    def parse_entries_dddef(self, content):
        input_content = re.sub(r"\n+", r"\n", content)
        entries = re.findall(r"(^\S+ +[\s\S]+?)(?=^\S+|\n$)", input_content, flags=re.MULTILINE)
        tmp_content = {}
        for entry in entries:
            entry_name = re.findall(r"^([\S-]+)", entry)[0]
            entry_content = entry + "\n\n"
            entry_content = re.findall(r"^.{10}([\w /\(\)]+?)(?:\s+=\s+([\S\s]+?))?(?=\n\s{10}\w|\n{2})", entry_content, flags=re.MULTILINE)
            tmp_content[entry_name] = {}
            for opt in entry_content:
                key = opt[0]
                value = opt[1]
                if key in ['CYL', 'TRK'] or key.find('BLK(') == 0:
                    value = key
                    key = "SPACE_UNIT"
                elif key in ['CATALOG', 'DELETE', 'KEEP']:
                    value = key
                    key = "DISPOSITION_FINAL"
                elif key in ['MOD', 'NEW', 'OLD', 'SHR']:
                    value = key
                    key = "DISPOSITION_INIT"
                elif key in ["WAIT", "WAITFORDSN"]:
                    value = "YES"
                    key = "WAIT"
                elif key in ["PROTECT"]:
                    value = "YES"
                    key = "PROTECT"
                elif key in ["CONCAT"]:
                    value = re.sub(r"[ \n]+", "<sep>", value).split('<sep>')
                    value = [x for x in value if x]

                if key not in tmp_content[entry_name]:
                    tmp_content[entry_name][key] = value

        return tmp_content

    def parse_entries_dlib(self, content):
        input_content = re.sub(r"\n+", r"\n", content)
        entries = re.findall(r"(^\S+ +[\s\S]+?)(?=^\S+|\n$)", input_content, flags=re.MULTILINE)
        tmp_content = {}
        for entry in entries:
            entry_name = re.findall(r"^([\S-]+)", entry)[0]
            entry_content = entry + "\n\n"
            entry_content = re.findall(r"^.{10}([\w /\(\)]+?)(?:\s+=\s+([\S\s]+?))?(?=\n\s{10}\w|\n{2})", entry_content, flags=re.MULTILINE)
            tmp_content[entry_name] = {}
            for opt in entry_content:
                key = opt[0]
                value = opt[1]
                if key in ["SYSTEM LIBRARY"]:
                    value = re.sub(r"[ \n]+", "<sep>", value).split('<sep>')
                    value = [x for x in value if x]

                if key not in tmp_content[entry_name]:
                    tmp_content[entry_name][key] = value

        return tmp_content

    def parse_entries_feature(self, content):
        input_content = re.sub(r"\n+", r"\n", content)
        entries = re.findall(r"(^\S+ +[\s\S]+?)(?=^\S+|\n$)", input_content, flags=re.MULTILINE)
        tmp_content = {}
        for entry in entries:
            entry_name = re.findall(r"^([\S-]+)", entry)[0]
            entry_content = entry + "\n\n"
            entry_content = re.findall(r"^.{10}([\w /\(\)]+?)(?:\s+=\s+([\S\s]+?))?(?=\n\s{10}\w|\n{2})", entry_content, flags=re.MULTILINE)
            tmp_content[entry_name] = {}
            for opt in entry_content:
                key = opt[0]
                value = opt[1]
                if key in ["FMID"]:
                    value = re.sub(r"[ \n]+", "<sep>", value).split('<sep>')
                    value = [x for x in value if x]
                elif key in ["PRODUCT"]:
                    prod = re.findall(r"(\S+)\s+(\S+)", re.sub(r"\n+", " ", value))
                    if len(prod) > 0:
                        value = {"ID": prod[0][0], "VRM": prod[0][1]}
                elif key in ["DATE/TIME REC"]:
                    ucl = re.findall(r".+\n +UCL += +(.+)", value)
                    if len(ucl) > 0:
                        value = re.sub(r"(.+)\n[\s\S]+", r"\1", value)
                        tmp_content[entry_name]["DATE/TIME UCL"] = ucl[0]

                if key not in tmp_content[entry_name]:
                    tmp_content[entry_name][key] = value

        return tmp_content

    def parse_entries_fmidset(self, content):
        input_content = re.sub(r"\n+", r"\n", content)
        entries = re.findall(r"(^\S+ +[\s\S]+?)(?=^\S+|\n$)", input_content, flags=re.MULTILINE)
        tmp_content = {}
        for entry in entries:
            entry_name = re.findall(r"^([\S-]+)", entry)[0]
            entry_content = entry + "\n\n"
            entry_content = re.findall(r"^.{10}([\w /\(\)]+?)(?:\s+=\s+([\S\s]+?))?(?=\n\s{10}\w|\n{2})", entry_content, flags=re.MULTILINE)
            tmp_content[entry_name] = {}
            for opt in entry_content:
                key = opt[0]
                value = opt[1]
                if key in ["FMID"]:
                    value = re.sub(r"[ \n]+", "<sep>", value).split('<sep>')
                    value = [x for x in value if x]
            
                if key not in tmp_content[entry_name]:
                    tmp_content[entry_name][key] = value

        return tmp_content

    def parse_entries_hfs(self, content):
        input_content = re.sub(r"\n+", r"\n", content)
        entries = re.findall(r"(^\S+ +[\s\S]+?)(?=^\S+|\n$)", input_content, flags=re.MULTILINE)
        tmp_content = {}
        for entry in entries:
            entry_name = re.findall(r"^([\S-]+)", entry)[0]
            entry_content = entry + "\n\n"
            entry_content = re.findall(r"^.{10}([\w /\(\)]+?)(?:\s+=\s+([\S\s]+?))?(?=\n\s{10}\w|\n{2})", entry_content, flags=re.MULTILINE)
            tmp_content[entry_name] = {}
            for opt in entry_content:
                key = opt[0]
                value = opt[1]
                if key in ["LINK", "SYMLINK", "SYMPATH"]:
                    value = re.sub(r"[ \n]+", "<sep>", value).split('<sep>')
                    value = [x for x in value if x]
                elif key in ["BINARY", "TEXT"]:
                    value = key
                    key = "INSTALLATION_MODE"

                if key not in tmp_content[entry_name]:
                    tmp_content[entry_name][key] = value

        return tmp_content

    def parse_entries_holddata(self, content):
        input_content = re.sub(r"\n+", r"\n", content)
        entries = re.findall(r"(^\S+ +[\s\S]+?)(?=^\S+|\n$)", input_content, flags=re.MULTILINE)
        tmp_content = {}
        for entry in entries:
            entry_name = re.findall(r"^([\S-]+)", entry)[0]
            entry_content = entry + "\n\n"
            entry_content = re.findall(r"^.{10}([\w /\(\)]+?)(?:\s+=\s+([\S\s]+?))?(?=\n\s{10}\w|\n{2})", entry_content, flags=re.MULTILINE)
            tmp_content[entry_name] = {}
            for opt in entry_content:
                key = opt[0]
                value = opt[1]
                if key not in tmp_content[entry_name]:
                    tmp_content[entry_name][key] = {}
                hold_reason, hold_content = re.findall(r"^(\w+) +([\s\S]+)", value)[0]
                if hold_reason not in tmp_content[entry_name][key]:
                    tmp_content[entry_name][key][hold_reason] = []
                tmp_content[entry_name][key][hold_reason].append(hold_content)

        return tmp_content

    def parse_entries_jar(self, content):
        input_content = re.sub(r"\n+", r"\n", content)
        entries = re.findall(r"(^\S+ +[\s\S]+?)(?=^\S+|\n$)", input_content, flags=re.MULTILINE)
        tmp_content = {}
        for entry in entries:
            entry_name = re.findall(r"^([\S-]+)", entry)[0]
            entry_content = entry + "\n\n"
            entry_content = re.findall(r"^.{10}([\w /\(\)]+?)(?:\s+=\s+([\S\s]+?))?(?=\n\s{10}\w|\n{2})", entry_content, flags=re.MULTILINE)
            tmp_content[entry_name] = {}
            for opt in entry_content:
                key = opt[0]
                value = opt[1]
                if key in ["LINK", "SYMLINK", "SYMPATH", "UMID"]:
                    value = re.sub(r"[ \n]+", "<sep>", value).split('<sep>')
                    value = [x for x in value if x]

                if key not in tmp_content[entry_name]:
                    tmp_content[entry_name][key] = value

        return tmp_content

    def parse_entries_lmod(self, content):
        input_content = re.sub(r"\n+", r"\n", content)
        entries = re.findall(r"(^\S+ +[\s\S]+?)(?=^\S+|\n$)", input_content, flags=re.MULTILINE)
        tmp_content = {}
        for entry in entries:
            entry_name = re.findall(r"^([\S-]+)", entry)[0]
            entry_content = entry + "\n\n"
            entry_content = re.findall(r"^.{10}([\w /\(\)]+?)(?:\s+=\s+([\S\s]+?))?(?=\n\s{10}\w|\n{2})", entry_content, flags=re.MULTILINE)
            tmp_content[entry_name] = {}
            for opt in entry_content:
                key = opt[0]
                value = opt[1]
                if key in ["CALLLIBS", "MODDEL", "SYSTEM LIBRARY"]:
                    value = re.sub(r"[ \n]+", "<sep>", value).split('<sep>')
                    value = [x for x in value if x]
                elif key in ["XZMODP", "COPY"]:
                    value = "YES"

                if key not in tmp_content[entry_name]:
                    tmp_content[entry_name][key] = value

        return tmp_content

    def parse_entries_mac(self, content):
        input_content = re.sub(r"\n+", r"\n", content)
        entries = re.findall(r"(^\S+ +[\s\S]+?)(?=^\S+|\n$)", input_content, flags=re.MULTILINE)
        tmp_content = {}
        for entry in entries:
            entry_name = re.findall(r"^([\S-]+)", entry)[0]
            entry_content = entry + "\n\n"
            entry_content = re.findall(r"^.{10}([\w /\(\)]+?)(?:\s+=\s+([\S\s]+?))?(?=\n\s{10}\w|\n{2})", entry_content, flags=re.MULTILINE)
            tmp_content[entry_name] = {}
            for opt in entry_content:
                key = opt[0]
                value = opt[1]
                if key in ["GENASM", "MALIAS", "UMID"]:
                    value = re.sub(r"[ \n]+", "<sep>", value).split('<sep>')
                    value = [x for x in value if x]
                if key not in tmp_content[entry_name]:
                    tmp_content[entry_name][key] = value
        return tmp_content

    def parse_entries_mod(self, content):
        input_content = re.sub(r"\n+", r"\n", content)
        entries = re.findall(r"(^\S+ +[\s\S]+?)(?=^\S+|\n$)", input_content, flags=re.MULTILINE)
        tmp_content = {}
        for entry in entries:
            entry_name = re.findall(r"^([\S-]+)", entry)[0]
            entry_content = entry + "\n\n"
            entry_content = re.findall(r"^.{10}([\w /\(\)]+?)(?:\s+=\s+([\S\s]+?))?(?=\n\s{10}\w|\n{2})", entry_content, flags=re.MULTILINE)
            tmp_content[entry_name] = {}
            for opt in entry_content:
                key = opt[0]
                value = opt[1]
                if key in ["LMOD", "TALIAS", "UMID"]:
                    value = re.sub(r"[ \n]+", "<sep>", value).split('<sep>')
                    value = [x for x in value if x]
                elif key in ["RMID"]:
                    if re.search(r"RMIDASM", value):
                        tmp_content[entry_name]["RMIDASM"] = "YES"
                elif key in ["RMIDASM", "XZLMODP"]:
                    value = "YES"
                if key not in tmp_content[entry_name]:
                    tmp_content[entry_name][key] = value
        return tmp_content

    def parse_entries_options(self, content):
        input_content = re.sub(r"\n+", r"\n", content)
        entries = re.findall(r"(^\S+ +[\s\S]+?)(?=^\S+|\n$)", input_content, flags=re.MULTILINE)
        tmp_content = {}
        for entry in entries:
            entry_name = re.findall(r"^([\S-]+)", entry)[0]
            entry_content = entry + "\n\n"
            entry_content = re.findall(r"^.{10}([\w /\(\)]+?)(?:\s+=\s+([\S\s]+?))?(?=\n\s{10}\w|\n{2})", entry_content, flags=re.MULTILINE)
            tmp_content[entry_name] = {}
            for opt in entry_content:
                key = opt[0]
                value = opt[1]
                if key in ["EXRTYDD", "FIXCAT", "RECEXZGRP", "RECZGRP", "RETRYDDN", "SUPPHOLD"]:
                    value = re.sub(r"[ \n]+", "<sep>", value).split('<sep>')
                    value = [x for x in value if x]
                elif key in ["NOPURGE", "NOREJECT", "SAVEMTS", "SAVESTS"]:
                    value = "YES"

                if key not in tmp_content[entry_name]:
                    tmp_content[entry_name][key] = value

        return tmp_content

    def parse_entries_order(self, content):
        input_content = re.sub(r"\n+", r"\n", content)
        entries = re.findall(r"(^\S+ +[\s\S]+?)(?=^\S+|\n$)", input_content, flags=re.MULTILINE)
        tmp_content = {}
        for entry in entries:
            entry_name = re.findall(r"^([\S-]+)", entry)[0]
            entry_content = entry + "\n\n"
            entry_content = re.findall(r"^.{10}([\w /\(\)]+?)(?:\s+=\s+([\S\s]+?))?(?=\n\s{10}\w|\n{2})", entry_content, flags=re.MULTILINE)
            tmp_content[entry_name] = {}
            for opt in entry_content:
                key = opt[0]
                value = opt[1]
                if key in ["APARS", "PTFS", "ZONES"]:
                    value = re.sub(r"[ \n]+", "<sep>", value).split('<sep>')
                    value = [x for x in value if x]
                    
                if key not in tmp_content[entry_name]:
                    tmp_content[entry_name][key] = value

        return tmp_content

    def parse_entries_product(self, content):
        input_content = re.sub(r"\n+", r"\n", content)
        entries = re.findall(r"(^\S+ +[\s\S]+?)(?=^\S+|\n$)", input_content, flags=re.MULTILINE)
        tmp_content = {}
        for entry in entries:
            entry_name = re.findall(r"^([\S-]+)", entry)[0]
            entry_content = entry + "\n\n"
            entry_content = re.findall(r"^.{10}([\w /\(\)]+?)(?:\s+=\s+([\S\s]+?))?(?=\n\s{10}\w|\n{2})", entry_content, flags=re.MULTILINE)
            if entry_name not in tmp_content:
                tmp_content[entry_name] = []
            tmp_obj = {}
            for opt in entry_content:
                key = opt[0]
                value = opt[1]
                if key in ["SREL"]:
                    value = re.sub(r"[ \n]+", "<sep>", value).split('<sep>')
                    value = [x for x in value if x]
                elif key in ["PRODSUP"]:
                    prodsups = re.findall(r"(\S+)\s+(\S+)", re.sub(r"\n+", " ", value))
                    value = list(map(lambda x: {"PRODUCT": x[0], "VRM": x[1]}, prodsups))
                elif key in ["DATE/TIME REC"]:
                    ucl = re.findall(r".+\n +UCL += +(.+)", value)
                    if len(ucl) > 0:
                        value = re.sub(r"(.+)\n[\s\S]+", r"\1", value)
                        tmp_obj["DATE/TIME UCL"] = ucl[0]

                if key not in tmp_obj:
                    tmp_obj[key] = value
            tmp_content[entry_name].append(tmp_obj)
        return tmp_content

    def parse_entries_program(self, content):
        input_content = re.sub(r"\n+", r"\n", content)
        entries = re.findall(r"(^\S+ +[\s\S]+?)(?=^\S+|\n$)", input_content, flags=re.MULTILINE)
        tmp_content = {}
        for entry in entries:
            entry_name = re.findall(r"^([\S-]+)", entry)[0]
            entry_content = entry + "\n\n"
            entry_content = re.findall(r"^.{10}([\w /\(\)]+?)(?:\s+=\s+([\S\s]+?))?(?=\n\s{10}\w|\n{2})", entry_content, flags=re.MULTILINE)
            tmp_content[entry_name] = {}
            for opt in entry_content:
                key = opt[0]
                value = opt[1]

                if key not in tmp_content[entry_name]:
                    tmp_content[entry_name][key] = value

        return tmp_content

    def parse_entries_source(self, content):
        input_content = re.sub(r"\n+", r"\n", content)
        entries = re.findall(r"(^\S+ +[\s\S]+?)(?=^\S+|\n$)", input_content, flags=re.MULTILINE)
        tmp_content = {}
        for entry in entries:
            entry_name = re.findall(r"^([\S-]+)", entry)[0]
            entry_content = entry + "\n\n"
            entry_content = re.findall(r"^.{10}([\w /\(\)]+?)(?:\s+=\s+([\S\s]+?))?(?=\n\s{10}\w|\n{2})", entry_content, flags=re.MULTILINE)
            tmp_content[entry_name] = {}
            for opt in entry_content:
                key = opt[0]
                value = opt[1]
                if key in ["UMID"]:
                    value = re.sub(r"[ \n]+", "<sep>", value).split('<sep>')
                    value = [x for x in value if x]

                if key not in tmp_content[entry_name]:
                    tmp_content[entry_name][key] = value

        return tmp_content

    def parse_entries_sysmod(self, content):
        input_content = re.sub(r"\n+", r"\n", content)
        entries = re.findall(r"(^\S+ +[\s\S]+?)(?=^\S+|\n$)", input_content, flags=re.MULTILINE)
        tmp_content = {}
        for entry in entries:
            entry_name = re.findall(r"^([\S-]+)", entry)[0]
            entry_content = entry + "\n\n"
            entry_content = re.findall(r"^.{10}([\w /\(\)]+?)(?:\s+=\s+([\S\s]+?))?(?=\n\s{10}\w|\n{2})", entry_content, flags=re.MULTILINE)
            tmp_content[entry_name] = {}
            for opt in entry_content:
                key = opt[0]
                value = opt[1]
                version = ""
                if re.search(r"\w+ +VER\(\d+\)", key):
                    key, version = re.findall(r"^(\w+) +VER\((\d+)\)$", opt[0])[0]

                if key in ["ACCEPT ZONE", "APPLY ZONE", "DATA", "DELETE", "DLMOD", "ERROR", "EXEC",
                            "FMID", "JAR", "JARUPD", "MAC", "MACUPD", "MOD", "MSGENU", "NPRE",
                            "PARM", "PNLENU", "PRE", "PROGRAM", "REQ", "RLMOD", "SAMP", "SKL", "SOURCEID", 
                            "SRC", "SRCUPD", "SUPING", "TBL", "VERS", "ZAP"]:
                    value = re.sub(r"[ \n]+", "<sep>", value).split('<sep>')
                    value = [x for x in value if x]
                elif key in ['DATE/TIME REC']:
                    ins = re.findall(r".+\n +INS += +(.+)", value)
                    if len(ins) > 0:
                        value = re.sub(r"(.+)\n[\s\S]+", r"\1", value)
                        tmp_content[entry_name]['DATE/TIME INS'] = ins[0]
                if key not in tmp_content[entry_name] and key.find('HOLD') == -1:
                    tmp_content[entry_name][key] = value
                
                if key.find('HOLD') == 0:
                    if key not in tmp_content[entry_name]:
                        tmp_content[entry_name][key] = {}
                    hold_reason, hold_content = re.findall(r"^(\w+) +([\s\S]+)", value)[0]
                    if hold_reason not in tmp_content[entry_name][key]:
                        tmp_content[entry_name][key][hold_reason] = []
                    tmp_content[entry_name][key][hold_reason].append(hold_content)

        return tmp_content

    def parse_entries_utility(self, content):
        input_content = re.sub(r"\n+", r"\n", content)
        entries = re.findall(r"(^\S+ +[\s\S]+?)(?=^\S+|\n$)", input_content, flags=re.MULTILINE)
        tmp_content = {}
        for entry in entries:
            entry_name = re.findall(r"^([\S-]+)", entry)[0]
            entry_content = entry + "\n\n"
            entry_content = re.findall(r"^.{10}([\w /\(\)]+?)(?:\s+=\s+([\S\s]+?))?(?=\n\s{10}\w|\n{2})", entry_content, flags=re.MULTILINE)
            tmp_content[entry_name] = {}
            for opt in entry_content:
                key = opt[0]
                value = opt[1]

                if key not in tmp_content[entry_name]:
                    tmp_content[entry_name][key] = value

        return tmp_content

    def parse_entries_zone(self, content):
        input_content = re.sub(r"\n+", r"\n", content)
        entries = re.findall(r"(^\S+ +[\s\S]+?)(?=^\S+|\n$)", input_content, flags=re.MULTILINE)
        tmp_content = {}
        for entry in entries:
            entry_name = re.findall(r"^([\S-]+)", entry)[0]
            entry_content = entry + "\n\n"
            entry_content = re.findall(r"^.{10}([\w /\(\)]+?)(?:\s+=\s+([\S\s]+?))?(?=\n\s{10}\w|\n{2})", entry_content, flags=re.MULTILINE)
            tmp_content[entry_name] = {}
            for opt in entry_content:
                key = opt[0]
                value = opt[1]
                if key in ["FMID", "SREL", "TIEDTO"]:
                    value = re.sub(r"[ \n]+", "<sep>", value).split('<sep>')
                    value = [x for x in value if x]
                elif key in ["ZONEINDEX"]:
                    zoneindexes = re.findall(r"(\S+) +(\S+) +(\S+)", value)
                    value = list(map(lambda x: {"NAME": x[0], "TYPE": x[1], "CSI": x[2]}, zoneindexes))
                elif key in ["ACCJCLIN"]:
                    value = "YES"

                if key not in tmp_content[entry_name]:
                    tmp_content[entry_name][key] = value

        return tmp_content

    def parse_entries_zoneset(self, content):
        input_content = re.sub(r"\n+", r"\n", content)
        entries = re.findall(r"(^\S+ +[\s\S]+?)(?=^\S+|\n$)", input_content, flags=re.MULTILINE)
        tmp_content = {}
        for entry in entries:
            entry_name = re.findall(r"^([\S-]+)", entry)[0]
            entry_content = entry + "\n\n"
            entry_content = re.findall(r"^.{10}([\w /\(\)]+?)(?:\s+=\s+([\S\s]+?))?(?=\n\s{10}\w|\n{2})", entry_content, flags=re.MULTILINE)
            tmp_content[entry_name] = {}
            for opt in entry_content:
                key = opt[0]
                value = opt[1]
                if key in ["ZONE"]:
                    value = re.sub(r"[ \n]+", "<sep>", value).split('<sep>')
                    value = [x for x in value if x]

                if key not in tmp_content[entry_name]:
                    tmp_content[entry_name][key] = value

        return tmp_content

    def group_contents(self, content, overall_content, entry_type, zone):
        new_content = overall_content
        if zone not in new_content:
            new_content[zone] = {}
        if entry_type not in new_content[zone]:
            new_content[zone][entry_type] = ""
        tmp_content = new_content[zone][entry_type]
        tmp_content += re.sub(r"\n\n", r"\n", content)
        new_content[zone][entry_type] = tmp_content
        return new_content

    def select_parse_function(self, content, entry_type):
        if entry_type in ['ASSEMBLER']:
            new_content = self.parse_entries_assembler(content)
        if entry_type in ['CLIST',  'BOOK',  'BOOKARA',  'BOOKCHS',  'BOOKCHT',  'BOOKDAN',  'BOOKDES',  'BOOKDEU',  'BOOKELL',  'BOOKENG',  'BOOKENP',  'BOOKENU',  'BOOKESP',  'BOOKFIN',  'BOOKFRA',  'BOOKFRB',  'BOOKFRC',  'BOOKFRS',  'BOOKHEB',  'BOOKISL',  'BOOKITA',  'BOOKITS',  'BOOKJPN',  'BOOKKOR',  'BOOKNLB',  'BOOKNLD',  'BOOKNOR',  'BOOKPTB',  'BOOKPTG',  'BOOKRMS',  'BOOKRUS',  'BOOKSVE',  'BOOKTHA',  'BOOKTRK',  'BSIND',  'BSINDARA',  'BSINDCHS',  'BSINDCHT',  'BSINDDAN',  'BSINDDES',  'BSINDDEU',  'BSINDELL',  'BSINDENG',  'BSINDENP',  'BSINDENU',  'BSINDESP',  'BSINDFIN',  'BSINDFRA',  'BSINDFRB',  'BSINDFRC',  'BSINDFRS',  'BSINDHEB',  'BSINDISL',  'BSINDITA',  'BSINDITS',  'BSINDJPN',  'BSINDKOR',  'BSINDNLB',  'BSINDNLD',  'BSINDNOR',  'BSINDPTB',  'BSINDPTG',  'BSINDRMS',  'BSINDRUS',  'BSINDSVE',  'BSINDTHA',  'BSINDTRK',  'CGM',  'CGMARA',  'CGMCHS',  'CGMCHT',  'CGMDAN',  'CGMDES',  'CGMDEU',  'CGMELL',  'CGMENG',  'CGMENP',  'CGMENU',  'CGMESP',  'CGMFIN',  'CGMFRA',  'CGMFRB',  'CGMFRC',  'CGMFRS',  'CGMHEB',  'CGMISL',  'CGMITA',  'CGMITS',  'CGMJPN',  'CGMKOR',  'CGMNLB',  'CGMNLD',  'CGMNOR',  'CGMPTB',  'CGMPTG',  'CGMRMS',  'CGMRUS',  'CGMSVE',  'CGMTHA',  'CGMTRK',  'DATA',  'DATA1',  'DATA2',  'DATA3',  'DATA4',  'DATA5',  'DATA6',  'DATA6ARA',  'DATA6CHS',  'DATA6CHT',  'DATA6DAN',  'DATA6DES',  'DATA6DEU',  'DATA6ELL',  'DATA6ENG',  'DATA6ENP',  'DATA6ENU',  'DATA6ESP',  'DATA6FIN',  'DATA6FRA',  'DATA6FRB',  'DATA6FRC',  'DATA6FRS',  'DATA6HEB',  'DATA6ISL',  'DATA6ITA',  'DATA6ITS',  'DATA6JPN',  'DATA6KOR',  'DATA6NLB',  'DATA6NLD',  'DATA6NOR',  'DATA6PTB',  'DATA6PTG',  'DATA6RMS',  'DATA6RUS',  'DATA6SVE',  'DATA6THA',  'DATA6TRK',  'EXEC',  'FONT',  'FONTARA',  'FONTCHS',  'FONTCHT',  'FONTDAN',  'FONTDES',  'FONTDEU',  'FONTELL',  'FONTENG',  'FONTENP',  'FONTENU',  'FONTESP',  'FONTFIN',  'FONTFRA',  'FONTFRB',  'FONTFRC',  'FONTFRS',  'FONTHEB',  'FONTISL',  'FONTITA',  'FONTITS',  'FONTJPN',  'FONTKOR',  'FONTNLB',  'FONTNLD',  'FONTNOR',  'FONTPTB',  'FONTPTG',  'FONTRMS',  'FONTRUS',  'FONTSVE',  'FONTTHA',  'FONTTRK',  'GDF',  'GDFARA',  'GDFCHS',  'GDFCHT',  'GDFDAN',  'GDFDES',  'GDFDEU',  'GDFELL',  'GDFENG',  'GDFENP',  'GDFENU',  'GDFESP',  'GDFFIN',  'GDFFRA',  'GDFFRB',  'GDFFRC',  'GDFFRS',  'GDFHEB',  'GDFISL',  'GDFITA',  'GDFITS',  'GDFJPN',  'GDFKOR',  'GDFNLB',  'GDFNLD',  'GDFNOR',  'GDFPTB',  'GDFPTG',  'GDFRMS',  'GDFRUS',  'GDFSVE',  'GDFTHA',  'GDFTRK',  'HELP',  'HELPARA',  'HELPCHS',  'HELPCHT',  'HELPDAN',  'HELPDES',  'HELPDEU',  'HELPELL',  'HELPENG',  'HELPENP',  'HELPENU',  'HELPESP',  'HELPFIN',  'HELPFRA',  'HELPFRB',  'HELPFRC',  'HELPFRS',  'HELPHEB',  'HELPISL',  'HELPITA',  'HELPITS',  'HELPJPN',  'HELPKOR',  'HELPNLB',  'HELPNLD',  'HELPNOR',  'HELPPTB',  'HELPPTG',  'HELPRMS',  'HELPRUS',  'HELPSVE',  'HELPTHA',  'HELPTRK',  'IMG',  'IMGARA',  'IMGCHS',  'IMGCHT',  'IMGDAN',  'IMGDES',  'IMGDEU',  'IMGELL',  'IMGENG',  'IMGENP',  'IMGENU',  'IMGESP',  'IMGFIN',  'IMGFRA',  'IMGFRB',  'IMGFRC',  'IMGFRS',  'IMGHEB',  'IMGISL',  'IMGITA',  'IMGITS',  'IMGJPN',  'IMGKOR',  'IMGNLB',  'IMGNLD',  'IMGNOR',  'IMGPTB',  'IMGPTG',  'IMGRMS',  'IMGRUS',  'IMGSVE',  'IMGTHA',  'IMGTRK',  'MSG',  'MSGARA',  'MSGCHS',  'MSGCHT',  'MSGDAN',  'MSGDES',  'MSGDEU',  'MSGELL',  'MSGENG',  'MSGENP',  'MSGENU',  'MSGESP',  'MSGFIN',  'MSGFRA',  'MSGFRB',  'MSGFRC',  'MSGFRS',  'MSGHEB',  'MSGISL',  'MSGITA',  'MSGITS',  'MSGJPN',  'MSGKOR',  'MSGNLB',  'MSGNLD',  'MSGNOR',  'MSGPTB',  'MSGPTG',  'MSGRMS',  'MSGRUS',  'MSGSVE',  'MSGTHA',  'MSGTRK',  'PARM',  'PNL',  'PNLARA',  'PNLCHS',  'PNLCHT',  'PNLDAN',  'PNLDES',  'PNLDEU',  'PNLELL',  'PNLENG',  'PNLENP',  'PNLENU',  'PNLESP',  'PNLFIN',  'PNLFRA',  'PNLFRB',  'PNLFRC',  'PNLFRS',  'PNLHEB',  'PNLISL',  'PNLITA',  'PNLITS',  'PNLJPN',  'PNLKOR',  'PNLNLB',  'PNLNLD',  'PNLNOR',  'PNLPTB',  'PNLPTG',  'PNLRMS',  'PNLRUS',  'PNLSVE',  'PNLTHA',  'PNLTRK',  'PROBJ',  'PROBJARA',  'PROBJCHS',  'PROBJCHT',  'PROBJDAN',  'PROBJDES',  'PROBJDEU',  'PROBJELL',  'PROBJENG',  'PROBJENP',  'PROBJENU',  'PROBJESP',  'PROBJFIN',  'PROBJFRA',  'PROBJFRB',  'PROBJFRC',  'PROBJFRS',  'PROBJHEB',  'PROBJISL',  'PROBJITA',  'PROBJITS',  'PROBJJPN',  'PROBJKOR',  'PROBJNLB',  'PROBJNLD',  'PROBJNOR',  'PROBJPTB',  'PROBJPTG',  'PROBJRMS',  'PROBJRUS',  'PROBJSVE',  'PROBJTHA',  'PROBJTRK',  'PROC',  'PRODXML',  'PRSRC',  'PRSRCARA',  'PRSRCCHS',  'PRSRCCHT',  'PRSRCDAN',  'PRSRCDES',  'PRSRCDEU',  'PRSRCELL',  'PRSRCENG',  'PRSRCENP',  'PRSRCENU',  'PRSRCESP',  'PRSRCFIN',  'PRSRCFRA',  'PRSRCFRB',  'PRSRCFRC',  'PRSRCFRS',  'PRSRCHEB',  'PRSRCISL',  'PRSRCITA',  'PRSRCITS',  'PRSRCJPN',  'PRSRCKOR',  'PRSRCNLB',  'PRSRCNLD',  'PRSRCNOR',  'PRSRCPTB',  'PRSRCPTG',  'PRSRCRMS',  'PRSRCRUS',  'PRSRCSVE',  'PRSRCTHA',  'PRSRCTRK',  'PSEG',  'PSEGARA',  'PSEGCHS',  'PSEGCHT',  'PSEGDAN',  'PSEGDES',  'PSEGDEU',  'PSEGELL',  'PSEGENG',  'PSEGENP',  'PSEGENU',  'PSEGESP',  'PSEGFIN',  'PSEGFRA',  'PSEGFRB',  'PSEGFRC',  'PSEGFRS',  'PSEGHEB',  'PSEGISL',  'PSEGITA',  'PSEGITS',  'PSEGJPN',  'PSEGKOR',  'PSEGNLB',  'PSEGNLD',  'PSEGNOR',  'PSEGPTB',  'PSEGPTG',  'PSEGRMS',  'PSEGRUS',  'PSEGSVE',  'PSEGTHA',  'PSEGTRK',  'PUBLB',  'PUBLBARA',  'PUBLBCHS',  'PUBLBCHT',  'PUBLBDAN',  'PUBLBDES',  'PUBLBDEU',  'PUBLBELL',  'PUBLBENG',  'PUBLBENP',  'PUBLBENU',  'PUBLBESP',  'PUBLBFIN',  'PUBLBFRA',  'PUBLBFRB',  'PUBLBFRC',  'PUBLBFRS',  'PUBLBHEB',  'PUBLBISL',  'PUBLBITA',  'PUBLBITS',  'PUBLBJPN',  'PUBLBKOR',  'PUBLBNLB',  'PUBLBNLD',  'PUBLBNOR',  'PUBLBPTB',  'PUBLBPTG',  'PUBLBRMS',  'PUBLBRUS',  'PUBLBSVE',  'PUBLBTHA',  'PUBLBTRK',  'SAMP',  'SAMPARA',  'SAMPCHS',  'SAMPCHT',  'SAMPDAN',  'SAMPDES',  'SAMPDEU',  'SAMPELL',  'SAMPENG',  'SAMPENP',  'SAMPENU',  'SAMPESP',  'SAMPFIN',  'SAMPFRA',  'SAMPFRB',  'SAMPFRC',  'SAMPFRS',  'SAMPHEB',  'SAMPISL',  'SAMPITA',  'SAMPITS',  'SAMPJPN',  'SAMPKOR',  'SAMPNLB',  'SAMPNLD',  'SAMPNOR',  'SAMPPTB',  'SAMPPTG',  'SAMPRMS',  'SAMPRUS',  'SAMPSVE',  'SAMPTHA',  'SAMPTRK',  'SKL',  'SKLARA',  'SKLCHS',  'SKLCHT',  'SKLDAN',  'SKLDES',  'SKLDEU',  'SKLELL',  'SKLENG',  'SKLENP',  'SKLENU',  'SKLESP',  'SKLFIN',  'SKLFRA',  'SKLFRB',  'SKLFRC',  'SKLFRS',  'SKLHEB',  'SKLISL',  'SKLITA',  'SKLITS',  'SKLJPN',  'SKLKOR',  'SKLNLB',  'SKLNLD',  'SKLNOR',  'SKLPTB',  'SKLPTG',  'SKLRMS',  'SKLRUS',  'SKLSVE',  'SKLTHA',  'SKLTRK',  'TBL',  'TBLARA',  'TBLCHS',  'TBLCHT',  'TBLDAN',  'TBLDES',  'TBLDEU',  'TBLELL',  'TBLENG',  'TBLENP',  'TBLENU',  'TBLESP',  'TBLFIN',  'TBLFRA',  'TBLFRB',  'TBLFRC',  'TBLFRS',  'TBLHEB',  'TBLISL',  'TBLITA',  'TBLITS',  'TBLJPN',  'TBLKOR',  'TBLNLB',  'TBLNLD',  'TBLNOR',  'TBLPTB',  'TBLPTG',  'TBLRMS',  'TBLRUS',  'TBLSVE',  'TBLTHA',  'TBLTRK',  'TEXT',  'TEXTARA',  'TEXTCHS',  'TEXTCHT',  'TEXTDAN',  'TEXTDES',  'TEXTDEU',  'TEXTELL',  'TEXTENG',  'TEXTENP',  'TEXTENU',  'TEXTESP',  'TEXTFIN',  'TEXTFRA',  'TEXTFRB',  'TEXTFRC',  'TEXTFRS',  'TEXTHEB',  'TEXTISL',  'TEXTITA',  'TEXTITS',  'TEXTJPN',  'TEXTKOR',  'TEXTNLB',  'TEXTNLD',  'TEXTNOR',  'TEXTPTB',  'TEXTPTG',  'TEXTRMS',  'TEXTRUS',  'TEXTSVE',  'TEXTTHA',  'TEXTTRK',  'USER1',  'USER2',  'USER3',  'USER4',  'USER5',  'UTIN',  'UTINARA',  'UTINCHS',  'UTINCHT',  'UTINDAN',  'UTINDES',  'UTINDEU',  'UTINELL',  'UTINENG',  'UTINENP',  'UTINENU',  'UTINESP',  'UTINFIN',  'UTINFRA',  'UTINFRB',  'UTINFRC',  'UTINFRS',  'UTINHEB',  'UTINISL',  'UTINITA',  'UTINITS',  'UTINJPN',  'UTINKOR',  'UTINNLB',  'UTINNLD',  'UTINNOR',  'UTINPTB',  'UTINPTG',  'UTINRMS',  'UTINRUS',  'UTINSVE',  'UTINTHA',  'UTINTRK',  'UTOUT',  'UTOUTARA',  'UTOUTCHS',  'UTOUTCHT',  'UTOUTDAN',  'UTOUTDES',  'UTOUTDEU',  'UTOUTELL',  'UTOUTENG',  'UTOUTENP',  'UTOUTENU',  'UTOUTESP',  'UTOUTFIN',  'UTOUTFRA',  'UTOUTFRB',  'UTOUTFRC',  'UTOUTFRS',  'UTOUTHEB',  'UTOUTISL',  'UTOUTITA',  'UTOUTITS',  'UTOUTJPN',  'UTOUTKOR',  'UTOUTNLB',  'UTOUTNLD',  'UTOUTNOR',  'UTOUTPTB',  'UTOUTPTG',  'UTOUTRMS',  'UTOUTRUS',  'UTOUTSVE',  'UTOUTTHA',  'UTOUTTRK']:
            new_content = self.parse_entries_data(content)
        elif entry_type in ['DDDEF']:
            new_content = self.parse_entries_dddef(content)
        elif entry_type in ['DLIB']:
            new_content = self.parse_entries_dlib(content)
        elif entry_type in ['FEATURE']:
            new_content = self.parse_entries_feature(content)
        elif entry_type in ['FMIDSET']:
            new_content = self.parse_entries_fmidset(content)
        elif entry_type in ['AIX1', 'AIX2', 'AIX3', 'AIX4', 'AIX5', 'CLIENT1', 'CLIENT2', 'CLIENT3', 'CLIENT4', 'CLIENT5', 'HFS', 'OS21', 'OS22', 'OS23', 'OS24', 'OS25', 'SHELLSCR', 'UNIX1', 'UNIX2', 'UNIX3', 'UNIX4', 'UNIX5', 'WIN1', 'WIN2', 'WIN3', 'WIN4', 'WIN5', 'HFSARA', 'HFSCHS', 'HFSCHT', 'HFSDAN', 'HFSDES', 'HFSDEU', 'HFSELL', 'HFSENG', 'HFSENP', 'HFSENU', 'HFSESP', 'HFSFIN', 'HFSFRA', 'HFSFRB', 'HFSFRC', 'HFSFRS', 'HFSHEB', 'HFSISL', 'HFSITA', 'HFSITS', 'HFSJPN', 'HFSKOR', 'HFSNLB', 'HFSNLD', 'HFSNOR', 'HFSPTB', 'HFSPTG', 'HFSRMS', 'HFSRUS', 'HFSSVE', 'HFSTHA', 'HFSTRK']:
            new_content = self.parse_entries_hfs(content)
        elif entry_type in ['HOLDDATA']:
            new_content = self.parse_entries_holddata(content)
        elif entry_type in ['JAR']:
            new_content = self.parse_entries_jar(content)
        elif entry_type in ['LMOD']:
            new_content = self.parse_entries_lmod(content)
        elif entry_type in ['MACRO']:
            new_content = self.parse_entries_mac(content)
        elif entry_type in ['MODULE']:
            new_content = self.parse_entries_mod(content)
        elif entry_type in ['OPTIONS']:
            new_content = self.parse_entries_options(content)
        elif entry_type in ['ORDER']:
            new_content = self.parse_entries_order(content)
        elif entry_type in ['PRODUCT']:
            new_content = self.parse_entries_product(content)
        elif entry_type in ['PROGRAM']:
            new_content = self.parse_entries_program(content)
        elif entry_type in ['SOURCE']:
            new_content = self.parse_entries_source(content)
        elif entry_type in ['SYSMOD']:
            new_content = self.parse_entries_sysmod(content)
        elif entry_type in ['UTILITY']:
            new_content = self.parse_entries_utility(content)
        elif entry_type in ['ZONE']:
            new_content = self.parse_entries_zone(content)
        elif entry_type in ['ZONESET']:
            new_content = self.parse_entries_zoneset(content)
        else:
            new_content = content
        return(new_content)

    def parse_gimsmp_list(self, cmd_response):
        try:
            result = {}
            # Ensure trailing spaces are trimmed
            input_content = re.sub(r" +\n ?", r"\n", cmd_response)
            #input_content = re.sub(r" +\n", r"\n", re.sub(r"(?:\f|\\f|\x0c|\d)PAGE \d+.+NOW SET TO.+", r"\n", cmd_response))

            # Replace line breaks with chars to facilitate parsing
            input_content = re.sub(r"(?:\f|\\f|\x0c|1)PAGE \d+.+NOW SET TO.+", r"\n", input_content)
            #return(input_content)
            overall_content = {}
            entries = re.findall(r"(\S+) +(\S+) +ENTRIES\s+((?:[\s\S])*?)\n(?=\S+ +\S+ +ENTRIES|LIST +SUMMARY REPORT)", input_content, flags=re.MULTILINE)
            for entry in entries:
                zone = entry[0]
                entry_type = entry[1]
                entry_content = entry[2]
                entry_content = re.sub(r"^NAME\n\n", r"", entry[2], flags=re.MULTILINE)

                if zone not in overall_content:
                    overall_content[zone] = {}

                overall_content = self.group_contents(entry_content, overall_content, entry_type, zone)
                
                if entry_type not in overall_content[zone]:
                    overall_content[zone][entry_type] = entry_content

            for zone in overall_content:
                for entry_type in overall_content[zone]:
                    overall_content[zone][entry_type] = self.select_parse_function(overall_content[zone][entry_type], entry_type)

            return overall_content
        except Exception as e:
            return e

    def parse_gimsmp(self, cmd_response, option):
        if not isinstance(cmd_response, list) and not isinstance(cmd_response, str):
            raise AnsibleFilterTypeError("parse_gimsmp - Filter must be applied on a list or string")
        elif isinstance(cmd_response, list):
            joined_content = '\n'.join(cmd_response)
        elif isinstance(cmd_response, str):
            joined_content = cmd_response

        if not isinstance(option, str):
            raise AnsibleFilterTypeError("parse_gimsmp - 'option' must be a string.")

        possible_options = ["LIST"]
        option = option.upper()

        if option not in possible_options:
            raise AnsibleFilterTypeError("parse_gimsmp - 'option' must be one of the following: %s" % str(possible_options))

        if option == "LIST":
            result = self.parse_gimsmp_list(joined_content)
        
        return(result)