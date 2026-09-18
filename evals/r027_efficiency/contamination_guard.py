from pathlib import PurePosixPath

def validate_changed_paths(changed_paths:list[str],allowed_paths:list[str])->None:
 allowed={str(PurePosixPath(p)) for p in allowed_paths};observed={str(PurePosixPath(p)) for p in changed_paths};extra=sorted(observed-allowed)
 if extra:raise ValueError(f"out-of-scope changed paths: {extra}")
def validate_no_cross_arm_refs(text:str,current_arm:str,all_arm_ids:list[str])->None:
 forbidden=sorted(a for a in all_arm_ids if a!=current_arm and a in text)
 if forbidden:raise ValueError(f"cross-arm references detected: {forbidden}")
