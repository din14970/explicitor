def _equal_errors(e1: BaseException, e2: BaseException) -> bool:
    return isinstance(e1, type(e2)) and (e1.args == e2.args)
