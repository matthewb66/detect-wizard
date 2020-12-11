import texttable


class WizardLogger(object):
    """
    This class represents the logging interface for the variable sensitivity system.
    """
    def __init__(self):
        self._log_dict = dict()

    def log(self, topic, causes, outcome, description):
        if topic not in self._log_dict:
            self._log_dict[topic] = set()
        self._log_dict[topic].add(((causes, ) if type(causes) == str else tuple(causes), outcome, description))

    def make_table(self, sensitivity_value=None):
        data_rows = []
        data_rows_no_op = []
        for topic, cod_list in self._log_dict.items():
            for idx, (cause, outcome, description) in enumerate(cod_list):
                if type(outcome) == tuple:
                    outcome = '\n'.join(outcome)
                if outcome == "NO-OP":
                    if idx == 0:
                        data_rows_no_op.append([topic, ', '.join(cause), description])
                    else:
                        data_rows_no_op.append(["", ', '.join(cause), description])
                else:
                    if idx == 0:
                        data_rows.append([topic, ', '.join(cause), outcome, description])
                    else:
                        data_rows.append(["", ', '.join(cause), outcome, description])
        table_pos = texttable.Texttable(max_width=120)
        table_pos.set_cols_align(["c", "c", "c", "c"])
        table_pos.header(["Actionable", "Reason(s) Action Taken", "Outcome", "Description"])
        table_pos.add_rows(data_rows, header=False)
        table_pos = table_pos.draw()

        table_neg = texttable.Texttable(max_width=120)
        table_neg.set_cols_align(["c", "c", "c"])
        table_neg.header(["Actionable", "Reason(s) Action NOT Taken", "Description"])
        table_neg.add_rows(data_rows_no_op, header=False)
        table_neg = table_neg.draw()

        table_width = max(table_pos.index('\n'), table_neg.index('\n'))
        title = " Sensitivity (= {}) Configuration Manifest ".format(sensitivity_value)
        size = (table_width - len(title)) // 2
        header_str = '-' * size + title + '-' * (size)
        footer_str = '-' * (len(header_str)) + "\n"
        return "{}\nACTIONS TAKEN: \n{}\n{}ACTIONS NOT TAKEN: \n{}\n{}".format(header_str, table_pos, footer_str, table_neg, footer_str)
