from ubtres import db
from ubtres.models import Result

def get_defconfig_data(defconfig, count):
    result = Result.query.filter(Result.defconfig==defconfig).all()
    if result == None:
        return None, None, None

    i = 0
    dates = []
    splsizes = []
    ubsizes = []
    for res in reversed(result):
        d = res.to_dict()
        dates.insert(0, d["basecommit"])
        ubsizes.insert(0, d["ubsize"])
        splsizes.insert(0, d["splsize"])
        i += 1
        if i == count:
            return dates, splsizes, ubsizes

    return dates, splsizes, ubsizes


