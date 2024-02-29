def keyword_mapper(subjects):
    subject_list = subjects.get("subject", {})
    if not isinstance(subject_list, list):
        subject_list = [subject_list]
    ret = [y.get("value") for y in subject_list]
    return ret
