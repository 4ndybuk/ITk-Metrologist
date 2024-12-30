from gspread_formatting import *
from gspread import worksheet
from multiprocessing import Queue

"""
Setting conditional formatting rules for the Google Sheets when uploading metrology results
"""

rule_dict = {"pass": 'NUMBER_BETWEEN',
            "fail": 'NUMBER_NOT_BETWEEN',
            "green": Color(0.8,1,0.8),
            "red": Color(1,0.9,0.9)}

def conditional_rule(sheet: worksheet,range,condition,values,color_range):
    rule = ConditionalFormatRule(ranges=[GridRange.from_a1_range(range,sheet)],
                                 booleanRule=BooleanRule(
                                 condition=BooleanCondition(condition,values),
                                 format=CellFormat(backgroundColor = color_range)))
    return rule

def hybrid_rules(sheet: worksheet,queue: Queue):
    """
    Creating and storing custom rules for the Hybrid spreadsheet
    """

    queue.put(45)

    rules = get_conditional_format_rules(sheet)

    rules.clear()

    queue.put(50)

    x_rule_pass = conditional_rule(sheet,'F:F',rule_dict["pass"],['39.5','39.7'],rule_dict["green"]) 
    rules.append(x_rule_pass)

    x_rule_fail = conditional_rule(sheet,'F:F',rule_dict["fail"],['39.5','39.7'],rule_dict["red"]) 
    rules.append(x_rule_fail)

    queue.put(55)

    y_rule_pass = conditional_rule(sheet,'G:G',rule_dict["pass"],['40.50','40.70'],rule_dict["green"])
    rules.append(y_rule_pass)
    
    y_rule_fail = conditional_rule(sheet,'G:G',rule_dict["fail"],['40.50','40.70'],rule_dict["red"])
    rules.append(y_rule_fail)

    queue.put(60)

    quad_rule_pass = conditional_rule(sheet,'H:K',rule_dict["pass"],['201.0','301.0'],rule_dict["green"])
    rules.append(quad_rule_pass)
    
    quad_rule_fail = conditional_rule(sheet,'H:K',rule_dict["fail"],['201.0','301.0'],rule_dict["red"])
    rules.append(quad_rule_fail)

    queue.put(65)

    hv_rule_pass = conditional_rule(sheet,'P:P',rule_dict["pass"],['1.701','2.001'],rule_dict["green"])
    rules.append(hv_rule_pass)
    
    hv_rule_fail = conditional_rule(sheet,'P:P',rule_dict["fail"],['1.701','2.001'],rule_dict["red"])
    rules.append(hv_rule_fail)

    queue.put(70)
    
    ftm_rule_pass = conditional_rule(sheet,'Q:Q',rule_dict["pass"],['1.521','1.761'],rule_dict["green"])
    rules.append(ftm_rule_pass)
    
    ftm_rule_fail = conditional_rule(sheet,'Q:Q',rule_dict["fail"],['1.521','1.761'],rule_dict["red"])
    rules.append(ftm_rule_fail)

    rules.save()

    queue.put(75)

def bare_rules(sheet: worksheet,queue: Queue):

    """
    Creating and storing custom rules for the Bare modules spreadsheet
    """
    queue.put(45)

    rules = get_conditional_format_rules(sheet)

    rules.clear()

    queue.put(50)

    fex_rule_pass = conditional_rule(sheet,'G:G',rule_dict["pass"],['42.187','42.257'],rule_dict["green"])
    rules.append(fex_rule_pass)
    
    fex_rule_fail = conditional_rule(sheet,'G:G',rule_dict["fail"],['42.187','42.257'],rule_dict["red"])
    rules.append(fex_rule_fail)

    queue.put(55)

    fey_rule_pass = conditional_rule(sheet,'H:H',rule_dict["pass"],['40.255','40.325'],rule_dict["green"])
    rules.append(fey_rule_pass)
    
    fey_rule_fail = conditional_rule(sheet,'H:H',rule_dict["fail"],['40.255','40.325'],rule_dict["red"])
    rules.append(fey_rule_fail)

    queue.put(60)

    senx_rule_pass = conditional_rule(sheet,'I:I',rule_dict["pass"],['39.5','39.55'],rule_dict["green"])
    rules.append(senx_rule_pass)

    senx_rule_fail = conditional_rule(sheet,'I:I',rule_dict["fail"],['39.5','39.55'],rule_dict["red"])
    rules.append(senx_rule_fail)

    queue.put(65)

    seny_rule_pass = conditional_rule(sheet,'J:J',rule_dict["pass"],['41.1','41.15'],rule_dict["green"])
    rules.append(seny_rule_pass)

    seny_rule_fail = conditional_rule(sheet,'J:J',rule_dict["fail"],['41.1','41.15'],rule_dict["red"])
    rules.append(seny_rule_fail)

    queue.put(70)

    fe_rule_pass = conditional_rule(sheet,'K:K',rule_dict["pass"],['0.140','0.175'],rule_dict["green"])
    rules.append(fe_rule_pass)

    fe_rule_fail = conditional_rule(sheet,'K:K',rule_dict["fail"],['0.140','0.175'],rule_dict["red"])
    rules.append(fe_rule_fail)

    bare_rule_pass = conditional_rule(sheet,'M:M',rule_dict["pass"],['0.285','0.415'],rule_dict["green"])
    rules.append(bare_rule_pass)

    bare_rule_fail = conditional_rule(sheet,'M:M',rule_dict["fail"],['0.285','0.415'],rule_dict["red"])
    rules.append(bare_rule_fail)

    rules.save()

    queue.put(75)

def assem_rules(sheet: worksheet,queue: Queue):

    """
    Creating and storing custom rules for the Asesembled modules spreadsheet
    """
    queue.put(45)

    rules = get_conditional_format_rules(sheet)

    queue.put(50)

    xa_rule_pass = conditional_rule(sheet,'H:H',rule_dict["pass"],['42.187','42.257'],rule_dict["green"])
    rules.append(xa_rule_pass)
    
    xa_rule_fail = conditional_rule(sheet,'H:H',rule_dict["fail"],['42.187','42.257'],rule_dict["red"])
    rules.append(xa_rule_fail)

    queue.put(55)

    ya_rule_pass = conditional_rule(sheet,'I:I',rule_dict["pass"],['41.1','41.15'],rule_dict["green"])
    rules.append(ya_rule_pass)
    
    ya_rule_fail = conditional_rule(sheet,'I:I',rule_dict["fail"],['41.1','41.15'],rule_dict["red"])
    rules.append(ya_rule_fail)

    queue.put(60)

    quadA_rule_pass = conditional_rule(sheet,'J:N',rule_dict["pass"],['466.0','721.0'],rule_dict["green"])
    rules.append(quadA_rule_pass)
    
    quadA_rule_fail = conditional_rule(sheet,'J:N',rule_dict["fail"],['466.0','721.0'],rule_dict["red"])
    rules.append(quadA_rule_fail)

    queue.put(65)

    ftma_rule_pass = conditional_rule(sheet,'S:S',rule_dict["pass"],['1.781','2.181'],rule_dict["green"])
    rules.append(ftma_rule_pass)
    
    ftma_rule_fail = conditional_rule(sheet,'S:S',rule_dict["fail"],['1.781','2.181'],rule_dict["red"])
    rules.append(ftma_rule_fail)

    queue.put(70)

    hva_rule_pass = conditional_rule(sheet,'T:T',rule_dict["pass"],['1.961','2.531'],rule_dict["green"])
    rules.append(hva_rule_pass)
    
    hva_rule_fail = conditional_rule(sheet,'T:T',rule_dict["fail"],['1.961','2.531'],rule_dict["red"])
    rules.append(hva_rule_fail)

    rules.save()

    queue.put(75)